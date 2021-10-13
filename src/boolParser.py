import ply.lex as lex
import ply.yacc as yacc

class BoolExpCalculator:

    def __init__(self, table, universe):
        self.table = {
            key : sorted(value)
            for (key, value) in table.items()
        }
        self.universe = sorted(list(universe))
        self.generateParser()

    def OR(self, item1, item2):
        ret = []
        i, j = 0, 0
        m, n = len(item1), len(item2)
        while i < m and j < n:
            if item1[i] < item2[j]:
                ret.append(item1[i])
                i += 1
            elif item1[i] > item2[j]:
                ret.append(item2[j])
                j += 1
            else:
                ret.append(item1[i])
                i += 1
                j += 1
        while i < m:
            ret.append(item1[i])
            i += 1
        while j < n:
            ret.append(item2[j])
            j += 1
        return ret

    def AND(self, item1, item2):
        ret = []
        i, j = 0, 0
        m, n = len(item1), len(item2)
        while i < m and j < n:
            if item1[i] < item2[j]:
                i += 1
            elif item1[i] > item2[j]:
                j += 1
            else:
                ret.append(item1[i])
                i += 1
                j += 1
        return ret

    def NOT(self, item):
        ret = []
        universe = self.universe
        i, j = 0, 0
        m, n = len(item), len(universe)
        while i < m and j < n:
            if item[i] < universe[j]:
                i += 1
            elif item[i] > universe[j]:
                ret.append(universe[j])
                j += 1
            else:
                i += 1
                j += 1
        while j < n:
            ret.append(universe[j])
            j += 1
        return ret

    def generateParser(self):
        tokens = (
            'AND',
            'OR',
            'NOT',
            'LPAREN',
            'RPAREN',
            'WORDS'
        )

        t_LPAREN    = r'\('
        t_RPAREN    = r'\)'
        t_ignore    = ' \t'

        def t_WORDS(t):
            r'([_0-9A-Za-z])+'
            if t.value in ('AND', 'OR', 'NOT'):
                t.type = t.value
            elif self.table.__contains__(t.value):
                t.value = self.table[t.value]
            else:
                t.value = []
            return t

        def t_error(t):
            print(f"Illegal character {t.value[0]}")
            t.lexer.skip(1)

        precedence = (
            ('left', 'OR'),
            ('left', 'AND'),
            ('right', 'NOT')
        )

        def p_exp_or(p):
            'exp : exp OR exp'
            p[0] = self.OR(p[1], p[3])

        def p_exp_and(p):
            'exp : exp AND exp'
            p[0] = self.AND(p[1], p[3])

        def p_exp_not(p):
            'exp : NOT exp'
            p[0] = self.NOT(p[2])

        def p_exp_factor(p):
            'exp : LPAREN exp RPAREN'
            p[0] = p[2]

        def p_exp_words(p):
            'exp : WORDS'
            p[0] = p[1]

        def p_error(p):
            print(f"Syntax error at {p} !")

        lexer = lex.lex()
        self.parser = yacc.yacc()
