from utils import SearchEngine
from boolParser import BoolExpCalculator

class BoolSearchEngine(SearchEngine, BoolExpCalculator):

    def __init__(self, init='load'):
        SearchEngine.__init__(self)
        if init == 'generate':
            self.generate()
        elif init == 'load':
            self.load()
        else:
            raise ValueError('The argument should be generate or load!')
        BoolExpCalculator.__init__(
            self,
            self.invertedIndexTable.table,
            self.invertedIndexTable.universe
        )
    
    def search(self, exp):
        return self.parser.parse(exp)
