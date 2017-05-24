# -*- coding:utf-8 -*-

from selenium import webdriver
from csv_parser import CSVParser
import urllib
import re
import os
import sys
import mysql.connector
from mysql.connector import Error


def extract_links(source, base):
    assert isinstance(source, str)
    lret = set([])
    p = 0
    while True:
        p = source.find("<a href=\"" + base + "/news", p)
        if p == -1:
            break
        p2 = source.find("\"", p + len("<a href=\""))
        if p2 == -1:
            break
        lret.add(source[p + len("<a href=\""): p2])
        p = p2 + 1
    lremove = set([])
    for addr in lret:
        pattern = re.compile(r".*\d\d\d\d-\d\d-\d\d.*")
        match_str = re.match(pattern, addr)
        if not match_str:
            lremove.add(addr)   #delete address without date
    return lret - lremove


def extract_news_info(url):
    assert isinstance(url, str)
    title = ""
    content = ""
    request = urllib.urlopen(url)
    source = request.read()
    assert isinstance(source, str)

    pArticleBox = source.find("<div class=\"article-box\"", 0)
    pArticleHeader = source.find("<div class=\"article-header", pArticleBox)
    pTitle = source.find("<h1>", pArticleHeader)
    pTitleEnd = source.find("</h1>", pTitle)
    assert pArticleBox != -1 and pArticleHeader != -1 and pTitle != -1 and pTitleEnd != -1
    title += source[pTitle + len("<h1>"): pTitleEnd].strip()

    stackNum = 1

    pFind = pArticleBox + len("<div class=\"article-box\"")  #find paired /div
    while stackNum > 0:
        p1 = source.find("<div", pFind)
        p2 = source.find("</div>", pFind)
        if p1 < p2:
            stackNum += 1
            pFind = p1 + len("<div")
        else:
            stackNum -= 1
            pFind = p2 + len("</div>")
    pContentEnd = pFind             #get the end of the content


    pContent = source.find("<div class=\"article-body main-body\">", pTitleEnd)
    while True:
        pParagraph = source.find("<p>", pContent)
        if pParagraph == -1 or pParagraph > pContentEnd:
            break
        pParagraphEnd = source.find("</p>", pParagraph)
        assert pContentEnd != -1
        content += source[pParagraph + len("<p>"): pParagraphEnd]
        pContent = pParagraphEnd + len("</p>")

    pFindBracket = 0
    pLast = False #true: the last bracket is <

    while True:
        if pLast:
            pFindBracketEnd = content.find(">", pFindBracket)
            if pFindBracketEnd == -1:
                break
            strMid = content[pFindBracket: pFindBracketEnd + 1]
            content = content.replace(strMid, "")
            pLast = False
            pFindBracket = 0
        else:
            pFindBracketNext = content.find("<", pFindBracket)
            if pFindBracketNext == -1:
                break
            pFindBracket = pFindBracketNext
            pLast = True

    return title, content


def write_news_to_file(title, content, date, province):
    assert isinstance(title, str)
    assert isinstance(content, str)
    assert isinstance(date, str)
    assert isinstance(province, str)
    f = open("./newsdata", "a")
    f.write(title + content + date + province)
    f.write("-------------------------------------------------\n")
    f.close()


def open_database_connection():
    conn = None
    try:
        conn = mysql.connector.connect(host="localhost", database="news", user="root", password="?&*()NSDWE19", charset="utf8")
        cursor = conn.cursor()
        cursor.execute("SET names utf8;")
        cursor.execute("SET character_set_client = utf8;")
        cursor.execute("SET character_set_connection = utf8;")
        cursor.execute("SET character_set_database = utf8;")
        cursor.execute("SET character_set_results = utf8;")
        cursor.execute("SET character_set_server = utf8;")
    except Error as e:
        print "Cannot connect to database, the error message:" + e.message + "\n"
        if conn is not None:
            conn.close()
            os._exit()
    return conn


def close_database_connection(conn):
    assert isinstance(conn, mysql.connector.connection.MySQLConnection)
    if conn is not None:
        conn.close()


def create_table(conn):
    assert isinstance(conn, mysql.connector.connection.MySQLConnection)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS news (id INT UNIQUE AUTO_INCREMENT, title VARCHAR(50), time_happened DATE, province VARCHAR(10), content TEXT, link TEXT, PRIMARY KEY(title, time_happened)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")


def write_news_to_database(conn, title, content, date, province, link):
    assert isinstance(conn, mysql.connector.connection.MySQLConnection)
    cursor = conn.cursor()
    content = content.replace("\\", "\\\\").replace("'", "\\'")
    title = title.replace("\\", "\\\\").replace("'", "\\'")
    link = link.replace("\\", "\\\\").replace("'", "\\'")
    sql = "INSERT INTO news(title, time_happened, province, content, link) VALUES('%s','%s','%s','%s', '%s');" % (title, date, province, content, link)
    cursor.execute(sql)
    conn.commit()


def rearrange_id(conn):
    cursor = conn.cursor()
    cursor.callproc("rearrange_id")


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    parser = CSVParser("./webmapping.csv")
    parser.parse()
    data = parser.get_element(1, 25, 0, 2)
    entry_dict = {}
    l = len(data)
    for i in range(0, l):
        entry_dict[data[i][0]] = ("http://" + data[i][1] + ".sina.com.cn").replace("\r", "").replace("\n", "")

    conn = open_database_connection()
    create_table(conn)
    for province in entry_dict.keys():
        url = entry_dict[province]
        source = urllib.urlopen(url).read()
        lnews = extract_links(source, url)          # the link of all news
        for lanews in lnews:
            try:
                title, content = extract_news_info(lanews)
                pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
                date = re.search(pattern, lanews).group()
                write_news_to_database(conn, title, content, date, province, lanews)
            except AssertionError as e:  #regardless of invalid news
                continue
            except Exception as e2:
                print "In news " + lanews + ":" + e2.message + "\n"
    conn.commit()
    print "Rearranging..."
    rearrange_id(conn)
    print "Finished."
    close_database_connection(conn)

main()