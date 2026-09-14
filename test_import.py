import sys

# Fake missing desktop modules
class FakeImportErrorMeta(type):
    def __import__(name, globals=None, locals=None, fromlist=(), level=0):
        if name in ['sounddevice', 'PyQt6', 'pyautogui', 'pyaudio', 'pywin32', 'comtypes']:
            raise ImportError(f"No module named {name}")
        return __import__(name, globals, locals, fromlist, level)

# Replace builtins.__import__
import builtins
orig_import = builtins.__import__
def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name in ['sounddevice', 'PyQt6', 'pyautogui', 'pyaudio', 'pywin32', 'comtypes']:
        raise ImportError(f"No module named {name}")
    return orig_import(name, globals, locals, fromlist, level)
builtins.__import__ = mock_import

try:
    import server_headless
    print("Headless import SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Headless import FAILED")
