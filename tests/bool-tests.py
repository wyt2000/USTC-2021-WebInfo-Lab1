import sys

sys.path.append('../src')

from bool_search import BoolSearchEngine

b = BoolSearchEngine()

def test_1():
    assert b.search('a') == ['1', '2', '3']

def test_2():    
    assert b.search('b') == ['2', '3', '4']

def test_3():
    assert b.search('c') == ['3', '4', '5']

def test_4():
    assert b.search('d') == []

def test_5():
    assert b.search('a AND b') == ['2', '3']

def test_6():
    assert b.search('b OR c') == ['2', '3', '4', '5']

def test_7():
    assert b.search('NOT c') == ['1', '2']

def test_8():
    assert b.search('NOT d') == ['1', '2', '3', '4', '5']

def test_9():
    assert b.search('a AND b AND c') == ['3']
    
def test_10():
    assert b.search('a OR b AND c') == ['1', '2', '3', '4']

def test_11():
    assert b.search('NOT a OR b AND c') == ['3', '4', '5']

def test_12():
    assert b.search('NOT NOT NOT a') == ['4', '5']

def test_13():
    assert b.search('a OR b AND b OR c') == ['1', '2', '3', '4', '5']

def test_14():
    assert b.search('(a OR b) AND (b OR c)') == ['2', '3', '4']

def test_15():
    assert b.search('NOT(a AND b)') == ['1', '4', '5']

def test_16():
    assert b.search('((a) AND ((b OR NOT c)) AND (a OR b))') == ['1', '2', '3']
