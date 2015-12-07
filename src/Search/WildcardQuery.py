__author__ = 'wenri'

from Search.Query import Query
from Utilities.Dictionary import Dictionary
import re

class WildcardQuery(Query):
    def __init__(self, string: str):
        Query.__init__(self, string)
        self.s = string

    def getPossibleQuery(self, dictionary: Dictionary) -> list:
        possibleWords = []
        postfix = self.s.split()
        prefix = []
        while len(postfix) > 0:
            item = postfix[0]
            del postfix[0]
            if item.find('*') >= 0:
                rep = re.compile(item.replace('*', '\\w*'))
                for term in dictionary.dictionary:
                    if rep.match(term):
                        possibleWords.append(term)
                break
            else:
                prefix.append(item)


        if len(possibleWords) > 0:
            result = []
            for item in possibleWords:
                result.append(' '.join(prefix + [item] + postfix))
        else:
            result = [ self.s ]

        return result