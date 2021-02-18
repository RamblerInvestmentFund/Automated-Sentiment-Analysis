
import re
from bs4 import BeautifulSoup


class FrontPage:

    def __findWordPairsInHeadlines(self):
        
        self.pairs = dict()
        for hl in self.headlines:
            words = hl.split()

            # Get rid of all non-alphanumeric characters in headlines and 's' at end of words
            for k in range(len(words)-1):
                words[k] = re.sub(r'\W+', '', words[k])
                words[k+1] = re.sub(r'\W+', '', words[k+1])
                words[k] = re.sub(r's+$', '', words[k].lower());
                words[k+1] = re.sub(r's+$', '', words[k+1].lower());
                self.pairs[(words[k], words[k+1])] = 1



    def __init__(self, path, timestamp):
        self.path = path
        self.timestamp = timestamp

        with open(path, "r") as infile:
            html = infile.read()

        self.headlines = []

        page = BeautifulSoup(html, "html.parser")

        for tag in page.body.find_all('h3'):
            while ( hasattr (tag, 'contents') ):
                tag = tag.contents[0]
            self.headlines.append(tag)

        for tag in page.body.find_all('h4'):
            try:
                while ( hasattr (tag, 'contents') ):
                    tag = tag.contents[0]
                self.headlines.append(tag)
            except:
                continue

        self.__findWordPairsInHeadlines()

        return





