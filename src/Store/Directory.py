__author__ = 'wenri'

from Store.IndexInput import IndexInput
from Store.IndexOutput import IndexOutput

class Directory(object):
    def __init__(self):
        pass

    def openInput(self, name: str) -> IndexInput:
        pass

    def openOutput(self, name: str) -> IndexOutput:
        pass