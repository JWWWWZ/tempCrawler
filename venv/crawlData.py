# -*- coding: utf-8-*-

import requests
import sqlite3
from bs4 import BeautifulSoup

import constants


def init():
    conn = sqlite3.connect(constants.database)
    sql = 'CREATE TABLE IF NOT EXISTS ' + constants.tablename + ' ("ID" INTEGER,"URL" TEXT,"TITLE" TEXT,"STATUS" INTEGER DEFAULT 0,"LOG" TEXT,PRIMARY KEY ("ID"));'
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()


def saveUrlToDb(crawlurl, code, currpage, totalpage, curr_website):

    try:
        count = 1
        conn = sqlite3.connect(constants.database)
        for num in range(int(currpage), int(totalpage) + 1):

            if(int(curr_website) == 1):
                domain = "http://www.sc.gov.cn"
                if (num == 1):
                    target = crawlurl
                else:
                    filepath = crawlurl[0:crawlurl.rindex('/')]
                    target = filepath + "/index_" + str(num) + ".shtml"
                req = requests.get(url=target)
                html = req.text.encode(req.encoding).decode(code)
                bf = BeautifulSoup(html, 'html.parser')
                texts = bf.find_all('span')

                print("第" + str(num) + "页数据-----------------------------")
                for each in texts:
                    titleAndUrlInfo = each.find_all('a')
                    if len(titleAndUrlInfo) > 0:
                        url = domain + titleAndUrlInfo[0].get('href')
                        title = titleAndUrlInfo[0].text
                        print(count, '、标题：', title, '链接地址：', url)
                        count = count + 1
                        cursor = conn.cursor()
                        cursor.execute('insert into ' + constants.tablename + '(URL, TITLE) values (\'' + url + '\',\'' + title + '\')')
                        cursor.close()

            elif(int(curr_website) == 2):
                filepath = crawlurl[0:crawlurl.rindex('/')]
                if (num == 1):
                    target = crawlurl
                else:
                    target = filepath + "/index_" + str(num) + ".html"
                req = requests.get(url=target)
                html = req.text.encode(req.encoding).decode(code)
                bf = BeautifulSoup(html, 'html.parser')
                texts = bf.find('div', attrs={'class': 'zx-wdsyw-con'}).find_all('li')
                count = 1
                print("第" + str(num) + "页数据-----------------------------")
                for each in texts:
                    titleAndUrlInfo = each.find_all('a')[0]
                    href = titleAndUrlInfo.get('href')
                    if str(href).startswith('.'):
                        href = str(href)[1:len(href)]
                    if len(titleAndUrlInfo) > 0:
                        url = filepath + href
                        title = titleAndUrlInfo.text
                        print(count, '、标题：', title, '链接地址：', url)
                        count = count + 1
                        cursor = conn.cursor()
                        cursor.execute('insert into ' + constants.tablename + '(URL, TITLE) values (\'' + url + '\',\'' + title + '\')')
                        cursor.close()

            elif(int(curr_website) == 3):
                if (num == 1):
                    target = crawlurl
                else:
                    filepath = crawlurl[0:crawlurl.rindex('/')]
                    target = filepath + "/" + str(num) + ".htm"
                req = requests.get(url=target)
                html = req.text.encode(req.encoding).decode(code)
                bf = BeautifulSoup(html, 'html.parser')
                texts = bf.find('div', attrs={'class': 'list list_1 list_2'}).find_all('li')
                count = 1
                print("第" + str(num) + "页数据-----------------------------")
                for each in texts:
                    titleAndUrlInfo = each.find_all('a')[0]
                    href = titleAndUrlInfo.get('href')
                    if str(href).startswith('.'):
                        href = str(href)[1:len(href)]
                    if len(titleAndUrlInfo) > 0:
                        url = href
                        title = titleAndUrlInfo.text
                        print(count, '、标题：', title, '链接地址：', url)
                        count = count + 1
                        cursor = conn.cursor()
                        cursor.execute('insert into ' + constants.tablename + '(URL, TITLE) values (\'' + url + '\',\'' + title + '\')')
                        cursor.close()
    except:
        return constants.failure
    finally:
        conn.commit()
        conn.close()


