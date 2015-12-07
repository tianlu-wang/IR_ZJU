__author__ = 'wenri'

from Search.Query import Query
from Analysis.BooleanAnalyzer import BooleanAnalyzer


class BooleanQuery(Query):

    symbol_priority = {0: ['('], 1: ["NOT"], 2: ["AND"], 3: ["OR"], 4: [')']}
    symbols = set()
    for i in symbol_priority.values():
        for j in i:
            symbols.add(j)

    def __init__(self, string: str):
        Query.__init__(self, string)
        self.s = string
        self.q = BooleanAnalyzer()

    def comparePriority(self, symbol, RPN_stack, symbol_stack):
        if len(symbol_stack) > 0:
            symbol_pop = symbol_stack.pop()
        else:
            return
        if symbol_pop == '(':
            symbol_stack.append(symbol_pop)
            symbol_stack.append(symbol)
            return
        for lists in BooleanQuery.symbol_priority.values():
            if(symbol in lists) and (symbol_pop in lists):
                symbol_stack.append(symbol_pop)
                symbol_stack.append(symbol)
                return
            elif symbol_pop in lists:
                RPN_stack.append(symbol_pop)
                self.comparePriority(symbol, RPN_stack, symbol_stack)
                symbol_stack.append(symbol)
                return
            elif symbol in lists:
                symbol_stack.append(symbol_pop)
                symbol_stack.append(symbol)
                return
            else:
                continue

    def scanf(self, input_str, RPN_stack, symbol_stack):
        for token in input_str:
            ch = token.upper()
            if not ch in BooleanQuery.symbols:
                RPN_stack.append(token)
            else:
                if len(symbol_stack) > 0:
                    if ch == '(':
                        symbol_stack.append(ch)
                    elif ch == ')':
                        while True:
                            symbol_pop = symbol_stack.pop()
                            if symbol_pop == '(':
                                break
                            else:
                                RPN_stack.append(symbol_pop)
                    else:
                        self.comparePriority(ch, RPN_stack, symbol_stack)
                else:
                    symbol_stack.append(ch)
        i = 0
        while i < len(symbol_stack):
            RPN_stack.append(symbol_stack.pop())
            i += 1
        return RPN_stack

    def Input(self):
        t = self.q.tokenStream("userfield", [self.s])
        t.reset()
        s = []
        RPN_stack = []
        symbol_stack = []
        while t.incrementToken():
            s.append(t.getTerm().text)
        return self.scanf(s, RPN_stack, symbol_stack)
