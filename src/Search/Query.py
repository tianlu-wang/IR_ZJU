__author__ = 'wenri'

from Analysis.StandardAnalyzer import StandardAnalyzer


class Query(object):
    def __init__(self, string: str):
        self.q = StandardAnalyzer()
        self.s = string

    def tokenVector(self):
        t = self.q.tokenStream("userfield", [ self.s ])
        t.reset()
        s = []
        l = {}
        while t.incrementToken():
            s.append(t.getTerm().text)
        l = set(s)
        return l



