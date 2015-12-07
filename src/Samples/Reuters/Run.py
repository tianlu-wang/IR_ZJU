__author__ = 'Wenri'

from Samples.Reuters.Server import FlaskServer
from Samples.Reuters.Reuters import ReutersData
import os

def CLIHandler():
    reuters = ReutersData(os.path.join('Samples', 'Reuters'))
    reuters.constructIndexReader()

    while True:
        queryString = input("Wildcard Query String: ")
        for docId, score in reuters.ScoredQuery(queryString, -1):
            print(score, reuters.documentMap[docId][0])
            print(reuters.documentMap[docId][2])


def CGIHandler():
    reuters = ReutersData(os.path.join('Samples', 'Reuters'))
    reuters.constructIndexReader()
    FlaskServer.run(reuters)

if __name__ == '__main__':
    CGIHandler()
