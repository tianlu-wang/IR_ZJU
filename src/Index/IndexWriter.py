__author__ = 'wenri'

from Store.Directory import Directory
from Document.Document import Document
from Index.IndexReader import IndexReader
from Index.IndexWriterConfig import IndexWriterConfig
from Codecs.DummyTermVectorsWriter import DummyTermVectorsWriter
from collections import defaultdict
from Utilities.Dictionary import Dictionary

class IndexWriter(object):
    def __init__(self, directory: Directory, config: IndexWriterConfig):
        self.d = directory
        self.codecs = DummyTermVectorsWriter(self.d)
        self.config = config
        self.numOfDocs = 0
        self.dictionary = Dictionary(self.d)

    def addDocument(self, document: Document):
        fields = document.getFields()
        numVectorFields = len(fields.keys())
        self.codecs.startDocument(numVectorFields)
        for fieldInfo in fields:
            tokenStream = document.getField(fieldInfo).tokenStream(self.config.analyzer)  # not assure if tokenStream will choose the right function automatically
            tokenStream.reset()
            termDict = defaultdict(list)
            while tokenStream.incrementToken():
                term = tokenStream.getTerm()
                position = tokenStream.getPosition()
                termDict[term].append(position)
            self.codecs.startField(fieldInfo,len(termDict))
            for term in termDict.keys():
                positions = termDict.get(term)
                self.codecs.startTerm(term,len(positions))
                for position, startOffset, endOffset in positions:
                    self.codecs.addPosition(position, startOffset, endOffset)
                self.codecs.finishTerm()
            self.codecs.finishField()
        self.codecs.finishDocument()
        self.numOfDocs += 1  # interesting about Python
        self.dictionary.addToDictionary(document)

    def addIndexes(self, readers: IndexReader):
        pass

    def numDocs(self):
        return self.numOfDocs

    def close(self):
        self.dictionary.save()