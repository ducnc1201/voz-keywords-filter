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

    # Define the regex and keywords pattern
    bbcode_tag = [r'\[URL=\'(.*?)\'\]|\[/URL\]']

    regex = [r'(?i)(\b\w*)bca(\w*\b)']

    # Define the keywords
    lowercase_keywords = ['công an', 'quân đội', 'thủ tướng']
    # make the very first letter of the keyword uppercase
    very_first_letter_uppercase_keywords = [keyword[0].upper() + keyword[1:] for keyword in lowercase_keywords]
    # make the first letter of the keyword uppercase
    first_letter_uppercase_keywords = [keyword.title() for keyword in lowercase_keywords]
    # make the keyword all uppercase
    all_uppercase_keywords = [keyword.upper() for keyword in lowercase_keywords]
    #append the keywords together
    keywords = lowercase_keywords + very_first_letter_uppercase_keywords + first_letter_uppercase_keywords + all_uppercase_keywords

    # Remove some BBcode tags, and format keywords
    # URL tags removal
    for pattern in bbcode_tag:
        content = re.sub(pattern, '', content)

    # Remove the regex
    for r in regex:
        content = re.sub(r, r'\1*\2', content)

    for keyword in keywords:
        words = keyword.split()  # Split the keyword into individual words
        formatted_words = []
        for word in words:
            formatted_word = word[0]+ '*'
            formatted_words.append(formatted_word)
        formatted_keyword = ' '.join(formatted_words)

        pattern = r'\b' + re.escape(keyword) + r'\b'
        content = re.sub(pattern, formatted_keyword, content)

    # Update the clipboard content based on the platform
    if sys.platform == 'win32':
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, content)  # No need to encode
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

remove_urls_from_clipboard()