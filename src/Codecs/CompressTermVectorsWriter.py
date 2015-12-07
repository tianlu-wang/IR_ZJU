__author__ = 'wenri'
import math
from Store.Directory import Directory
from Index.Term import Term
from Codecs.TermVectorsWriter import TermVectorsWriter

class CompressTermVectorsWriter(TermVectorsWriter):
    array_write = 233
    ans_sum = bytearray(0)

    def __init__(self, directory: Directory):
        TermVectorsWriter.__init__(self, directory)
        self.fileOutput = self.d.openOutput('compressIndex')

    def write(self, bin):
        if self.array_write *2 > 255:
            ans = (self.array_write).to_bytes(1, byteorder="big")
            self.ans_sum += bytearray(ans)
            self.array_write = 0
        self.array_write *= 2
        self.array_write += bin
    def write_a_number(self, number):
        string = ''
        if number == 1:
            string = '0'
        else:
            len = int(math.log(number)/math.log(2))
            i = 0
            while i < len:
                string += '1'
                i = i+1
            string+='0'
            bit = bin(number)[3:]
            string += str(bit)
        for i in string:
            self.write(int(i))
        return string
    def write_a_word(self, word):
        for i in word:
            self.write_a_number(ord(i))
    def addPosition(self, position: int, startOffset: int, endOffset: int):
        self.write_a_number(position)
        self.write_a_number(startOffset)
        self.write_a_number(endOffset)
    def finishDocument(self):
        #write(self.ans_sum)
        self.fileOutput.write(self.ans_sum)
        self.ans_sum = bytearray(0)
    def finishField(self):
        pass
    def finishTerm(self):
        pass
    def startDocument(self, numVectorFields: int):
        self.write_a_number(numVectorFields)
    def startField(self, fieldInfo, numTerms: int):
        self.write_a_number(len(str(fieldInfo)))
        self.write_a_word(str(fieldInfo))
        self.write_a_number(numTerms)
    def startTerm(self, term: Term, freq: int):
        self.write_a_number(len(str(term.text)))
        self.write_a_word(str(term.text))
        self.write_a_number(freq)