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
        print()
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
    def main(self):
        # 获取当前日期
        today = datetime.datetime.now().date()

        # 定义起始日期
        start_date = datetime.datetime(2024, 5, 16).date()

        # 计算天数差
        delta = today - start_date
        total_days = delta.days

        # 计算年数和月数
        years = today.year - start_date.year
        months = today.month - start_date.month

        # 调整负数月份
        if months < 0:
            years -= 1
            months += 12

        # 如果结束日期的天数小于开始日期的天数，则减去一个月
        if today.day < start_date.day:
            months -= 1
            if months < 0:
                years -= 1
                months += 12

        print(f"从2024年5月16日到今天({today})")
        print(f"相差 {total_days} 天")
        print(f"一共 {years} 年 {months} 个月")
        content = f"<p><span style=\"font-size: 18px;\">从2024年5月16日到今天<strong>{today}</strong>天</span></p><p><span style=\"color:#ce9178\"><span style=\"color: rgb(0, 0, 0); font-size: 18px;\">尤一已经</span></span><span style=\"color:#ce9178\"><span style=\"font-size: 18px; text-decoration: underline; color: rgb(192, 80, 77);\"><em><strong>{years}.{months}</strong></em></span></span><span style=\"color:#ce9178\"><span style=\"color: rgb(0, 0, 0); font-size: 18px;\">岁了</span></span></p><p><br/></p>"

        notificationTool().main(titleMsg='尤一已经{}.{}岁'.format(years,months), message=content)

def handler():
    """ 
    d1 = datetime.datetime.now();
    d2 = datetime.datetime(2021, 2, 17);
    d3 = datetime.datetime(2024, 5, 16);
    d4 = (d1 - d2).days + 1; # 在一起多久
    d5 = (d1 - d3).days + 1; # 孩子已经多少天
    msg = 'Tips: 认识晓粉已经' + str(d4) + '天'
    msg2 = 'Tips: 孩子已经' + str(d5) + '天'
    print(msg)
    notificationTool().main(titleMsg='宝宝' + str(d5) + '天', message=msg + '<br />\n' + msg2) 
    """
    dayNote().main()
    weChat_listening().requestURL()
  

if __name__ == '__main__':
    handler()
    # hellogithub_rss().getHelloGithub()
    