# -*- coding: utf-8 -*-
# 一天计数一次
from urllib.parse import quote, unquote
import datetime


import time

import requests
from bs4 import BeautifulSoup
# import urllib.request

from html import unescape
import re

from notificationTool import notificationTool

wechat_Header = {
            # "accept": "*/*",
            # "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            # "cache-control": "no-cache",
            # "pragma": "no-cache",
            # "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            # "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": "\"Windows\"",
            # "sec-fetch-dest": "empty",
            # "sec-fetch-mode": "cors",
            # "sec-fetch-site": "same-origin",


            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }

hellogithub_header = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "Bearer null",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://hellogithub.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

class weChat_listening:
    
    def extract_notice_with_bs4(self,html_content):
    
      # 创建BeautifulSoup对象，指定解析器
      soup = BeautifulSoup(html_content, 'html.parser')
      
      # 第一步：提取script标签中window.wxCgi对象的内容（核心数据存储在这里）
      notice_data = {}
      # 遍历所有script标签，找到包含window.wxCgi的标签
      for script in soup.find_all('script'):
          script_text = script.string
          if script_text and 'window.wxCgi = {' in script_text:
              # 提取window.wxCgi对象的内容
              cgi_start = script_text.find('window.wxCgi = {') + len('window.wxCgi = {')
              cgi_end = script_text.find('}', cgi_start)
              cgi_content = script_text[cgi_start:cgi_end].strip()
              
              # 解析标题
              title_match = re.search(r'title:"(.*?)",', cgi_content)
              notice_data['title'] = title_match.group(1) if title_match else '未找到标题'
              
              # 解析内容
              content_match = re.search(r'content:"(.*?)",\s*author:', cgi_content)
              if content_match:
                  # 处理HTML转义字符，清理标签
                  raw_content = unescape(content_match.group(1))
                  # 替换br标签为换行，移除其他HTML标签
                  # raw_content = re.sub(r'<br\s*\/?\s*>', '\n', raw_content)
                  # raw_content = re.sub(r'<[^>]+>', '', raw_content)
                  notice_data['content'] = raw_content
              else:
                  notice_data['content'] = '未找到内容'
              
              # 解析发布时间戳并格式化
              time_match = re.search(r'online_time:"(\d+)"', cgi_content)
              if time_match:
                  timestamp = int(time_match.group(1))
                  publish_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y年%m月%d日")
                  notice_data['publish_time'] = publish_time
              else:
                  notice_data['publish_time'] = '未找到发布时间'
              
              break  # 找到目标script后退出循环
      
      # 第二步（备选）：从页面DOM中提取标题（兜底方案）
      if notice_data.get('title') == '未找到标题':
          title_elem = soup.find('h3', class_='announcement_title')
          if title_elem:
              notice_data['title'] = title_elem.get_text(strip=True)
      
      return notice_data
    
    def extract_notice_with_url(self, url):
        responseValue = requests.get(url=url,headers=wechat_Header)
        if responseValue.status_code == 200:
          # 提取通知信息
          notice_info = self.extract_notice_with_bs4(responseValue.text)
          content = '<h3>{}</h3>{}'.format(notice_info['title'],notice_info['content'])
          # print(notice_info['content'])
          notificationTool().main(titleMsg="微信公众号系统公告", message=content)



    def requestURL(self):
        wechat_URL = 'https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncementlist&lang=zh_CN'
        
        responseValue = requests.get(url=wechat_URL,headers=wechat_Header)
        # print(responseValue.text)
        beautifulSoup = BeautifulSoup(responseValue.text, 'html.parser')
        resultStrring = beautifulSoup.find('li', class_ = 'mp_news_item')
        
        item_title = resultStrring.select('strong')[0].get_text()
        item_time = resultStrring.select('span')[0].get_text()
        yes_time = self.timeTransform()

        
        item_href = resultStrring.select('a')[0]['href']

        if item_time in str(yes_time) and len(item_href) >=10:
            time.sleep(3)
            self.extract_notice_with_url('https://mp.weixin.qq.com{}'.format(item_href))
            # notification_Model.notificationWeChatToken(notification_Model,"微信公众号系统公告", item_title)

    def timeTransform(self):
        today = datetime.date.today()
        # 3.计算昨天的日期
        yesterday = today - datetime.timedelta(days=1)
        return yesterday


class hellogithub_rss:
    def getHelloGithub(self):
        url = 'https://api.hellogithub.com/v1/periodical/' 
        responseValue = requests.get(url=url,headers=hellogithub_header)
        res = responseValue.json()
        
        if res['success'] == True and responseValue.status_code == 200:
            currentData = res['volumes'][0]
            if self.time_diff(currentData['lastmod']) :
                print('更新')
                time.sleep(5)
                notificationTool().main(titleMsg='HelloGitHub 月刊更新', message='https://hellogithub.com/periodical/volume/118')
        
    
    def time_diff(self,dateContent):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        if current_date in dateContent:
            return True
        else:
            return False
        

class dayNote:
   
    def calculateTimeDifference(self, year_const, month_const,day_const):
        # 初始日期
        entry_date = datetime.date(year_const, month_const, day_const)
        # 强制使用北京时间获取今日日期，避免系统时区差异导致误差
        try:
            from zoneinfo import ZoneInfo
            today = datetime.datetime.now(ZoneInfo("Asia/Shanghai")).date()
        except (ImportError, ModuleNotFoundError, Exception):
            # Windows系统找不到时区时直接使用本地系统时间，Windows时区设置正确时结果一致
            today = datetime.date.today()
        # today = datetime.datetime.now(ZoneInfo("Asia/Shanghai")).date()

        # 计算初始年月日差值
        years = today.year - entry_date.year
        months = today.month - entry_date.month
        days = today.day - entry_date.day

        # 处理日借位：日不够减时向月借1个月
        if days < 0:
            months -= 1
            # 自动计算上个月总天数（自动兼容大小月、闰年2月）
            if today.month == 1:
                first_day_prev_month = datetime.date(today.year - 1, 12, 1)
            else:
                first_day_prev_month = datetime.date(today.year, today.month - 1, 1)
            prev_month_days = (first_day_prev_month - datetime.timedelta(days=1)).day
            days += prev_month_days

        # 处理月借位：月不够减时向年借1年
        if months < 0:
            years -= 1
            months += 12

        # 打印结果
        # print("=" * 40)
        # print(f"入职日期：{entry_date.strftime('%Y-%m-%d')}")
        # print(f"计算日期：{today.strftime('%Y-%m-%d')}")
        # print("-" * 40)
        # print(f"累计入职：{years}年{months}个月{days}天")
        # print("=" * 40)

        return f"{years}年{months}个月{days}天"
    
    def main(self):
        distanceTitle = self.calculateTimeDifference(2024,5,16)
        distanceContent = self.calculateTimeDifference(2022,4,6)
        # print(f"distanceTitle====:{distanceTitle}, distanceContent====:{distanceContent}")
        
        notificationTool().main(titleMsg=f"尤一已经{distanceTitle}", message=f"入职已经{distanceContent}")



def handler():
    # dayNote().jobTime()
    dayNote().main()
    # weChat_listening().requestURL()
  

if __name__ == '__main__':
    handler()
    # hellogithub_rss().getHelloGithub()
    