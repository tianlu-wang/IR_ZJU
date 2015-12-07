__author__ = 'wenri'

from Store.Directory import Directory
from Index.Term import Term
from Codecs.DummyTermVectorsReader import DummyTermVectorsReader
from Utilities.Dictionary import Dictionary
import math

class IndexReader(object):
    def __init__(self, directory: Directory):
        self.d = directory
        self.codecs = DummyTermVectorsReader(self.d)
        self.numOfDocs = 0
        self.indexFormTitle = dict()  # key: term value:list list[0] is total frequency list[1] is a dict key is docID  value is a list list[0] is frequency list[1] is a list
        self.indexFormAbstract = dict()
        self.indexFormContents = dict()

        #  construct the form
        while True:  # assume if there is no document return 0
            numFields = self.codecs.getDocument()
            if numFields == 0:
                break

            for i in range(numFields):
                fieldName, numTerms = self.codecs.getField()
                if fieldName == 'title':
                    self.handleField(numTerms, self.indexFormTitle, self.numOfDocs)
                elif fieldName == 'abstract':
                    self.handleField(numTerms, self.indexFormAbstract, self.numOfDocs)
                elif fieldName == 'contents':
                    self.handleField(numTerms, self.indexFormContents, self.numOfDocs)
                self.codecs.finishField()

            self.codecs.finishDocument()
            self.numOfDocs += 1
        self.dictionary = Dictionary(directory)
        self.dictionary.load()

    def handleField(self, numTerms:int, dictInput: dict, numOfDocs:int):  # termInfo[0] is frequency and termInfo[1] is the term
        if numTerms > 0:
            sum = 0
            termList = []
            for i in range(numTerms):
                termInfo = self.codecs.getTerm()
                termList.append(termInfo[1])
                sum += termInfo[0] ** 2
                tempList1 = []
                for j in range(termInfo[0]):
                    tempList1.append(self.codecs.getPosition())
                positionList = [termInfo[0], tempList1]
                if dictInput.get(termInfo[1]) is None:  # new term
                    record = [termInfo[0], {numOfDocs: positionList}]
                else:
                    record = dictInput.get(termInfo[1])
                    record[0] += termInfo[0]
                    tempDict = {numOfDocs: positionList}
                    record[1].update(tempDict)
                dictInput[termInfo[1]] = record
                self.codecs.finishTerm()
            sum = math.sqrt(sum)
            for term in termList:
                record = dictInput[term]
                positionList = record[1][numOfDocs]
                positionList[0] /= sum
        else:
            pass

    def docFreq(self, term: Term):
        if term.field is 'title':
            return len(self.indexFormTitle.get(term)[1])
        elif term.field is 'abstract':
            return len(self.indexFormAbstract.get(term)[1])
        else:
            return len(self.indexFormContents.get(term)[1])

    def getTermVector(self, docID: int, field:str):
        result = {}
        if field is 'title':
            self.getTermVectorField(docID, self.indexFormTitle, result)
        elif field is 'abstract':
            self.getTermVectorField(docID, self.indexFormAbstract, result)
        else:
            self.getTermVectorField(docID, self.indexFormContents, result)
        return result

    def getTermVectorField(self, docID: int, indexForm: dict, result: dict):
        for key in indexForm.keys():
            if docID in indexForm.get(key)[1]:
                result[key] = indexForm.get(key)[1].get(docID)[0]
        return result

    def termPosition(self, term: Term):
        if term.field is 'title':
            tempDict = self.indexFormTitle.get(term)
        elif term.field is 'abstract':
            tempDict = self.indexFormAbstract.get(term)
        else:
            tempDict = self.indexFormContents.get(term)

        '''
        newDict = {}
        for key in tempDict.keys():
            newDict[key] = tempDict.get(key)[1]
        return newDict
        '''

        if tempDict is not None:
            return tempDict[1]
        else:
            return None


    def numDocs(self) -> int:
        return self.numOfDocs

    def totalTermFreq(self,term: Term) -> int:
        if term.field is 'title':
            return self.indexFormTitle.get(term)[0]
        elif term.field is 'abstract':
            return self.indexFormAbstract.get(term)[0]
        else:
            return self.indexFormContents.get(term)[0]
