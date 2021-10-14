from utils import SearchEngine, Preprocessor
from collections import Counter

class SemanticSearchEngine(SearchEngine):
    
    def __init__(self, init='load'):
        SearchEngine.__init__(self, init)
        self.TF = self.indexTable.getTF()
        self.IDF = self.invertedIndexTable.getIDF()
        self.TFIDF = {
            id : {
                token : tf * self.IDF[token]
                for (token, tf) in TF.items()
            }
            for (id, TF) in self.TF.items()
        }

    def search(self, words):
        p = Preprocessor()
        p.text = words
        p.preprocess()
        tokens = sorted(p.tokens)
        TF = {
            key : value / len(tokens)
            for (key, value) in Counter(tokens).items()
        }
        print(TF)

if __name__ == '__main__':
    e = SemanticSearchEngine()
    e.search(
        'We merging markets are set for an even bigger rally in 2018, says one technician')
