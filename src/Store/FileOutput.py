__author__ = 'WenriJ'

from Store.IndexOutput import IndexOutput
import io

class FileOutput(IndexOutput):
    def __init__(self, filename: str):
        IndexOutput.__init__(self)
        self.file = open(filename, 'wb')

    def write(self, data):
        return self.file.write(data)

    def seek(self, pos: int, whence = io.SEEK_SET):
        return self.file.seek(pos, whence)

    def tell(self) -> int:
        return self.file.tell()

