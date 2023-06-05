import re
import subprocess
import sys

def remove_urls_from_clipboard():
    # Retrieve the clipboard content based on the platform
    if sys.platform == 'darwin':  # macOS
        command = ['pbpaste']
    elif sys.platform.startswith('linux'):  # Linux
        command = ['xclip', '-selection', 'clipboard', '-o']
    elif sys.platform == 'win32':  # Windows
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            content = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)  # Use CF_UNICODETEXT for text in Unicode format
            win32clipboard.CloseClipboard()
        except ImportError:
            print("pywin32 library is required for clipboard access on Windows.")
            return
        except Exception as e:
            print("An error occurred while accessing the clipboard on Windows:", str(e))
            return
    else:
        print("Unsupported platform.")
        return

    if sys.platform != 'win32':
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                print("An error occurred while retrieving the clipboard content.")
                return
            content = result.stdout.strip()
        except Exception as e:
            print("An error occurred while accessing the clipboard:", str(e))
            return

    # Define the regex pattern
    pattern = r'\[URL=\'(.*?)\'\]|\[/URL\]'

    # Remove URLs and closing tags
    content = re.sub(pattern, '', content)

    # Update the clipboard content based on the platform
    if sys.platform == 'win32':
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, content)  # No need to encode
            win32clipboard.CloseClipboard()
            print("URLs removed and clipboard updated successfully.")
        except Exception as e:
            print("An error occurred while updating the clipboard on Windows:", str(e))
    else:
        try:
            result = subprocess.run(['pbcopy'] if sys.platform == 'darwin' else ['xclip', '-selection', 'clipboard'],
                                    input=content, text=True)
            if result.returncode != 0:
                print("An error occurred while updating the clipboard.")
                return
            print("URLs removed and clipboard updated successfully.")
        except Exception as e:
            print("An error occurred while updating the clipboard:", str(e))

remove_urls_from_clipboard()
