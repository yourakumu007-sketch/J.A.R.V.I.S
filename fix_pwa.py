import os

filepath = r"dashboard\server.py"
with open(filepath, "r", encoding="utf-8") as f:
    code = f.read()

# Add a route for manifest.json
old_route = """        @app.get("/static/crypto.js")"""
new_route = """        @app.get("/manifest.json")
        async def serve_manifest():
            return JSONResponse({
                "name": "J.A.R.V.I.S.",
                "short_name": "JARVIS",
                "start_url": "/",
                "display": "standalone",
                "background_color": "#050002",
                "theme_color": "#ff1b2d"
            })

        @app.get("/static/crypto.js")"""
if "/manifest.json" not in code:
    code = code.replace(old_route, new_route)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    print("Added manifest route to server.py")
else:
    print("Manifest route already exists")
