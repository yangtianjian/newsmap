#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from csv_parser import CSVParser
import mysql.connector
from mysql.connector import Error
import urllib
import urlparse
import lxml.html
from search import Searcher


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
            exit(0)
    return conn


def get_substring(the_str, str_begin, str_end, index_begin):
    if index_begin >= len(the_str) - 1:
        return "", -1
    p1 = the_str.find(str_begin, index_begin) + len(str_begin)
    if p1 == -1 or p1 < index_begin:
        return "", -1
    p2 = the_str.find(str_end, p1)
    if p2 == -1 or p2 < p1:
        return "", -1
    return the_str[p1: p2], p2 + len(str_end)


def normalize(content_str):
    p = 0
    ret_str = content_str
    while True:
        sub_str, pnext = get_substring(content_str, "<", ">", p)
        if pnext == -1:
            break
        ret_str = ret_str.replace("<" + sub_str + ">", "")
        p = pnext
    return ret_str.replace("\\", "\\\\").replace("\'", "\\\'")


def save_news_content(conn, info):
    req = urllib.urlopen(info["link"])
    html = req.read().decode("gbk").encode("utf-8").lower()
    p = 0
    content_str = ""
    while True:
        para, pnext = get_substring(html, "<p>", "</p>", p)
        if pnext == -1:
            break
        content_str += "\n  " + para
        p = pnext
    content_str = normalize(content_str).strip()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM news;")
    id = cursor.fetchone()[0] + 1
    time, no_use = get_substring(info["link"], "/", "/", 7)
    sql = "INSERT INTO news(id, title, time_happened, province, content, link) VALUES('%s','%s','%s','%s','%s','%s');" %(id, normalize(info["title"]), time, info["province"], normalize(content_str), normalize(info["link"]))
    cursor.execute(sql)
    conn.commit()


def get_news_titles(conn, entry, a_province):
    req = urllib.urlopen(entry)
    html = req.read().decode("gb2312").encode("utf-8")
    pre_sel, pnext = get_substring(html, "<sohu_cms_include:sohu_localnews_list>", "</sohu_cms_include", 0)
    L = []
    plast = 0
    while True:
        sel1, pnext = get_substring(pre_sel, "<li>", "</li>", plast)
        if pnext == -1:
            break
        the_link, pnext2 = get_substring(sel1, "<a href=\"", "\"", 0)
        if pnext == -1:
            break
        the_title, pnext2 = get_substring(sel1, ">", "<", pnext2)
        if sel1 != "" and the_link != "" and the_title != "":
            L.append({"province": a_province, "link": the_link, "title": the_title})
        plast = pnext
    for element in L:
        save_news_content(conn, element)


def main():
    parser = CSVParser("./webmapping2.csv")
    parser.parse()
    result_set = parser.get_element(1, 10, 0, 2)
    conn = open_database_connection()
    for data in result_set:
        try:
            get_news_titles(conn, "http://news.sohu.com" + "/" + data[1].replace("\n", "") + ".shtml", data[0])
        except Exception as e:
            continue
    s = Searcher("./index")
    s.update_index()

main()