from utils import SearchEngine, Preprocessor
import numpy as np

np.random.seed(114514)

class Word2vecSearchEngine(SearchEngine):

    def __init__(self, init='load', filename='tests/semantic-tests.json'):
        SearchEngine.__init__(self, init, filename)
        self.words = self.invertedIndexTable.table.keys()
        self.context = self.indexTable.table

    def initVectors(self, vecLength, k):
        self.vectors = {
            word: np.random.rand(vecLength, 1)
            for word in self.words
        }
        self.thetas = {
            word: np.random.rand(vecLength, 1)
            for word in self.words
        }
        for i in range(2 * k):
            self.vectors[f'__aux{i}'] = np.random.rand(vecLength, 1)
            self.thetas[f'__aux{i}'] = np.random.rand(vecLength, 1)
        self.context = {
            id : (tokens + [f'__aux{i}' for i in range(2 * k)])
            for (id, tokens) in self.context.items()
        }
        self.vecLength = vecLength
        self.k = k

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def negativeSample(self, u, size=5):
        ret = set()
        while len(ret) < size:
            choice = np.random.choice(
                [
                    word
                    for words in self.context.values()
                    for word in words 
                ]
            )
            if choice != u:
                ret.add(choice)
        return ret

    def update(self, id, i, lr):
        k = self.k
        context = self.context[id][i - k - 1 : i + k]
        w = self.context[id][i]
        x = np.sum(
            [
                self.vectors[word] for word in context 
            ]
        ) - self.vectors[w]
        
        # update x args
        e = 0
        q = self.sigmoid(x.T @ self.thetas[w])
        g = lr * (1 - q)
        e = e + g * self.thetas[w]
        self.thetas[w] += g * x

        # update NEG(x) args
        for u in self.negativeSample(w):
            q = self.sigmoid(x.T @ self.thetas[u])
            g = - lr * q
            e = e + g * self.thetas[u]
            self.thetas[u] += g * x

        # update vectors
        for word in context:
            self.vectors[word] += e
        self.vectors[w] -= e

    def train(self, epoch, lr):
        for i in range(epoch):
            for id in self.context.keys():
                for i in range(len(self.context[id])):
                    self.update(id, i, lr)
        print(self.vectors)

if __name__ == '__main__':
    e = Word2vecSearchEngine()
    e.initVectors(vecLength=5, k=2)
    e.train(10, 0.1)
