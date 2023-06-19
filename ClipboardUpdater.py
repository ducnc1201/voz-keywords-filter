import clipboard
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
        try:
            clipboard.copy(content)
            print("Content processed and clipboard updated successfully")
        except clipboard.ClipboardException as e:
            print("An error occurred while updating the clipboard:", str(e))
