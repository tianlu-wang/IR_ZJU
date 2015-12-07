__author__ = 'wenri'

from Search.Query import Query
from Search.BooleanQuery import BooleanQuery
from Search.PhraseQuery import PhraseQuery
from Index.IndexReader import IndexReader
from Analysis.SimpleAnalyzer import SimpleAnalyzer
import math
import heapq
from Index.Term import Term
from collections import defaultdict

class IndexSearcher(object):
    def __init__(self, indexReader: IndexReader, query: Query, field: str):
        self.r = indexReader
        self.query = query
        self.field = field

    def calcutescore(self, field: str) -> dict:
        """
        :rtype : object
        :param query: 
        :param field:
        :return: 
        """
        lists = list(self.query.tokenVector())
        #lists.sort()
        print('Token Vector: ', lists)
        numdoc = self.r.numDocs()
        i = 0
        freqs = defaultdict(dict)
        idf = {}
        finalTerms = []

        for value in lists:
            freq = self.r.termPosition(Term(field, value))
            if freq is not None:
                for docId in freq:
                    freqs[docId][value] = freq[docId][0]
                finalTerms.append(value)

        for value in finalTerms:
            t = Term(field, value)
            idf[value] = math.log(self.r.numDocs() / self.r.docFreq(t))

        score = defaultdict(float)

        for docId, keys in freqs.items():
            for k, v in keys.items():
                score[docId] += v * idf[k]

        return score

    def Indexsearch(self, k = -1):
        scores = {}
        s = []
        score1 = self.calcutescore("content")
        print("Score of Content finished")
        score2 = self.calcutescore("title")
        print("Score of Title finished")
        score3 = self.calcutescore("abstract")
        print("Score of Abstract finished")

        docs = set(score1.keys()).union(set(score2.keys())).union(set(score3))

        for docId in docs:
            scores[docId] = (score1.get(docId, 0) + score2.get(docId, 0) + score3.get(docId, 0) ) / 3

        self.s = scores.items()
        if k==-1:
            return sorted(self.s, key=lambda d: d[1], reverse=True)
        elif k>0:
            return heapq.nlargest(k, self.s, key=lambda d: d[1])

        return self.s

    def getIndex(self, term: str, field: str):  #
        #numDoc = self.r.numDocs()
        #i = 0
        #document = []
        #j = 0
        #for i in range(numDoc):
         #   doc = self.r.getTermVector(i, field)
          #  if term in doc.keys():
           #     document[j].append(i)
        #return document.sort()

        position = self.r.termPosition(Term(field,term))
        if position is not None:
            return sorted(position.keys())
        return []

    def Booland(self, l1: list, l2: list):
        s1 = set(l1)
        s2 = set(l2)
        s = s1.intersection(s2)
        return list(s)

    def Boolor(self, l1: list, l2: list):
        s1 = set(l1)
        s2 = set(l2)
        s = s1 | s2
        return list(s)

    def Boolnot(self, l: list):
        docnum = self.r.numDocs()
        i = 0
        s = set({})
        while i < docnum:
            s.add(i)
            i += 1
        return list(s.difference(set(l)))

    def boolSearchField(self, field: str) -> list:
        ## RPN_stack = []
        ## symbol_stack = []
        if not isinstance(self.query, BooleanQuery):
            return []
        R_stack = self.query.Input()
        print(R_stack)
        i = 0
        P_stack = []
        for i in range(len(R_stack)):
            if R_stack[i] != "AND" and R_stack[i] != "OR" and R_stack[i] != "NOT":
                P_stack.append(self.getIndex(R_stack[i], field))
            elif R_stack[i] == "AND":
                l1 = P_stack.pop()
                l2 = P_stack.pop()
                l = self.Booland(l1, l2)
                P_stack.append(l)
            elif R_stack[i] == "OR":
                l1 = P_stack.pop()
                l2 = P_stack.pop()
                l = self.Boolor(l1, l2)
                P_stack.append(l)
            elif R_stack[i] == "NOT":
                l1 = P_stack.pop()
                l = self.Boolnot(l1)
                P_stack.append(l)
        i = 0
        result = []
        while i < len(P_stack):
            l = P_stack.pop()
            j = 0
            while j < len(l):
                result.append(l[j])
                j += 1
            i += 1

        self.s = result

        return result

    def Boolsearch(self):
        score1 = self.boolSearchField("content")
        score2 = self.boolSearchField("title")
        score3 = self.boolSearchField("abstract")

        result = defaultdict(float)

        for i in score1:
            result[i] += 1
        for i in score2:
            result[i] += 1
        for i in score3:
            result[i] += 1

        self.s = result.items()

        return sorted(self.s, key=lambda d: d[1], reverse=True)


    def PosSearch(self, ppl: list, ll: list, pp1, k: int, ith: int):
        # while ppo[0] < len(po[b[0]]):
        ppi = ppl[ith]
        l = ll[ith]
        try:
            while True:
                pp2 = next(ppi)
                if(abs(pp1[0]-pp2[0]) <= k):
                    if(ith + 1 < len(ppl)):
                        for result in self.PosSearch(ppl, ll, pp2, k, ith+1):
                            l.append((pp2, ) + result)
                    else:
                        l.append((pp2, ))
                elif pp2[0] > pp1[0]:
                    break
        except StopIteration:
            pass

        while len(l):
            if(abs(l[0][0][0] - pp1[0]) <= k):
                break
            del l[0]

        return l

    def phraseFilterField(self, field: str, p_stack: list, k: int):
        r_stack = self.s
        # for i in range( len(p_stack) ):
        #     if p_stack[i] != "AND":
        #         r_stack.append(self.getIndex(p_stack[i], field))
        #     elif p_stack[i] == "AND":
        #         l1 = r_stack.pop()
        #         l2 = r_stack.pop()
        #         l = self.Booland(l1, l2)
        #         r_stack.append(l)
        # p = set(p_stack)
        # r = list(p)
        positions = []
        # i = 0
        # while len(r) > 0:
        #     key_pop = r.pop()
        #     t = Term()
        #     t.field = field
        #     t.text = key_pop
        #     position[key_pop] = self.r.termPosition(t)
        # i = 0
        # l = r_stack.pop()

        result = []
        for term in p_stack:
            print("retrial term: " + term)
            pos = self.r.termPosition(Term(field, term))
            if pos is not None:
                positions.append(pos)
            else:
                return result

        for docId, score in r_stack:
            # q = 0
            # j = 0
            # b = {}
            po = []
            ppo = []
            for v in positions:
                # b[j] = v
                # ppo[j] = 0
                if docId in v:
                    po.append(iter(v[docId][1]))
                    ppo.append([])
                else:
                    break
            else:
                ppi = po[0]
                answer = []
                try:
                    while True:
                        pp1 = next(ppi)
                        for ret in self.PosSearch(po, ppo, pp1, k, 1):
                           answer.append((pp1, ) + ret)
                except StopIteration:
                    pass

                if len(answer):
                    result.append((docId, score, answer))
        print("Field result:", result)
        return result

    def Phrasefilter(self, queries: list, k = -1):
        print("Phrase queries: ", queries)
        tokenStream = SimpleAnalyzer().tokenStream("userfield", queries)
        tokenStream.reset()
        tokenStream.incrementToken()
        ppos = tokenStream.getPosition()[0]
        kpos = 1
        while tokenStream.incrementToken():
            pos = tokenStream.getPosition()[0]
            if pos - ppos > kpos:
                kpos = pos - ppos
            ppos = pos

        finalResult = defaultdict(float)
        for query in queries:
            queryVec = PhraseQuery(query).tokenVector()
            print("Phrase ", kpos, "query: ", queryVec)
            score1 = self.phraseFilterField("content", queryVec, kpos)
            score2 = self.phraseFilterField("title", queryVec, kpos)
            score3 = self.phraseFilterField("abstract", queryVec, kpos)

            for docId, score, answer in score1:
                finalResult[docId] += score
            for docId, score, answer in score2:
                finalResult[docId] += score
            for docId, score, answer in score3:
                finalResult[docId] += score

        self.s = finalResult.items()

        if k==-1:
            return sorted(self.s, key=lambda d: d[1], reverse=True)
        elif k>0:
            return heapq.nlargest(k, self.s, key=lambda d: d[1])

        return self.s

    def Wildcardsearch(self, k = -1):
        result = self.query.getPossibleQuery(self.r.dictionary)
        finalResult = defaultdict(float)
        for queryString in result:
            self.query = Query(queryString)
            print('Query: ', queryString)
            for docId, score in self.Indexsearch(0):
                finalResult[docId] += score

        self.s = finalResult.items()

        if k==-1:
            return sorted(self.s, key=lambda d: d[1], reverse=True)
        elif k>0:
            return heapq.nlargest(k, self.s, key=lambda d: d[1])

        return self.s
