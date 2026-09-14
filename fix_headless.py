import os
import re

# 1. Modify main.py imports to be optional
main_path = "main.py"
with open(main_path, "r", encoding="utf-8") as f:
    main_code = f.read()

# Replace sounddevice import
main_code = re.sub(
    r"^import sounddevice as sd$",
    "try:\n    import sounddevice as sd\nexcept ImportError:\n    sd = None",
    main_code,
    flags=re.MULTILINE
)

# Replace ui import
main_code = re.sub(
    r"^from ui import JarvisUI, JarvisUI$",
    "try:\n    from ui import JarvisUI\nexcept ImportError:\n    JarvisUI = None",
    main_code,
    flags=re.MULTILINE
)
main_code = re.sub(
    r"^from ui import JarvisUI$",
    "try:\n    from ui import JarvisUI\nexcept ImportError:\n    JarvisUI = None",
    main_code,
    flags=re.MULTILINE
)

# Add fallback for _origPopen
if "import platform as _platform" in main_code:
    pass

# Safe _mic_loop and _spk_loop
def safe_loop(code, func_name):
    target = f"    async def {func_name}(self):\n"
    replacement = f"    async def {func_name}(self):\n        if sd is None: return\n"
    if target in code and replacement not in code:
        return code.replace(target, replacement)
    return code

main_code = safe_loop(main_code, "_mic_loop")
main_code = safe_loop(main_code, "_spk_loop")

with open(main_path, "w", encoding="utf-8") as f:
    f.write(main_code)
print("Made main.py imports safe.")

# 2. Create server_headless.py
headless_code = """import asyncio
import os
import sys

from dashboard.server import DashboardServer, PORT
from main import JarvisOrchestrator

class HeadlessUI:
    def __init__(self):
        self.muted = False
        self.current_file = None
        # Mock the Window so prompt_reconfig does not hang
        class DummyWin:
            _ready = True
        self._win = DummyWin()
        
    def write_log(self, text): print(text)
    def set_state(self, state): pass
    def notify_phone_connected(self): pass
    def prompt_reconfig(self): print("[Headless] API Key needed in ENV vars.")
    def show_content(self, title, content): print(f"[Headless] Show Content: {title}")
    def stop_camera_stream(self): pass
    def wait_for_api_key(self): pass

async def start_headless():
    ui = HeadlessUI()
    jarvis = JarvisOrchestrator(ui)
    
    server = DashboardServer()
    
    # Add health endpoint
    @server.app.get("/health")
    async def health():
        return {"status": "ok"}
        
    jarvis._dashboard = server
    server.set_connect_callback(jarvis._on_phone_connected)
    
    asyncio.create_task(jarvis._process_dashboard_commands())
    asyncio.create_task(jarvis.run())
    
    port = int(os.environ.get("PORT", os.environ.get("JARVIS_PORT", PORT)))
    import uvicorn
    config = uvicorn.Config(server.app, host="0.0.0.0", port=port, log_level="info")
    srv = uvicorn.Server(config)
    print(f"Starting headless server on port {port}")
    await srv.serve()

if __name__ == "__main__":
    # Remove UI dependencies from sys.modules to simulate missing optional deps
    sys.modules.pop('ui', None)
    asyncio.run(start_headless())
"""

with open("server_headless.py", "w", encoding="utf-8") as f:
    f.write(headless_code)
print("Created server_headless.py")

# 3. Update render.yaml
render_yaml = """services:
  - type: web
    name: jarvis-web
    env: python
    buildCommand: "pip install -r requirements_render.txt"
    startCommand: "python server_headless.py"
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
print("Updated render.yaml")

# 4. Create requirements_render.txt (excluding pyqt6, sounddevice)
reqs = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        for line in f:
            l = line.strip().lower()
            if not l or "pyqt6" in l or "sounddevice" in l or "pyaudio" in l or "opencv" in l or "pycaw" in l or "comtypes" in l:
                continue
            reqs.append(line.strip())
reqs.append("psycopg2-binary>=2.9.9")
with open("requirements_render.txt", "w", encoding="utf-8") as f:
    f.write("\\n".join(reqs))
print("Created requirements_render.txt")

