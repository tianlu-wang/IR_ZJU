__author__ = 'wenri'

from Index.Term import Term

class TokenStream(object):
    def __init__(self, field: str):
        self.field = field

    def incrementToken(self) -> bool:
        pass

    def close(self):
        pass

    def reset(self):
        pass

    def end(self):
        pass

    def getTerm(self) -> Term:
        pass

    def getPosition(self):
        pass