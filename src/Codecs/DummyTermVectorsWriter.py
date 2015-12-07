__author__ = 'Wenri'

from Codecs.TermVectorsWriter import TermVectorsWriter
from Store.Directory import Directory
from Index.Term import Term
import pickle

class DummyTermVectorsWriter(TermVectorsWriter):
    def __init__(self, directory: Directory):
        TermVectorsWriter.__init__(self, directory)
        self.documents = []

    def __del__(self):
        pickle.dump(self.documents, self.d.openOutput('dummy'))

    def addPosition(self, position: int, startOffset: int, endOffset: int):
        self.currentTerm[2].append((position, startOffset, endOffset))

    def finishDocument(self):
        self.documents.append(self.currentDoc)

    def finishField(self):
        self.currentDoc[1].append(self.currentField)

    def finishTerm(self):
        self.currentField[2].append(self.currentTerm)

    def startDocument(self, numVectorFields: int):
        self.currentDoc = (numVectorFields, [])

    def startField(self, fieldInfo, numTerms: int):
        self.currentField = (fieldInfo, numTerms, [])

    def startTerm(self, term: Term, freq: int):
        self.currentTerm = (term, freq, [])
