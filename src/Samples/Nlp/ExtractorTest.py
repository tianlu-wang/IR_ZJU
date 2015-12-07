__author__ = 'wtl'
from Utilities.Extractor import *
import zipfile


with zipfile.ZipFile('Samples/Reuters/Reuters.zip') as zipf:
    for zipArticle in zipf.infolist():
        strArticle = ''
        with zipf.open(zipArticle) as article:
            strTitle = str(article.readline(), 'latin1')
            for line in article:
                strArticle += str(line, 'latin1')
            abstract = summarize('', strTitle, strArticle)
            print('Title: ' + strTitle + ', Abstract: ', abstract)