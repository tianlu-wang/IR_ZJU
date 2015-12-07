__author__ = 'Wenri'

from Utilities.Dictionary import Dictionary
import heapq

class SpellCheck(object):
    def __init__(self, directory: Dictionary):
        self.directory = directory

    # Christopher P. Matthews
    # christophermatthews1985@gmail.com
    # Sacramento, CA, USA
    def levenshtein(self, s, t):
        # ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(t)]

    def SpellAdvise(self, s: str, k: int) -> list:
        editDist = {}
        for t in self.directory.dictionary:
            editDist[t] = self.levenshtein(s, t)
        return heapq.nsmallest(k, editDist.items(), key=lambda d: d[1])

    def CheckSpell(self, s: str) -> list:
        words = s.split()
        result = []
        for word in words:
            if word not in self.directory.dictionary:
                result += self.SpellAdvise(word, 5)
        return result