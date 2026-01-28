# -*- coding: utf-8 -*-
import datetime
import requests
from notificationTool import notificationTool



# 获取当前日期和时间
now = datetime.datetime.now()

# 提取年月日时分秒
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute
second = now.second
timeINvalue = 'dreamskywwl.github.io: {}-{}-{} {}:{}:{}'.format(year,month,day,hour,minute,second)
print(timeINvalue)
notificationTool().main(titleMsg='更新时间', message=timeINvalue)