__author__ = 'wenri'

from Index.IndexableField import IndexableField
from Analysis.Analyzer import Analyzer

class TextField(IndexableField):
    def __init__(self, name, contents):
        IndexableField.__init__(self, name)
        self.contents = contents

    def tokenStream(self, analyzer: Analyzer):
        return analyzer.tokenStream(self.name(), self.contents)