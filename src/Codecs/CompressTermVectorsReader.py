__author__ = 'wenri'

from Store.Directory import Directory
from Index.Term import Term
from Codecs.TermVectorsReader import TermVectorsReader

class CompressTermVectorsReader(TermVectorsReader):
    array_read = '11010101'
    head_read = 0
    field_name = ''

    def __init__(self, directory: Directory):
        TermVectorsReader.__init__(self, directory)
        self.inputFile = self.d.openInput('compressIndex')

    def read(self):
        if self.head_read == 8:
            self.inputFile.read(1)
            s1 = 233
            self.array_read = str(bin(s1)[2:])
            self.head_read = 0
        ans = self.array_read[self.head_read]
        self.head_read += 1
        return ans
    def read_a_number(self):
        l_counter = 0
        char = self.read()
        if char == '0':
            ans = 1
            return ans
        while char != '0':
            l_counter = l_counter+1
            char = self.read()
        j = 0
        num_str = ''
        while j < l_counter:
            char = self.read()
            num_str += char
            j = j+1
        num_str = '1'+num_str
        num_str = int(num_str,2)
        return num_str
    def read_a_word(self, l):
        word_list = ''
        i = 0
        while i < l:
            char = self.read_a_number()
            char = chr(char)
            word_list += char
            i = i+1
        return word_list
    def getDocument(self)->int:  # return numVectorFields
        return self.read_a_number()

    def getField(self)->(str,int):  # return numTerms
        l = self.read_a_number()
        s = self.read_a_word(l)
        num = self.read_a_number()
        self.field_name = s
        return (s,num)

    def getTerm(self)->(int, Term):  # return a tuple: frequency and the term
        l = self.read_a_number()
        text = self.read_a_word(l)
        freq = self.read_a_number()
        tem = Term(self.field_name, text)
        return (freq, tem)
    def getPosition(self)->tuple:  # position and startOffset and endOffset are put in a tuple
        position = self.read_a_number()
        startOffset = self.read_a_number()
        endOffset = self.read_a_number()
        return (position, startOffset, endOffset)
    def finishTerm(self):
        pass

    def finishField(self):
        pass

    def finishDocument(self):
        pass