__author__ = 'wenri'

from Store.Directory import Directory
from Document.Document import Document
from Analysis.SimpleAnalyzer import SimpleAnalyzer
import pickle

class Dictionary(object):
    def __init__(self, directory: Directory):
        self.d = directory
        self.dictionary = set()

    def save(self):
        wfile = self.d.openOutput('dictionary')
        pickle.dump(self.dictionary, wfile)

    def load(self):
        rfile = self.d.openInput('dictionary')
        if rfile is not None:
            self.dictionary = pickle.load(rfile)

    def addToDictionary(self, document: Document):
        for k in document.getFields():
            token = document.getField(k).tokenStream(SimpleAnalyzer())
            token.reset()
            while token.incrementToken():
                term = token.getTerm()
                self.dictionary.add(term.text)
            token.close()