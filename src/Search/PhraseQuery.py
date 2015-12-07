__author__ = 'wenri'

from Search.Query import Query
from Analysis.StandardAnalyzer import StandardAnalyzer

class PhraseQuery(Query):
    def __init__(self, string: str):
        Query.__init__(self, string)
        self.q = StandardAnalyzer()
        self.s = string

    def tokenVector(self):
        t = self.q.tokenStream("userfield", [ self.s ])
        t.reset()
        l = []
        while t.incrementToken():
            l.append(t.getTerm().text)
        return l

    def booleanQuery(self):
        l = self.tokenVector()
        i = 0
        num = len(l)
        for i in range( num-1 ):
            l.append("AND")

        return l

