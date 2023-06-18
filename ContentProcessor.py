import re
from KeywordManager import KeywordManager

class ContentProcessor:
    def __init__(self):
        self.keyword_manager = KeywordManager()

    def process_content(self, content):
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

        return content