# -*- coding: utf-8 -*-
# 一小时计数一次

import os 
from os.path import join, getsize 
import pip
import requests
import json
from urllib.parse import quote, unquote
import feedparser
import time
from datetime import datetime
from bs4 import BeautifulSoup
import pytz
from notificationTool import notificationTool
from time_tracker import TimeTracker

timeMaxLine = 3600

class fuliba:  
    def netWork(self):
        url = 'https://fuliba2023.net/feed'
        feed = feedparser.parse(url)
        arrContent = []
        for entry in feed['entries']:
            # print(entry.keys())
            oneTime = entry['published']
            if self.transformTime(oneTime):
                arrContent.append(entry['title'] + '-----: ' + entry['link'])
            else:
                print(entry['title'] + ' -----:' + entry['link'] + ' -----' + oneTime)

        return arrContent

    def transformTime(self,oneTime):
        # 解析目标时间
        target_time = datetime.strptime(oneTime, "%a, %d %b %Y %H:%M:%S %z")
        
        # 设置目标时区为上海
        target_time = target_time.astimezone(pytz.timezone('Asia/Shanghai'))
        
        # 获取当前时间（上海时区）
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        
        # 计算时间差
        time_diff = now - target_time
        # print('time_diff:',time_diff,sep='--------')
        print("time_diff:{} | target_time:{} | now:{}".format(time_diff.total_seconds(),target_time,now))
        return time_diff.total_seconds() <= timeMaxLine        
    

class juejin:
    def loadData(self,uuid):
        urlValueJueJin ='https://api.juejin.cn/content_api/v1/article/query_list?aid=2608&uuid=7351316729601197608&spider=0'
        headers = {
            'accept':'*/*',
            "Content-Type": "application/json",
            'accept-language':'zh-CN,zh;q=0.9',
            'content-type':'application/json',
            'origin':'https://juejin.cn',
            'priority':'u=1, i',
            'referer':'https://juejin.cn/',
            'sec-ch-ua':'"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-site',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'x-secsdk-csrf-token':'0001000000018142c0fe5e0687deb4fef31b493dcc253134c075f09cf887ff59ff118343d78c188814669520f224',
        }
        data = {"user_id":uuid,"sort_type":2,"cursor":"0"}
        requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        s = requests.session()
        s.keep_alive = False # 关闭多余连接
        respose = s.post(url=urlValueJueJin,headers=headers,data=json.dumps(data))
        resultData = respose.json()
        
        # print('resultData:', resultData)
        
        arrContent = []
        if resultData['err_no'] == 0 and resultData['err_msg'] == 'success':
            firstData = resultData['data']
            for item in firstData:
                itemID = item['article_id']
                titleValue = item['article_info']['title']
                brief_content = item['article_info']['brief_content']
                cover_image = item['article_info']['cover_image']
                ctime = item['article_info']['mtime']
                
                if ctime == None:
                    ctime = item['article_info']['ctime']
                createTime = self.transformTime(ctime)
                
                if createTime:
                  arrContent.append(titleValue + '-----:' + 'https://juejin.cn/post/' + str(itemID))
                    
        
        return arrContent

    def transformTime(self,timeString):
        py = pytz.timezone('Asia/Shanghai')
        old_time = datetime.fromtimestamp(float(timeString), py)
        now_time = datetime.now(py)
        totleTime = (now_time - old_time)
        print("timeString:{}--old_time:{}--total_seconds:{}".format(timeString,old_time,totleTime.total_seconds()))
        if totleTime.total_seconds() <= timeMaxLine:
            return True
        else:
            return False

      
class result_model:
    def total_func():
        arrOne = []
        arrOne = fuliba().netWork()
        arr_uuids = ['1574156384091320', '3483683111318823', '2946346894759319', '53218623894222','1139531179102392','1063982986187486','3298190611978526']
        
        arrSecond = []
        for item in arr_uuids:
            arrThird = juejin().loadData(item)
            arrSecond.extend(arrThird)
            time.sleep(2)
        title = '文章更新汇总'
        
        if len(arrOne) == 0:
            title = '掘金文章更新'
        if len(arrSecond) == 0:
            title = '知乎文章更新'
        arrLast = arrOne+arrSecond
        content = '\n'.join(arrLast)

        if len(arrLast) != 0:
            notificationTool().main(title, content)
                      
def main_handler():
  timeMaxLine = TimeTracker.main(filename='dayToHour_actions')
  if not timeMaxLine:
      timeMaxLine = 3600
  result_model.total_func()
    
    
if __name__ == '__main__':
    # print('触发__name__')
    main_handler()
    

