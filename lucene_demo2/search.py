# -*- coding:utf-8 -*-

import mysql.connector
from mysql.connector import Error
import sys, os, threading, time
import lucene as lc


from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.util import Version
from java.nio.file import Paths, Path
from org.apache.lucene.document import Field, StringField, TextField
from org.wltea.analyzer
import java.io


class Indexer(object):
    def __init__(self, store_file):
        self.__analyzer = StandardAnalyzer()
        self.__indexWriterConfig = IndexWriterConfig(self.__analyzer)
        self.__indexWriterConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.__directory = MMapDirectory.open(Paths.get(store_file))
        self.__indexWriter = IndexWriter(self.__directory, self.__indexWriterConfig)

    def write(self, data):
        if None in data or u"" in data:
            return
        t1 = FieldType()
        t1.setStored(False)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        doc = Document()
        doc.add(Field("id", unicode(data[u"id"]), t1))
        doc.add(Field("title", unicode(data[u"title"]), t2))
        doc.add(Field("content", unicode(data[u"content"]), t2))
        self.__indexWriter.addDocument(doc)

    def flush(self):
        self.__indexWriter.commit()

    def close(self):
        self.__indexWriter.commit()
        self.__indexWriter.close()
        self.__directory.close()


class Searcher(object):
    def __init__(self):
        lc.initVM()

    def update_index_file(self):
        conn = None
        indexer = Indexer("./indexes")
        try:
            conn = mysql.connector.connect(host="localhost", database="news", user="root", password="?&*()NSDWE19")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM news")
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

    

s = Searcher()
s.update_index_file()

