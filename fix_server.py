import os

filepath = r"dashboard\server.py"
with open(filepath, "r", encoding="utf-8") as f:
    code = f.read()

old_port = "PORT        = 8000"
new_port = "import os\nPORT        = int(os.environ.get('JARVIS_PORT', 8000))"
if old_port in code:
    code = code.replace(old_port, new_port)

old_host = 'host="0.0.0.0"'
new_host = 'host=os.environ.get("JARVIS_HOST", "0.0.0.0")'
if old_host in code:
    code = code.replace(old_host, new_host)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(code)
print("Updated server.py")
