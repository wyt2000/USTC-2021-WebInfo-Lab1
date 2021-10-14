from utils import SearchEngine
from boolParser import BoolExpCalculator

class BoolSearchEngine(SearchEngine, BoolExpCalculator):

    def __init__(self, init='load'):
        SearchEngine.__init__(self, init)
        BoolExpCalculator.__init__(
            self,
            self.invertedIndexTable.table,
            self.invertedIndexTable.universe
        )
    
    def search(self, exp):
        return self.parser.parse(exp)

if __name__ == '__main__':
    b = BoolSearchEngine()
