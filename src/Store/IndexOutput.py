__author__ = 'WenriJ'

import io

class IndexOutput(object):
    def __init__(self):
        pass

    def write(self, data):
        pass

    def seek(self, pos: int, whence = io.SEEK_SET):
        pass

    def tell(self) -> int:
        pass
