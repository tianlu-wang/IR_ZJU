__author__ = 'wenri'

from Store.Directory import Directory
from Index.Term import Term

class TermVectorsReader(object):
    def __init__(self, directory: Directory):
        self.d = directory

    def getDocument(self)->int:  # return numVectorFields
        pass

    def getField(self)->(str, int):  # return (field, numTerms)
        pass

    def getTerm(self)->(int, Term):  # return a tuple: frequency and the term
        pass

    def getPosition(self)->tuple:  # position and startOffset and endOffset are put in a tuple
        pass

    def finishTerm(self):
        pass

    def finishField(self):
        pass

    def finishDocument(self):
        pass

