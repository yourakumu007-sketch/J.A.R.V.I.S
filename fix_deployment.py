import os
import re

# 1. Update memory_manager.py to support PostgreSQL architecture
mem_path = r"memory\memory_manager.py"
with open(mem_path, "r", encoding="utf-8") as f:
    mem_code = f.read()

new_mem_code = """import json
import os
import sys
from datetime import datetime
from threading import RLock
from pathlib import Path

def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR         = get_base_dir()
MEMORY_PATH      = BASE_DIR / "memory" / "long_term.json"
_lock            = RLock()
MAX_VALUE_LENGTH = 380
MEMORY_MAX_CHARS = 2200

DB_URL = os.environ.get("DATABASE_URL")

def _empty_memory() -> dict:
    return {
        "identity":      {},
        "preferences":   {},
        "projects":      {},
        "relationships": {},
        "wishes":        {},
        "notes":         {},
    }

def _get_db_conn():
    if not DB_URL: return None
    try:
        import psycopg2
        conn = psycopg2.connect(DB_URL)
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS user_memory (user_id VARCHAR PRIMARY KEY, memory JSONB)")
            conn.commit()
        return conn
    except Exception as e:
        print(f"[Memory] DB Init Error: {e}")
        return None

def load_memory(user_id="default") -> dict:
    with _lock:
        try:
            conn = _get_db_conn()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT memory FROM user_memory WHERE user_id = %s", (user_id,))
                    row = cur.fetchone()
                    if row and row[0]:
                        data = row[0] if isinstance(row[0], dict) else json.loads(row[0])
                        base = _empty_memory()
                        for key in base:
                            if key not in data: data[key] = {}
                        return data
                return _empty_memory()
            
            if not MEMORY_PATH.exists():
                return _empty_memory()
            data = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                base = _empty_memory()
                for key in base:
                    if key not in data:
                        data[key] = {}
                return data
            return _empty_memory()
        except Exception as e:
            print(f"[Memory] Load error: {e}")
            return _empty_memory()

def update_memory(new_data: dict, user_id="default") -> None:
    with _lock:
        mem = load_memory(user_id)
        for cat, items in new_data.items():
            if cat not in mem:
                mem[cat] = {}
            if isinstance(items, dict):
                for k, v in items.items():
                    mem[cat][k] = v

        try:
            conn = _get_db_conn()
            if conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO user_memory (user_id, memory) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET memory = EXCLUDED.memory",
                        (user_id, json.dumps(mem))
                    )
                    conn.commit()
                return
            
            MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
            MEMORY_PATH.write_text(json.dumps(mem, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"[Memory] Save error: {e}")

def _all_entries(memory: dict) -> list[tuple]:
    entries = []
    for cat, items in memory.items():
        if not isinstance(items, dict): continue
        for k, v in items.items():
            if isinstance(v, dict):
                entries.append((cat, k, v.get("value", ""), v.get("ts", "")))
    return entries

def format_memory_for_prompt(memory: dict) -> str:
    entries = _all_entries(memory)
    if not entries: return "No long-term memories yet."
    entries.sort(key=lambda x: x[3] if len(x)>3 else "", reverse=True)
    lines = []
    for cat, k, val, ts in entries:
        lines.append(f"- [{cat.upper()}] {k}: {val}")
    out = chr(10).join(lines)
    if len(out) > MEMORY_MAX_CHARS: out = out[:MEMORY_MAX_CHARS] + "... (truncated)"
    return out
"""
if "user_memory" not in mem_code:
    with open(mem_path, "w", encoding="utf-8") as f:
        f.write(new_mem_code)
    print("Updated memory_manager.py for DB support.")

# 2. Add psycopg2 to requirements if not present
req_path = r"requirements.txt"
if os.path.exists(req_path):
    with open(req_path, "r", encoding="utf-8") as f:
        reqs = f.read()
    if "psycopg2-binary" not in reqs:
        with open(req_path, "a", encoding="utf-8") as f:
            f.write("\npsycopg2-binary>=2.9.9\n")
        print("Added psycopg2-binary to requirements.txt")

# 3. Create render.yaml
render_yaml = """services:
  - type: web
    name: jarvis-web
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python main.py"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: jarvis-db
          property: connectionString
      - key: GEMINI_API_KEY
        sync: false
      - key: JARVIS_HOST
        value: "0.0.0.0"

databases:
  - name: jarvis-db
    databaseName: jarvis
    user: jarvis
"""
with open("render.yaml", "w", encoding="utf-8") as f:
    f.write(render_yaml)
print("Created render.yaml")

