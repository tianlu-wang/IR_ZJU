__author__ = 'wenri'

from Analysis.Tokenizer import Tokenizer
from Index.Term import Term
from nltk import word_tokenize

class WhitespaceTokenizer(Tokenizer):
    def __init__(self, field: str, reader):
        Tokenizer.__init__(self, field, reader)

        self.tokens = list()
        for lineBytes in reader:
            if isinstance(lineBytes, str):
                line = lineBytes
            else:
                line = str(lineBytes, 'latin1')

            self.tokens += word_tokenize(line.lower())

    def incrementToken(self) -> bool:
        try:
            self.token = next(self.tokenIter)
            self.position += 1
            self.offset += self.len + 1
            self.len = len(self.token)

        except StopIteration:
            return False

        return True

    def close(self):
        self.tokens.clear()

    def reset(self):
        self.tokenIter = iter(self.tokens)
        self.position = 0
        self.offset = 0
        self.len = 0

    def end(self):
        pass

    def getTerm(self) -> Term:
        return Term(self.field, self.token)

    def getPosition(self):
        return self.position, self.offset, self.offset + self.len
