__author__ = 'wenri'

from Analysis.TokenFilter import TokenFilter
from Analysis.TokenStream import TokenStream
from Index.Term import Term
from nltk.corpus import stopwords
import string

class PunctuationFilters(TokenFilter):
    additional_stopwords = ['lt']
    stop = set(stopwords.words('english') + additional_stopwords).union( set(string.punctuation) )

    def __init__(self, inputStream: TokenStream):
        TokenFilter.__init__(self, inputStream)

    def incrementToken(self) -> bool:
        while self.stream.incrementToken():
            self.term = self.stream.getTerm()
            if str.isalnum(self.term.text) and self.term.text not in PunctuationFilters.stop:
                return True

        return False

    def close(self):
        self.stream.close()

    def reset(self):
        self.stream.reset()

    def end(self):
        self.stream.end()

    def getTerm(self) -> Term:
        return self.term

