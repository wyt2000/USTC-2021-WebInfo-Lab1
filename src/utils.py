import json
import nltk
from nltk.stem import WordNetLemmatizer
import os

class Preprocessor:
    '''
    >>> import nltk
    >>> nltk.download('punkt')
    >>> nltk.download('wordnet')
    >>> nltk.download('averaged_perceptron_tagger')
    >>> nltk.download('stopwords')
    '''
    def __init__(self):
        self.text = ''
        self.tokens = []
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords += ['!', ',', '.', '?', '|',
                           '\'\'', '\'', '``', '`', '\'s', 'n\'t',
                           '*', '+', '-', '/', '--', '#', '$'
                           ]

    def load(self, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            self.text = json.load(f)['text']
            self.id = filename
    
    def tokenize(self):
        self.tokens = nltk.word_tokenize(self.text)

    def getTags(self, tag):
        if tag.startswith('J'):
            return 'a'
        elif tag.startswith('V'):
            return 'v'
        elif tag.startswith('N'):
            return 'n'
        elif tag.startswith('R'):
            return 'r'
        else:
            return 's'

    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        self.tokens = [
            lemmatizer.lemmatize(token, self.getTags(tag))
            for token, tag in nltk.pos_tag(self.tokens)
        ]

    def deleteStopwords(self):
        self.tokens = [
            token
            for token in self.tokens if token.lower() not in self.stopwords
        ]

class InvertedIndexTable:
    
    def __init__(self):
        self.table = {}
        self.universe = set()
    
    def insert(self, tokens, id):
        for token in tokens:
            if self.table.__contains__(token):
                self.table[token].add(id)
            else:
                self.table[token] = {id}

    def save(self, filename):
        self.table = {
            key : list(sorted(value)) for (key, value) in self.table.items()
        }
        with open(filename, 'w') as f:
            dump = json.dumps(
                self.table,
                sort_keys = True,
                indent = 4,
                separators = (',', ': ')
            )
            f.write(dump)
    
    def load(self, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            self.table = json.load(f)
            for value in self.table.values():
                for item in value:
                    self.universe.add(item)
            
class SearchEngine:

    def __init__(self):
        self.t = InvertedIndexTable()
    
    def generate(self):
        p = Preprocessor()
        self.t.table = {
            key: set(value) for (key, value) in self.t.table.items()
        }
        os.chdir('../dataset')
        datelist = os.listdir('.')
        try:
            for date in datelist:
                filelist = os.listdir(date)
                for file in filelist:
                    fullpath = f'{date}/{file}'
                    print(fullpath)
                    self.t.universe.add(fullpath)
                    p.load(fullpath)
                    p.tokenize()
                    p.lemmatize()
                    p.deleteStopwords()
                    self.t.insert(p.tokens, p.id)
        finally:
            self.t.save('../output/table.json')
    
    def load(self):
        self.t.load('../output/test.json')

if __name__ == '__main__':
    e = SearchEngine()
    e.load()
    e.generate()
