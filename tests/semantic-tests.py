import sys

sys.path.append('src')

from semantic_search import SemanticSearchEngine

s = SemanticSearchEngine()

def test_1():
    assert s.search('home xxx home shopping', k=3) == [('2', 0.3902428471380446), ('4', 0.35446777811575614), (
        '1', 0.18647444280780595)]
