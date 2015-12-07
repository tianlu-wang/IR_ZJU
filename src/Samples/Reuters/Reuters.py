__author__ = 'wenri'

from Analysis.StandardAnalyzer import StandardAnalyzer
from Analysis.SimpleAnalyzer import SimpleAnalyzer
from Store.FileSystemDirectory import FileSystemDirectory
from Store.Directory import Directory
from Index.IndexWriterConfig import IndexWriterConfig
from Index.IndexWriter import IndexWriter
from Index.IndexReader import IndexReader
from Document.Document import Document
from Document.StringField import StringField
from Document.TextField import TextField
from Utilities.Extractor import summarize
from Utilities.Dictionary import Dictionary
from Utilities.SpellCheck import SpellCheck
from Utilities.WordNet import GetSimilar
from Search.Query import Query
from Search.PhraseQuery import PhraseQuery
from Search.BooleanQuery import BooleanQuery
from Search.WildcardQuery import WildcardQuery
from Search.IndexSearcher import IndexSearcher
import zipfile
import os
import pickle
import heapq

class ReutersData(object):
    def __init__(self, basePath: str):
        self.documentMap = list()
        self.basePath = basePath

    def addArticle(self, w, article):
        global documentMap

        strTitle = str(article.readline(), 'latin1')
        strArticle = ''
        for line in article:
            strArticle += str(line, 'latin1')
        strAbstract = summarize('', strTitle, strArticle)

        document = Document()
        document.add(StringField('title', strTitle))
        document.add(TextField('abstract', strAbstract))
        document.add(StringField('contents', strArticle))

        w.addDocument(document)
        self.documentMap.append( (strTitle, strAbstract, strArticle) )

    def LoadArchive(self, filename: str, index: Directory):
        analyzer = StandardAnalyzer()
        config = IndexWriterConfig(analyzer)
        w = IndexWriter(index, config)

        with zipfile.ZipFile(filename) as zipf:
            for zipArticle in zipf.infolist():
                with zipf.open(zipArticle) as article:
                    self.addArticle(w, article)

        w.close()

    def constructIndexReader(self):
        directory = FileSystemDirectory(self.basePath)
        mapFilePath = os.path.join(self.basePath, 'documentMap')
        if os.path.exists(mapFilePath):
            print('Loading documents map...')
            with open(mapFilePath, 'rb') as mapFile:
                self.documentMap = pickle.load(mapFile)
        else:
            print('Building index and documents map...')
            self.LoadArchive(os.path.join(self.basePath, 'Reuters.zip'), directory)
            print('Writing documents map...')
            with open(mapFilePath, 'wb') as mapFile:
                pickle.dump(self.documentMap, mapFile)
        print('Loading index and building inverted table...')
        self.index = IndexReader(directory)

    def ScoredQuery(self, queryString: str, k: int) -> list:
        print('Starting query: ' + queryString)
        query = WildcardQuery(queryString)
        searcher = IndexSearcher(self.index, query, '')
        return searcher.Wildcardsearch(k)

    def BooleanQuery(self, queryString: str) -> list:
        print('Starting query: ' + queryString)
        query = BooleanQuery(queryString)
        searcher = IndexSearcher(self.index, query, '')
        return searcher.Boolsearch()

    def PhraseQuery(self, queryString: str, k: int) -> list:
        print('Starting query: ' + queryString)
        query = WildcardQuery(queryString)
        searcher = IndexSearcher(self.index, query, '')
        searcher.Wildcardsearch(0)
        return searcher.Phrasefilter(query.getPossibleQuery(self.index.dictionary), k)

    def SimilarQuery(self, queryString: str, k: int) -> list:
        print('Starting similar query: ' + queryString)
        querySet = set()
        for queryStr in queryString.split():
            querySet.add(queryStr)
            querySet |= GetSimilar(queryStr)
        print("QuerySet: ", querySet)
        self.queryStr = ' '.join(querySet)
        query = Query(self.queryStr)
        searcher = IndexSearcher(self.index, query, '')
        return searcher.Indexsearch(k)

    def CheckSpell(self, queryString: str) -> list:
        return SpellCheck(self.index.dictionary).CheckSpell(queryString)
