__author__ = 'wenri'

from Analysis.Analyzer import Analyzer

class IndexWriterConfig:
    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer
