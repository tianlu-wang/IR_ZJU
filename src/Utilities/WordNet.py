__author__ = 'wenri'

from nltk.corpus import wordnet as wn

def GetSimilar(word: str):
    result = set()
    synsets = wn.synsets(word)
    for synset in synsets:
        result.add(synset.name().split('.')[0])
    print("Word: ", word, "Set: ", result)
    return result