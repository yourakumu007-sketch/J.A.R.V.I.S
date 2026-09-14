import asyncio
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
