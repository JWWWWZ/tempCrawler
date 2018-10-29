# -*- coding: utf-8-*-
import sqlite3

import requests

import constants


def syncData(domain, channelid, cruser):

    try:
        conn = sqlite3.connect(constants.database)

        c = conn.cursor()

        SQL = "SELECT ID, URL, TITLE FROM " + constants.tablename + " WHERE STATUS = 0"

        cursor1 = c.execute(SQL)
        count = 1
        for row in cursor1:

            cursor = conn.cursor()
            id = row[0]
            url = row[1]
            title = row[2]
            print(count, '、标题：', title, '链接地址：', url)
            requestUrl = domain + "/gov/opendata.do?serviceid=gov_webdocument&methodname=saveDocumentInWeb&ChannelId=" + channelid + "&ObjectId=0&RecId=&DOCID=0&DocType=30&DOCTITLE=" + title + "&DOCHTMLCON=&DOCCONTENT=&DOCABSTRACT=&SUBDOCTITLE=&DOCAUTHOR=%E6%88%91%E4%BB%AC&DOCKEYWORDS=&DOCRELTIME=2018-10-18%2018%3A01&DOCRELNEWS=%5B%5D&DOCRELPIC=%5B%5D&DOCRELVIDEO=%5B%5D&DOCRELFILE=%5B%5D&OTHERPUBLISH=%5B%5D&NEWSSOURCES=&DOCLINK=" + url + "&LISTSTYLE=&LISTTITLE=&LISTPICS=&LABEL=&ISFOCUSIMAGE=0&FOCUSIMAGE=&DOCCOVERPIC=&COMMENTFLAG=0&READINGMOODFLAG=0&DOCFILE=%5B%5D&DOCPUBTIME=2018-10-19%2018%3A01&DOCSOURCENAME=1015&DetailTemplateId=3724&CurrUserName=" + cruser + ""
            ret = requests.get(requestUrl, verify=False)
            if(ret.status_code == 200):
                print("迁移数据成功")
                updatesql = "UPDATE " + constants.tablename + " SET STATUS = 1 WHERE ID = " + str(id)
                cursor.execute(updatesql)
                cursor.close()
            else:
                print("迁移数据失败")
                updatesql = "UPDATE " + constants.tablename + " SET STATUS = 0 AND LOG = "+ ret.text +" WHERE ID = " + str(id)
                cursor.execute(updatesql)
                cursor.close()

            count = count + 1
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        return constants.failure
    finally:
        cursor1.close()
        conn.commit()
        conn.close()