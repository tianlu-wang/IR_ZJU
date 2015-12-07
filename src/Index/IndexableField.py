__author__ = 'wenri'

from Analysis.TokenStream import TokenStream
from Analysis.Analyzer import Analyzer

class IndexableField(object):
    def __init__(self, name: str):
        self.fieldName = name

    def name(self) -> str:
        return self.fieldName

    def tokenStream(self, analyzer: Analyzer) -> TokenStream:
        pass


