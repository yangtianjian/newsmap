# -*- coding:utf-8 -*-

import mysql.connector
from mysql.connector import Error
import sys, os, threading, time
import lucene as lc
import jcc

lc.initVM()
from java.io import File, IOException, StringReader
from java.nio.file import Paths
from org.apache.lucene.analysis import Analyzer, TokenStream
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute, TermToBytesRefAttribute
from org.apache.lucene.document import Document, Field, TextField, FieldType
from org.apache.lucene.index import DirectoryReader, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, Query, TopDocs
from org.apache.lucene.store import Directory, FSDirectory, SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.cn.smart import SmartChineseAnalyzer


class Indexer(object):
    def __init__(self, index_path):
        self.__directory = SimpleFSDirectory(Paths.get(index_path))
        analyzer = SmartChineseAnalyzer()
        indexWriterConfig = IndexWriterConfig(analyzer)
        self.__indexWriter = IndexWriter(self.__directory, indexWriterConfig)
        self.__indexWriter.deleteAll()

    def write(self, data):
        if None in data or u"" in data:
            return
        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        try:
            document = Document()
            document.add(Field(u"id", unicode(data[u"id"]), t1))
            document.add(Field(u"title", unicode(data[u"title"]), t2))
            document.add(Field(u"content", unicode(data[u"content"]), t2))
            self.__indexWriter.addDocument(document)
        except Exception as e:
            print e.message

    def flush(self):
        self.__indexWriter.commit()

    def close(self):
        self.__indexWriter.commit()
        self.__indexWriter.close()
        self.__directory.close()


class Searcher(object):
    def __init__(self, index_file):
        self.__index_file = index_file
        self.__directory = SimpleFSDirectory(Paths.get(index_file))

    def update_index(self):
        conn = None
        indexer = Indexer(self.__index_file)
        try:
            conn = mysql.connector.connect(host="localhost", database="news", user="root", password="?&*()NSDWE19")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM news;")
            symbol = cursor.column_names
            all_data = cursor.fetchall()
            for i in range(0, len(all_data)):
                d = {}
                for j in range(0, len(symbol)):
                    d[symbol[j]] = all_data[i][j]
                indexer.write(d)
        except Error as e:
            print e.message
        except Exception as e:
            print e.message
        finally:
            if conn:
                conn.close()
        indexer.close()

    def query(self, kw):
        directoryReader = DirectoryReader.open(self.__directory)
        indexSearcher = IndexSearcher(directoryReader)
        analyzer = SmartChineseAnalyzer()
        parser = QueryParser("content", analyzer)
        query = parser.parse(kw)
        topDocs = indexSearcher.search(query, 99999)
        scoreDocs = topDocs.scoreDocs
        result = list()
        for scoreDoc in scoreDocs:
            document = indexSearcher.doc(scoreDoc.doc)
            result.append(document.get("id"))
        return result


def query(keyword):
    s = Searcher("./index")
    res = s.query(keyword)
    return res