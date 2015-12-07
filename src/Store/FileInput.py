__author__ = 'WenriJ'

from Store.IndexInput import IndexInput
import io

class FileInput(IndexInput):
    def __init__(self, filename: str):
        IndexInput.__init__(self)
        self.file = open(filename, 'rb')

    def read(self, len: int):
        return self.file.read(len)

    def readline(self):
        return self.file.readline()

    def seek(self, pos: int, whence = io.SEEK_SET):
        return self.file.seek(pos, whence)

    def tell(self) -> int:
        return self.file.tell()
