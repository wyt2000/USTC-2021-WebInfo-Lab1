import json
import nltk
from nltk.stem import WordNetLemmatizer
import os
import math
from collections import Counter

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
    
    def preprocess(self):
        self.tokenize()
        self.lemmatize()
        self.deleteStopwords()

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

    def fromIndexTable(self, indexTable):
        self.table = {}
        for (id, tokens) in indexTable.items():
                self.insert(tokens, id)

    def save(self, filename):
        self.table = {
            key: list(sorted(value)) for (key, value) in self.table.items()
        }
        with open(filename, 'w') as f:
            dump = json.dumps(
                self.table,
                sort_keys = True,
                indent = 4,
                separators = (',', ': ')
            )
            f.write(dump)

    def getIDF(self):
        IDF = {
            token : math.log10(len(self.universe) / (len(self.table[token]) + 1))
            for token in self.table.keys()
        }
        return IDF

class IndexTable:

    def __init__(self):
        self.table = {}
    
    def insert(self, id, tokens):
        self.table[id] = tokens

    def save(self, filename):
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

    def getTF(self):
        TF = {
            id : {
                key: value / len(tokens)
                for (key, value) in Counter(sorted(tokens)).items()
            }
            for (id, tokens) in self.table.items()
        }
        return TF

class SearchEngine:

    def __init__(self, init='load', filename='tests/semantic-tests.json'):
        self.indexTable = IndexTable()
        self.invertedIndexTable = InvertedIndexTable()
        if init == 'generate':
            self.generate()
        elif init == 'load':
            self.load(filename)
        else:
            raise ValueError('The argument should be generate or load!')
    
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
                    p.preprocess()
                    self.indexTable.insert(p.id, p.tokens)
                    self.invertedIndexTable.insert(p.tokens, p.id)
        finally:
            self.invertedIndexTable.save('output/table.json')
    
    def load(self, filename):
        self.indexTable.load(filename)
        self.invertedIndexTable.fromIndexTable(self.indexTable.table)

if __name__ == '__main__':
    e = SearchEngine('load')
    e.invertedIndexTable.save('output/table.json')
