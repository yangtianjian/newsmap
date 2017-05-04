# -*- coding:utf-8 -*-

from selenium import webdriver
from csv_parser import CSVParser
import urllib
import re


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
    pContentEnd = pFind


    pContent = source.find("<div class=\"article-body main-body\">", pTitleEnd)
    while True:
        pParagraph = source.find("<p>", pContent)
        if pParagraph == -1 or pParagraph > pContentEnd:
            break
        pParagraphEnd = source.find("</p>", pParagraph)
        assert pContentEnd != -1
        content += source[pParagraph + len("<p>"): pParagraphEnd]
        pContent = pParagraphEnd + len("</p>")
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


def main():
    parser = CSVParser("./webmapping.csv")
    parser.parse()
    data = parser.get_element(1, 25, 0, 2)
    entry_dict = {}
    l = len(data)
    for i in range(0, l):
        entry_dict[data[i][0]] = ("http://" + data[i][1] + ".sina.com.cn").replace("\r", "").replace("\n", "")

    for province in entry_dict.keys():
        source = urllib.urlopen(entry_dict[province]).read()
        lnews = extract_links(source, entry_dict[province])          # the link of all news
        for lanews in lnews:
            title, content = extract_news_info(lanews)
            date = "2017-5-4"
            #TODO: aquire the date
            prov = province
            write_news_to_file(title, content, date, prov)

main()