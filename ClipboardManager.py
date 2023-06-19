import clipboard

class ClipboardManager:
    @staticmethod
    def get_clipboard_content():
        try:
            return clipboard.paste()
        except clipboard.ClipboardException as e:
            print("An error occurred while accessing the clipboard:", str(e))
            return
        # Check if user haven't installed clipboard package
        except ModuleNotFoundError as e:
            print("An error occurred while accessing the clipboard:", str(e))
            print("To use clipboard functionality, please install the 'clipboard' package.")
            print("You can install it by running 'pip install clipboard' in your command prompt.")
