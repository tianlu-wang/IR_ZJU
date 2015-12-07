__author__ = 'yunshen'

from Analysis.TokenStream import TokenStream
from Analysis.TokenFilter import TokenFilter
from Index.Term import Term

class StemFilter(TokenFilter):
    def __init__(self, inputStream: TokenStream):
        TokenFilter.__init__(self, inputStream)
        self.buffer = ""
        self.k = 0
        self.f = 0
        self.length = 0

    def cons(self, i):
        if self.buffer[i] == 'a' or self.buffer[i] == 'e' or self.buffer[i] == 'i' or self.buffer[i] == 'o' or \
                        self.buffer[i] == 'u':
            return 0
        elif self.buffer[i] == 'y':
            if i == self.f or not self.cons(i - 1):
                return 1
            else:
                return 0
            return 1

    def vc_num(self):
        n = 0
        i = self.f
        while i <= self.length:  # may be wrong, find the first sequence of vowel
            if not self.cons(i):
                break
            i += 1
        i += 1
        while i <= self.length:
            while i <= self.length:
                if self.cons(i):
                    break
                i += 1
            n += 1
            i += 1
            while i <= self.length:
                if not self.cons(i):
                    break
                i += 1
            i += 1
        # print 'n'
        #print n
        return n

    def at_least_one_v(self):
        i = self.f
        while i <= self.length:  # may be wrong, the length includes '\0'??
            if not self.cons(i):
                return 1
            else:
                i += 1
        return 0

    def doublecon(self, i):
        if i < 1:
            return 0
        if self.buffer[i] != self.buffer[i - 1]:
            return 0
        return self.cons(i)

    def cvc_form(self, i):
        if i < 2 or not self.cons(i - 2) or self.cons(i - 1) or not self.cons(i):
            return 0
        if self.buffer[i] == 'w' or self.buffer[i] == 'x' or self.buffer[i] == 'y':
            return 0
        return 1

    def ends(self, s):
        l = len(s)
        o = self.k - l + 1
        if ( o < 0 ):
            return 0
        i = 0
        for ch in self.buffer[o:self.k + 1]:
            if ch != s[i]:
                return 0
            else:
                i += 1
        self.length = self.k - l  # length change
        # print 'in ends() :self.length'
        #print self.length
        return 1

    def setto(self, s):
        l = len(s)
        o = self.length + 1
        # print 'ooo'
        #print o
        self.buffer = self.buffer[:self.length + 1] + s + self.buffer[self.length + l + 1:]
        self.k = self.length + l

    def replace(self, s):
        if self.vc_num()> 0:
            self.setto(s)

    def step1(self):
        # print self.k
        #print self.buffer[self.k]
        if (self.buffer[self.k] == 's'):  #sses-->ss
            if self.ends("sses"):
                self.setto("ss")  #length may be wrong
            elif self.ends("ies"):  #ies-->i
                self.setto("i")
            elif self.buffer[self.k - 1] != 's':  #s-->
                if self.ends("s"):
                    #print 'yes'
                    self.setto("")  #length may be wrong
                    #self.length--

        if (self.ends("eed")):
            if self.vc_num()> 0:
                self.k -= 1
                #self.length--
        elif (self.ends("ed") or self.ends("ing")) and self.at_least_one_v():
            self.k = self.length
            if self.ends("at"):
                self.setto("ate")
            elif self.ends("bl"):
                self.setto("ble")
            elif self.vc_num() == 1 and self.cvc_form(self.k):
                self.setto("e")
            elif self.doublecon(self.k):
                self.k -= 1
                #self.length--
                if self.buffer[self.k] == 's' or self.buffer[self.k] == 'l' or self.buffer[self.k] == 'z':
                    self.k += 1
                    #self.length++

        if self.ends("y") and self.at_least_one_v():
            self.setto("i")

    def step2(self):
        if self.k == 0:
            return
        if self.buffer[self.k - 1] == 'a':
            if self.ends("ational"):
                self.replace("ate")
            elif self.ends("tional"):
                self.replace("tion")
        elif self.buffer[self.k - 1] == 'c':
            if self.ends("enci"):
                self.replace("ence")
            elif self.ends("anci"):
                self.replace("ance")
        elif self.ends("izer"):
            self.replace("ize")
        elif self.buffer[self.k - 1] == 'l':
            if self.ends("bli"):
                self.replace("ble")
            elif self.ends("alli"):
                self.replace("al")
            elif self.ends("entli"):
                self.replace("ent")
            elif self.ends("eli"):
                self.replace("e")
            elif self.ends("ousli"):
                self.replace("ous")
        elif self.buffer[self.k - 1] == 'o':
            if self.ends("ization"):
                self.replace("ize")
            elif self.ends("ation"):
                self.replace("ate")
            elif self.ends("ator"):
                self.replace("ate")
        elif self.buffer[self.k - 1] == 's':
            if self.ends("alism"):
                self.replace("al")
            elif self.ends("iveness"):
                self.replace("ive")
            elif self.ends("fulness"):
                self.replace("ful")
            elif self.ends("ousness"):
                self.replace("ous")
        elif self.buffer[self.k - 1] == 't':
            if self.ends("aliti"):
                self.replace("al")
            elif self.ends("iviti"):
                self.replace("ive")
            elif self.ends("biliti"):
                self.replace("ble")
        elif self.buffer[self.k - 1] == 'g':
            if self.ends("logi"):
                self.replace("log")

    def step3(self):
        if self.buffer[self.k] == 'e':
            if self.ends("icate"):
                self.replace("ic")
            elif self.ends("ative"):
                self.replace("")
            elif self.ends("alize"):
                self.replace("al")
        elif self.buffer[self.k] == 'i':
            if self.ends("iciti"):
                self.replace("ic")
        elif self.buffer[self.k] == 'l':
            if self.ends("ical"):
                self.replace("ic")
            elif self.ends("ful"):
                self.replace("")
        elif self.buffer[self.k] == 's':
            if self.ends("ness"):
                self.replace("")

    def step4(self):
        if self.buffer[self.k - 1] == 'a':
            if self.ends("al"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'c':
            if self.ends("ance"):
                #print('step4 ance')
                # if self.vc_num()>1:
                #self.k=self.length
                pass
            elif self.ends("ence"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'e':
            if self.ends("er"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'i':
            if self.ends("ic"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'l':
            if self.ends("able"):
                pass
            elif self.ends("ible"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'n':
            if self.ends("ant"):
                pass
            elif self.ends("ement"):
                pass
            elif self.ends("ment"):
                pass
            elif self.ends("ent"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'o':  # may be wrong
            if self.ends("ion") and (self.buffer[self.length] == 's' or self.buffer[self.length] == 't'):
                pass
            elif self.ends("ou"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 's':
            if self.ends("ism"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 't':
            if self.ends("ate"):
                pass
            elif self.ends("iti"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'u':
            if self.ends("ous"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'v':
            if self.ends("ive"):
                pass
            else:
                return
        elif self.buffer[self.k - 1] == 'z':
            if self.ends("ize"):
                pass
            else:
                return
        else:
            return
        if self.vc_num() > 1:
            self.k = self.length  # change the word

            # def step5(self): #may be wrong
            #self.length=self.k
            #if self.buffer[self.k]=='e':
            #if self.vc_num()>1 or (self.vc_num()==1 and not self.cvc_form(self.k-1)):
            #self.k-=1
            #if self.vc_num()>1 and self.doublecon(self.k) and self.buffer[self.k]=='l':
            #self.k-=1
    def stem(self, p, m, n):
        try:
            self.buffer = p
            self.k = n
            self.f = m
            self.length = n
            if self.k <= self.f + 1:
                return self.buffer
            self.step1()
            #print('step 1')
            #print(self.buffer, self.k)
            self.step2()
            #print('step 2')
            #print(self.buffer, self.k)
            self.step3()
            #print('step 3')
            #print(self.buffer, self.k)
            self.step4()
            #print('step 4')
            #print(self.buffer, self.k)
            #self.step5()
            #print 'step 5'
            #print self.buffer, self.k
            return self.buffer[self.f:self.k + 1]
        except TypeError:
            print("Error at '" + p + "'")


    def incrementToken(self) -> bool:
        return self.stream.incrementToken()

    def close(self):
        self.stream.close()

    def reset(self):
        self.stream.reset()

    def end(self):
        self.stream.end()

    def getTerm(self) -> Term:
        term = self.stream.getTerm()
        term.text = self.stem(term.text, 0, len(term.text)-1)
        return term







