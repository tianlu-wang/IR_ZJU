__author__ = 'WenriJ'

from Store.Directory import Directory
from Store.FileInput import FileInput
from Store.FileOutput import FileOutput
import os

class FileSystemDirectory(Directory):
    def __init__(self, dir: str):
        Directory.__init__(self)
        self.dir = dir

    def openInput(self, name: str) -> FileInput:
        fileName = os.path.join(self.dir, name)
        if os.path.exists(fileName):
            return FileInput(fileName)
        else:
            return None

    def openOutput(self, name: str) -> FileOutput:
        return FileOutput(os.path.join(self.dir, name))
