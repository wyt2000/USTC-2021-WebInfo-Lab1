from utils import SearchEngine, Preprocessor
from collections import Counter
import math
import heapq
import json

class SemanticSearchEngine(SearchEngine):
    
    def __init__(self, init='load', filename='tests/semantic-tests.json'):
        SearchEngine.__init__(self, init, filename)
        self.TF = self.indexTable.getTF()
        self.IDF = self.invertedIndexTable.getIDF()
        self.TFIDF = {
            id : {
                token : tf * self.IDF[token]
                for (token, tf) in TF.items()
            }
            for (id, TF) in self.TF.items()
        }

    def save(self, filename):
        with open(filename, 'w') as f:
            dump = json.dumps(
                self.TFIDF,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
            f.write(dump)

    def norm(self, vec):
        return math.sqrt(
            sum(
                value ** 2
                for value in vec.values()
            )
        )

    def dict2list(self, vec):
        return [
            (key, value)
            for (key, value) in vec.items()
        ]

    def getSimilarity(self, vec1, vec2):
        norm1 = self.norm(vec1)
        norm2 = self.norm(vec2)
        vec1 = self.dict2list(vec1)
        vec2 = self.dict2list(vec2)
        ret = 0
        i, j = 0, 0
        m, n = len(vec1), len(vec2)
        while i < m and j < n:
            if vec1[i][0] < vec2[j][0]:
                i += 1
            elif vec1[i][0] > vec2[j][0]:
                j += 1
            else:
                ret += vec1[i][1] * vec2[j][1]
                i += 1
                j += 1
        ret /= norm1
        ret /= norm2
        return ret

    def search(self, words, k=10):
        p = Preprocessor()
        p.text = words
        p.preprocess()
        tokens = sorted(p.tokens)
        TF = {
            key : value / len(tokens)
            for (key, value) in Counter(tokens).items()
        }
        searchVec = {
            token : tf * self.IDF[token] if self.IDF.__contains__(token) 
            else tf * math.log10(len(self.invertedIndexTable.universe))
            for (token, tf) in TF.items()
        }
        similarities = {
            id : self.getSimilarity(searchVec, vec)
            for (id, vec) in self.TFIDF.items()
        }
        return heapq.nlargest(
            k, 
            self.dict2list(similarities),
            key=lambda a: (a[1], a[0])
        )
    
if __name__ == '__main__':
    e = SemanticSearchEngine()
    e.save('output/tfidf.json')