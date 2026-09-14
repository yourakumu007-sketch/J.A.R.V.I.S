import sys
import os
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Remove UI dependencies
sys.modules.pop('ui', None)

from dashboard.server import DashboardServer
from main import JarvisLive

class HeadlessUI:
    def __init__(self):
        self.muted = False
        self.current_file = None
        class DummyWin:
            _ready = True
        self._win = DummyWin()
        
    def write_log(self, text): print(text)
    def set_state(self, state): pass
    def notify_phone_connected(self): pass
    def prompt_reconfig(self): pass
    def show_content(self, title, content): pass
    def stop_camera_stream(self): pass
    def wait_for_api_key(self): pass

# Initialize Dashboard
_server = DashboardServer()

# Add a health endpoint
@_server.app.get("/health")
async def health():
    return {"status": "ok"}

ui = HeadlessUI()
jarvis = JarvisLive(ui)
jarvis._dashboard = _server
_server.set_connect_callback(jarvis._on_phone_connected)

# Start tasks in the background for Vercel's event loop
# Note: Vercel functions are stateless and kill background tasks after request ends.
# WebSockets on standard Serverless functions will fail or drop.
# This code initializes the app but expects short-lived execution unless on Fluid.
@_server.app.on_event("startup")
async def startup_event():
    asyncio.create_task(jarvis._process_dashboard_commands())
    asyncio.create_task(jarvis.run())

app = _server.app
