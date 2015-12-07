__author__ = 'wenri'

from Samples.Reuters import Run as Reuters
from Samples.Tokenize import StringTokenize
import nltk
import os

SampleTable = {
    'reuters': Reuters.CLIHandler,
    'tokenize': StringTokenize.tokenizePrint,
    'server': Reuters.CGIHandler
}

def Welcome():
    print('Welcome to IR Testing System')

def Version():
    print('This is alpha version of IR Test System')
    print('Author: Shengming Zhang, Yun Shen, Tianlu Wang and Bingchen Gong')

def PrintSamples():
    print('The following test are available: ')
    for k in SampleTable:
        print(k)

def main():
    Welcome()
    print()
    Version()
    print()
    PrintSamples()
    print()
    index = input('Select target testing procedure: ').lower()
    if index in SampleTable:
        SampleTable[index]()
    else:
        print("Wrong input!")

if __name__ == '__main__':
    nltk.data.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resource', 'nltk_data'))
    main()
