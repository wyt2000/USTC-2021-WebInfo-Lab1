import json
import nltk
from nltk.stem import WordNetLemmatizer
import os
import math

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
        self.universe.add(id)
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

    def getIDF(self):
        IDF = {
            token : math.log(len(self.universe) / (len(self.table[token]) + 1))
            for token in self.table.keys()
        }
        return IDF

class IndexTable:

    def __init__(self):
        self.table = {}
    
    def insert(self, id, tokens):
        counter = {}
        for token in tokens:
            if counter.__contains__(token):
                counter[token] += 1
            else:
                counter[token] = 1
        self.table[id] = counter

    def getTF(self):
        TF = {
            id : {
                key : (value / sum(tokens))
                for (key, value) in tokens
            } for (id, tokens) in self.table.items()
        }
        return TF

class SearchEngine:

    def __init__(self):
        self.invertedIndexTable = InvertedIndexTable()
    
    def generate(self):
        p = Preprocessor()
        self.invertedIndexTable.table = {
            key: set(value) for (key, value) in self.invertedIndexTable.table.items()
        }
        os.chdir('../dataset')
        datelist = os.listdir('.')
        try:
            for date in datelist:
                filelist = os.listdir(date)
                for file in filelist:
                    fullpath = f'{date}/{file}'
                    print(fullpath)
                    p.load(fullpath)
                    p.tokenize()
                    p.lemmatize()
                    p.deleteStopwords()
                    self.invertedIndexTable.insert(p.tokens, p.id)
        finally:
            self.invertedIndexTable.save('../output/table.json')
    
    def load(self):
        self.invertedIndexTable.load('tests/test.json')

if __name__ == '__main__':
    e = SearchEngine()
    e.load()
    e.generate()
