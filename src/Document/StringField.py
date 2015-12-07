__author__ = 'wenri'

from Index.IndexableField import IndexableField
from Analysis.Analyzer import Analyzer

class StringField(IndexableField):
    def __init__(self, name: str, text: str):
        IndexableField.__init__(self, name)
        self.text = text

    def tokenStream(self, analyzer: Analyzer):
        return analyzer.tokenStream(self.name(), [self.text])
