import sys
from ClipboardManager import ClipboardManager
from ContentProcessor import ContentProcessor

class ClipboardUpdater:
    def __init__(self):
        self.clipboard_manager = ClipboardManager()
        self.content_processor = ContentProcessor()

    def remove_content_from_clipboard(self):
        content = self.clipboard_manager.get_clipboard_content()
        if content is None:
            return

        processed_content = self.content_processor.process_content(content)
        self.update_clipboard_content(processed_content)

    def update_clipboard_content(self, content):
        if sys.platform == 'win32':
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, content)
                win32clipboard.CloseClipboard()
                print("Content processed and clipboard updated successfully")
            except Exception as e:
                print("An error occurred while updating the clipboard on Windows:", str(e))
        else:
            try:
                result = subprocess.run(['pbcopy'] if sys.platform == 'darwin' else ['xclip', '-selection', 'clipboard'],
                                        input=content, text=True)
                if result.returncode != 0:
                    print("An error occurred while updating the clipboard.")
                    return
                print("Content processed and clipboard updated successfully")
            except Exception as e:
                print("An error occurred while updating the clipboard:", str(e))
