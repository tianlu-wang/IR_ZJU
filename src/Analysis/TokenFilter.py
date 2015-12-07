__author__ = 'wenri'

from Analysis.TokenStream import TokenStream

class TokenFilter(TokenStream):
    def __init__(self, inputStream: TokenStream):
        TokenStream.__init__(self, inputStream.field)
        self.stream = inputStream

    def getPosition(self):
        return self.stream.getPosition()
