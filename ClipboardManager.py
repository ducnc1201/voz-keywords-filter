import subprocess
import sys

class ClipboardManager:
    @staticmethod
    def get_clipboard_content():
        if sys.platform == 'darwin':  # macOS
            command = ['pbpaste']
        elif sys.platform.startswith('linux'):  # Linux
            command = ['xclip', '-selection', 'clipboard', '-o']
        elif sys.platform == 'win32':  # Windows
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                content = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                return content
            except ImportError:
                print("pywin32 library is required for clipboard access on Windows. Install it using the command: pip install pywin32")
                return
            except Exception as e:
                print("An error occurred while accessing the clipboard on Windows:", str(e))
                return
        else:
            print("Unsupported platform.")
            return

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                print("An error occurred while retrieving the clipboard content.")
                return
            return result.stdout.strip()
        except Exception as e:
            print("An error occurred while accessing the clipboard:", str(e))
            return
