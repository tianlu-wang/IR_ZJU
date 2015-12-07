__author__ = 'wenri'

from Analysis.StandardAnalyzer import StandardAnalyzer

def tokenizePrint():
    while True:
        analyzer = StandardAnalyzer()
        ts = analyzer.tokenStream("myfield", [ input("Input the string to tokenize: ") ])
        #    OffsetAttribute offsetAtt = addAttribute(OffsetAttribute.class);

        ts.reset() # Resets this stream to the beginning. (Required)
        while ts.incrementToken() :
            # Use AttributeSource.reflectAsString(boolean)
            # for token stream debugging.
            print("token: " + ts.getTerm().text)
            print('pos: ', ts.getPosition())
            #print("token start offset: " + offsetAtt.startOffset())
            #print("  token end offset: " + offsetAtt.endOffset())

        ts.end()   # Perform end-of-stream operations, e.g. set the final offset.

        ts.close() # Release resources associated with this stream.


if __name__ == '__main__':
    tokenizePrint()
