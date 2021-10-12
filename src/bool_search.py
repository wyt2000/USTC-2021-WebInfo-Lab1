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
        BoolExpCalculator.__init__(self, self.t.table, self.t.universe)
    
    def search(self, exp):
        return self.parser.parse(exp)

if __name__ == '__main__':
    b = BoolSearchEngine()
    print(b.search('a'))    #123
    print(b.search('b'))    #234
    print(b.search('c'))    #345
    print(b.search('d'))
    print(b.search('a AND b'))
    print(b.search('b OR c'))
    print(b.search('NOT c'))
    print(b.search('NOT d'))
    print(b.search('a AND b AND c'))
    print(b.search('a OR b AND c'))
    print(b.search('a AND NOT b'))
    print(b.search('NOT a OR b AND c'))
    print(b.search('NOT NOT NOT a'))
    print(b.search('a OR b AND b OR c'))
    print(b.search('(a OR b) AND (b OR c)'))
    print(b.search('NOT(a AND b)'))
    print(b.search('((a) AND ((b OR NOT c)) AND (a OR b))'))