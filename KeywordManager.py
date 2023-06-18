class KeywordManager:
    def __init__(self):
        self.lowercase_keywords = []
        self.very_first_letter_uppercase_keywords = [keyword[0].upper() + keyword[1:] for keyword in self.lowercase_keywords]
        self.first_letter_uppercase_keywords = [keyword.title() for keyword in self.lowercase_keywords]
        self.all_uppercase_keywords = [keyword.upper() for keyword in self.lowercase_keywords]
        self.keywords = self.lowercase_keywords + self.very_first_letter_uppercase_keywords + self.first_letter_uppercase_keywords + self.all_uppercase_keywords

        self.bbcode_tag_patterns = [r'\[URL=\'(.*?)\'\]|\[/URL\]']
        self.regex_patterns = [r'(?i)(\b\w*)bca(\w*\b)']

    # get keywords from filter/keyword.txt, then append them to self.lowercase_keywords
    def get_keywords_from_file(self):
        with open('filter/keyword.txt', 'r') as file:
            for line in file:
                self.lowercase_keywords.append(line.strip())

    def format_keywords(self):
        formatted_keywords = []
        for keyword in self.keywords:
            words = keyword.split()
            formatted_words = [word[0] + '*' for word in words]
            formatted_keyword = ' '.join(formatted_words)
            formatted_keywords.append(formatted_keyword)
        return formatted_keywords

    def get_bbcode_tag_patterns(self):
        return self.bbcode_tag_patterns

    def get_regex_patterns(self):
        return self.regex_patterns