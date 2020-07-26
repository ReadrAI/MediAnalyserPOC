from html.parser import HTMLParser

"""
Extracts the text from New York Times raw html text

usage:
nytParser = NYTParser()
nytParser.feed(raw_nyt_html_article)
text = nytParser.getText()

to reuse, create a new parser or call 'reset()'
"""


class NYTParser(HTMLParser):

    forbiddenTags = ['script', 'style', 'span', 'iframe', 'h2']

    def __init__(self):
        self.reset()

    def reset(self):
        self.output = ""
        self.print = True
        self.tag = ""
        self.attrs = None

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag in self.forbiddenTags:
            self.print = False
        else:
            if tag == 'div':
                self.output += "\n"
            self.tag = tag
            self.attrs = attrs

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        if tag in self.forbiddenTags:
            self.print = True

    def handle_data(self, data):
        if self.print:
            if (
                len(self.attrs) == 1 and (
                    self.attrs[0][0] == 'class' or self.attrs[0][0] == 'data-rh'
                )
            ) or (
                len(self.attrs) >= 3 and self.attrs[1][0] == 'href' and self.attrs[1][1].startswith(
                    "https://")
            ):
                self.output = self.output + data + \
                    ("\n" if data.endswith("\n") else "")
                self.attrs = None
                # print(self.tag, self.attrs, data)
            else:
                # print(self.tag, data)
                pass

    def getText(self):
        text = self.output
        x = len(text)
        while True:
            text = text.replace("\t", "").replace("  ", " ").replace("\n\n", "")\
                .replace("\n ", "\n").replace(" \n", "\n")
            if len(text) == x:
                return text.strip()
            else:
                x = len(text)

    def checkOutput(text, formatted_html):
        missing_piece = ""
        for sub in text.split("\n\n"):
            i = formatted_html.find(sub)
            if i < 0 or i >= len(formatted_html):
                for subsub in sub.split("\n"):
                    j = formatted_html.find(subsub)
                    if j < 0 or j >= len(formatted_html):
                        missing_piece += sub + "\n######################################"
        return missing_piece
