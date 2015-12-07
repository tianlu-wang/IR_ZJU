__author__ = 'wenri'

from Analysis.Analyzer import Analyzer
from Analysis.TokenStream import TokenStream
from Analysis.WhitespaceTokenizer import WhitespaceTokenizer
from Analysis.PunctuationFilters import PunctuationFilters
from Analysis.StemFilter import StemFilter

class StandardAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)

    def tokenStream(self, fieldName: str, reader) -> TokenStream:
        #return PunctuationFilters(WhitespaceTokenizer(fieldName, reader))
        return StemFilter(PunctuationFilters(WhitespaceTokenizer(fieldName, reader)))
