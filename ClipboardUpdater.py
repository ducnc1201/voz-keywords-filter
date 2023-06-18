import re
import sys
from ClipboardManager import ClipboardManager
from KeywordManager import KeywordManager

class ClipboardUpdater:
    def __init__(self):
        self.clipboard_manager = ClipboardManager()
        self.keyword_manager = KeywordManager()

    def remove_urls_from_clipboard(self):
        content = self.clipboard_manager.get_clipboard_content()
        if content is None:
            return

        bbcode_tag_patterns = self.keyword_manager.get_bbcode_tag_patterns()
        regex_patterns = self.keyword_manager.get_regex_patterns()
        formatted_keywords = self.keyword_manager.format_keywords()

        for pattern in bbcode_tag_patterns:
            content = re.sub(pattern, '', content)

        for pattern in regex_patterns:
            content = re.sub(pattern, r'\1*\2', content)

        for keyword, formatted_keyword in zip(self.keyword_manager.keywords, formatted_keywords):
            pattern = r'\b' + re.escape(keyword) + r'\b'
            content = re.sub(pattern, formatted_keyword, content)

        self.update_clipboard_content(content)

    def update_clipboard_content(self, content):
        if sys.platform == 'win32':
            try:
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, content)
                win32clipboard.CloseClipboard()
                print("URLs and keywords removed, clipboard updated successfully")
            except Exception as e:
                print("An error occurred while updating the clipboard on Windows:", str(e))
        else:
            try:
                result = subprocess.run(['pbcopy'] if sys.platform == 'darwin' else ['xclip', '-selection', 'clipboard'],
                                        input=content, text=True)
                if result.returncode != 0:
                    print("An error occurred while updating the clipboard.")
                    return
                print("URLs and keywords removed, clipboard updated successfully")
            except Exception as e:
                print("An error occurred while updating the clipboard:", str(e))