# -*- coding: utf-8-*-


import sys

import syncDataToHd

print('开始迁移数据到海云中')
# 参数列表 1、访问域名 2、栏目ID 3、操作人
syncDataToHd.syncData(sys.argv[1], sys.argv[2], sys.argv[3])
print('迁移数据完成')