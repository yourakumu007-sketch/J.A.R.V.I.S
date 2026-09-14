import os
import re

main_path = "main.py"
with open(main_path, "r", encoding="utf-8") as f:
    main_code = f.read()

# Update _get_api_key to prioritize GEMINI_API_KEY from env
old_get_api_key = """def _get_api_key() -> str:
    try:
        with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
            key = json.load(f)["gemini_api_key"]
    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        raise ApiKeyMissing(f"config/api_keys.json is missing or invalid: {e}") from e
    if not key or key.strip() in ("", "YOUR_GEMINI_API_KEY_HERE"):
        raise ApiKeyMissing("No API key set in config/api_keys.json")
    return key"""

new_get_api_key = """def _get_api_key() -> str:
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key and env_key not in ("", "YOUR_GEMINI_API_KEY_HERE"):
        return env_key
    try:
        with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
            key = json.load(f)["gemini_api_key"]
    except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
        raise ApiKeyMissing(f"GEMINI_API_KEY env var missing and config/api_keys.json is invalid: {e}") from e
    if not key or key.strip() in ("", "YOUR_GEMINI_API_KEY_HERE"):
        raise ApiKeyMissing("No API key set in ENV or config/api_keys.json")
    return key"""

if "env_key = os.environ.get" not in main_code:
    main_code = main_code.replace(old_get_api_key, new_get_api_key)
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(main_code)
    print("Updated API key extraction in main.py")
