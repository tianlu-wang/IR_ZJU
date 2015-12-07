__author__ = 'Wenri'

from Store.Directory import Directory
from Index.Term import Term
from Codecs.TermVectorsReader import TermVectorsReader
import pickle

class DummyTermVectorsReader(TermVectorsReader):
    def __init__(self, directory: Directory):
        TermVectorsReader.__init__(self, directory)
        self.documents = pickle.load(self.d.openInput('dummy'))
        self.docIter = iter(self.documents)

    def getDocument(self)->int:  # return numVectorFields
        try:
            self.currentDoc = next(self.docIter)
            self.fieldIter = iter(self.currentDoc[1])
            return self.currentDoc[0]
        except StopIteration:
            return 0

    def getField(self)->(str, int):  # return (field, numTerms)
        self.currentField = next(self.fieldIter)
        self.termIter = iter(self.currentField[2])
        return self.currentField[0], self.currentField[1]

    def getTerm(self)->(int, Term):  # return a tuple: frequency and the term
        self.currentTerm = next(self.termIter)
        self.posIter = iter(self.currentTerm[2])
        return self.currentTerm[1], self.currentTerm[0]

    def getPosition(self)->tuple:  # position and startOffset and endOffset are put in a tuple
        return next(self.posIter)

    def finishTerm(self):
        pass

    def finishField(self):
        pass

    def finishDocument(self):
        pass

