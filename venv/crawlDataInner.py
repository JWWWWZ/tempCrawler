# -*- coding: utf-8-*-

import sys

import crawlData

print('初始化数据库中')
crawlData.init()
print('初始化完成...')

print('开始爬取网页...')

# 参数列表 爬取的网址、编码格式、当前页数、总的页数、爬取的网站（1、2、3中的哪一个）
status = crawlData.saveUrlToDb(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
print('爬取网页完成')
