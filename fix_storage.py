import os
import re

filepath = r"dashboard\server.py"
with open(filepath, "r", encoding="utf-8") as f:
    code = f.read()

old_upload = """@app.post("/api/upload")
        async def upload_file(req: Request, file: FastAPIFile(...)):
            if not _auth(req):
                return JSONResponse({"error": "Unauthorized"}, status_code=401)"""

new_upload = """@app.post("/api/upload")
        async def upload_file(req: Request, file: FastAPIFile(...)):
            if os.environ.get("RENDER"):
                return JSONResponse({"error": "Cloud file persistence explicitly disabled until object storage (S3) is implemented."}, status_code=503)
            if not _auth(req):
                return JSONResponse({"error": "Unauthorized"}, status_code=401)"""

if "Cloud file persistence explicitly disabled" not in code:
    code = code.replace(old_upload, new_upload)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    print("Disabled uploads on Render")
