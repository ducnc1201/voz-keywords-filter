import re
import subprocess

def remove_urls_from_clipboard():
    # Get the clipboard text using subprocess
    if subprocess.run(['which', 'pbpaste'], capture_output=True, text=True).stdout.strip():
        # macOS
        clipboard_command = 'pbpaste'
        update_command = 'pbcopy'
    elif subprocess.run(['which', 'xclip'], capture_output=True, text=True).stdout.strip():
        # Linux
        clipboard_command = 'xclip -selection clipboard -o'
        update_command = 'xclip -selection clipboard'
    elif subprocess.run(['which', 'powershell.exe'], capture_output=True, text=True).stdout.strip():
        # Windows
        clipboard_command = 'powershell.exe -command "Get-Clipboard"'
        update_command = 'powershell.exe -command "Set-Clipboard"'

    try:
        # Retrieve the clipboard text
        process = subprocess.Popen(clipboard_command, stdout=subprocess.PIPE, shell=True)
        content, _ = process.communicate()
        content = content.decode().strip()

        # Define the regex pattern
        pattern = r'\[URL=\'(.*?)\'\]|\[/URL\]'

        # Remove URLs and closing tags
        content = re.sub(pattern, '', content)

        # Update the clipboard with the modified content
        process = subprocess.Popen(update_command, stdin=subprocess.PIPE, shell=True)
        process.communicate(input=content.encode())
        process.wait()

        print("URLs removed and clipboard updated successfully.")
    except Exception as e:
        print("An error occurred:", str(e))

remove_urls_from_clipboard()
