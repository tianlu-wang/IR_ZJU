__author__ = 'wenri'

from Store.Directory import Directory
from Index.Term import Term

class TermVectorsWriter(object):
    def __init__(self, directory: Directory):
        self.d = directory

    def addPosition(self, position: int, startOffset: int, endOffset: int):
        pass

    def finishDocument(self):
        pass

    def finishField(self):
        pass

    def finishTerm(self):
        pass

    def startDocument(self, numVectorFields: int):
        pass

    def startField(self, fieldInfo, numTerms: int):
        pass

    def startTerm(self, term: Term, freq: int):
        pass
