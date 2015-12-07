__author__ = 'wenri'

class Term(object):
    def __init__(self, fld: str, text: str):
        self.field = fld
        self.text = text

    def __hash__(self):
        return self.text.__hash__()

    def __eq__(self, other):
        if isinstance(other, Term):
            return self.text.__eq__(other.text)
        else:
            return self.text.__eq__(other)
