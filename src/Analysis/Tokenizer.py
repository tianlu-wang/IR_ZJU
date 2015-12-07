__author__ = 'wenri'

from Analysis.TokenStream import TokenStream

class Tokenizer(TokenStream):
    def __init__(self, field: str, reader):
        TokenStream.__init__(self, field)
        self.reader = reader
