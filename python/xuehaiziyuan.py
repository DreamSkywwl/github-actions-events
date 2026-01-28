# -*- coding: utf-8 -*-
from lxml import html
import requests
import os
import time

initializeData = ''
defaultTotalPages = 12
defaultIndex = 1
defaultFile = r'D:\Code\dreamskyNote\abdc.txt'

class notification_Model:
   
    def notificationWeChatToken(self,titleMsg, message):
        url = "https://push.showdoc.com.cn/server/api/push/303b94dcc4ac08927ccbce0e72ad9fec430211407"
        
        payload = {
            "title": titleMsg,
            "content": message,
            "user_token": "12307831fb70e549bb4d5af466858b64839451758"
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

        response = requests.post(url, headers=headers, data=payload)
        notification_Model().notificationWeChatToken2(titleMsg)
        print(response.text)
    
    def notificationWeChatToken2(self,titleMsg, ):
        
        url = "https://api.letserver.run/message/info?token=cq0mkh8jn87bju92b0ag&msg=" + titleMsg
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.get(url, headers=headers)

        print(response.text)

 

# 在获取列表的时候先判断一下是否还有
def checkFileContent(content):
    # 判断文件是否存在，如果不存在则创建
    if not os.path.exists(defaultFile):
        with open(defaultFile, 'w', encoding='utf-8') as f:
            f.write('')
    
    # 读取文件内容
    with open(defaultFile, 'r',encoding='utf-8') as f:
        file_content = f.read()
    
    # 判断内容是否已存在
    if content in file_content:
       return False
    else:
        return True

def check_and_write(content):
    # 判断文件是否存在，如果不存在则创建
    if not os.path.exists(defaultFile):
        with open(defaultFile, 'w', encoding='utf-8') as f:
            f.write('')
    
    # 读取文件内容
    with open(defaultFile, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    # 判断内容是否已存在
    if content not in file_content:
        global initializeData
        initializeData = initializeData + '|||' + content
        # 如果不存在，则追加写入
        with open(defaultFile, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
        print(f"内容 '{content}' 已添加到文件中。")
    else:
        print(f"内容 '{content}' 已存在于文件中。")

# 获取网页内容
def test_xuehaiziyuan():
  url = 'http://www.xuehaiziyuan.com/?page=1'
  headers = {
      "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
      "accept-language": "zh-CN,zh;q=0.9",
      "cache-control": "no-cache",
      "pragma": "no-cache",
      "upgrade-insecure-requests": "1",
      "cookie": "__51cke__=; timezone=8; __tins__21995819=%7B%22sid%22%3A%201768876943491%2C%20%22vd%22%3A%2039%2C%20%22expires%22%3A%201768880497282%7D; __51laig__=39",
      "Referer": "http://www.xuehaiziyuan.com/page_11.html",
      "Referrer-Policy": "strict-origin-when-cross-origin"
  }
  html_content = requests.get(headers=headers,url=url)
  # print(html_content.status_code, html_content.text)
  getTotalPage(html_content.text)

# 获取网页内容
def xuehaiziyuan(index):
  url = 'http://www.xuehaiziyuan.com/?page=' + str(index)
  headers = {
      "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
      "accept-language": "zh-CN,zh;q=0.9",
      "cache-control": "no-cache",
      "pragma": "no-cache",
      "upgrade-insecure-requests": "1",
      "cookie": "__51cke__=; timezone=8; __tins__21995819=%7B%22sid%22%3A%201768876943491%2C%20%22vd%22%3A%2039%2C%20%22expires%22%3A%201768880497282%7D; __51laig__=39",
      "Referer": "http://www.xuehaiziyuan.com/page_11.html",
      "Referrer-Policy": "strict-origin-when-cross-origin"
  }
  html_content = requests.get(headers=headers,url=url)
  analysisHtml(content=html_content.text)

# 解析网页内容
def analysisHtml(content):
  tree = html.fromstring(content)
  # 方法1：使用XPath提取列表项
  print("=== XPath解析 ===")
  products = tree.xpath('//a[@class="tzt-media-box"]')
  for idx, product in enumerate(products, 1):
      title_elements = product.xpath('.//h3[@class="tzt-media-box_title"]/text()')
      title = title_elements[0].strip() if title_elements else "未找到标题"
      link = product.get('href', "未找到链接")
      timeArr = product.xpath('.//div[@class="tzt-media-box_time"]/text()')

      productTag = ''
      productTime = ''
      if len(timeArr) == 2:
        productTag = timeArr[0]
        productTime = timeArr[1]
      # print(title,link, productTag,productTime)
      lastContent = ','.join([title,link, productTag,productTime])
      print("=== XPath解析结果: ===",lastContent, checkFileContent(lastContent))
      if checkFileContent(lastContent):
         print('执行下一步')
         getHtmlNext(link, lastContent)
         time.sleep(3)
         
      

# 获取默认页码
def getTotalPage(content):
   tree = html.fromstring(content)
   lists = tree.xpath('//ul[@class="tzt-pagination"]/li')
   print(len(lists))
   endLists = lists[len(lists) - 1].xpath('./a/text()')
   if len(endLists) >= 1:
    endPage = endLists[0].strip().replace('共','').replace('页','')
    print(endPage)
    defaultTotalPages = int(endPage)


# 获取网页内容
def getHtmlNext(url,message):
  headers = {
      "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
      "accept-language": "zh-CN,zh;q=0.9",
      "cache-control": "no-cache",
      "pragma": "no-cache",
      "upgrade-insecure-requests": "1",
      "cookie": "__51cke__=; timezone=8; __tins__21995819=%7B%22sid%22%3A%201768876943491%2C%20%22vd%22%3A%2039%2C%20%22expires%22%3A%201768880497282%7D; __51laig__=39",
      "Referer": "http://www.xuehaiziyuan.com/page_11.html",
      "Referrer-Policy": "strict-origin-when-cross-origin"
  }
  html_content = requests.get(headers=headers,url=url)
  print('执行下一步网页：',html_content.status_code)
  nextPageDetail(html_content.text, message)


def nextPageDetail(content, saveMessage):
   print("=== XPath解析: ===nextPageDetail")
   tree = html.fromstring(content)
   lists = tree.xpath('.//div[@id="viewer"]/p')
   for idx, listItem in enumerate(lists, 1):
    linkKeyWord = listItem.xpath('.//span/text()')
    link = listItem.xpath('.//a/text()')
    # print(endLists,link)
    status = len(linkKeyWord) >= 1 and len(link) >= 1 and 'https://' in link[0].strip() and '链接' in linkKeyWord[0].strip()
    # 循环状态： False ['链接：'] ['https://pan.quark.cn/s/a8683fb7b005']
    # print('循环状态：',status,linkKeyWord,link)
    if status == True:
       newMessage = ','.join([saveMessage, link[0]])
       check_and_write(newMessage)
       break
    


def run():
   initializeData = ''
   defaultTotalPages = 12
   test_xuehaiziyuan()
    #  休眠一下
   time.sleep(1)

   xuehaiziyuan(1)


run()

time.sleep(1)
print('initializeData', initializeData)

if len(initializeData) >=1:
   arr = initializeData.split('|||')
   arrContent = []
   for item in arr :
      arrNext = item.split(',')
      arrContent.append('<br />'.join(arrNext))
      arrContent.append('=====分割线=====')
   contentMessage = '<br />'.join(arrContent)
   notification_Model.notificationWeChatToken(notification_Model, '网盘资源更新',contentMessage)
 










'''
# 示例HTML（包含列表）
html_content = """
<html>
    <body>
        <h1>商品列表</h1>
        <ul id="product-list">
            <li class="product">商品A <span class="price">¥100</span></li>
            <li class="product">商品B <span class="price">¥200</span></li>
            <li class="product">商品C <span class="price">¥300</span></li>
        </ul>
    </body>
</html>
"""

# 解析HTML
tree = html.fromstring(html_content)

# 方法1：使用XPath提取列表项
print("=== XPath解析 ===")
products = tree.xpath('//ul[@id="product-list"]/li')
for idx, product in enumerate(products, 1):
    name = product.xpath('./text()')[0].strip()
    price = product.xpath('./span[@class="price"]/text()')[0]
    print(f"{idx}. {name} - 价格: {price}")

'''

'''
fetch("http://www.xuehaiziyuan.com/?page=1", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "upgrade-insecure-requests": "1",
    "cookie": "__51cke__=; timezone=8; __tins__21995819=%7B%22sid%22%3A%201768876943491%2C%20%22vd%22%3A%2039%2C%20%22expires%22%3A%201768880497282%7D; __51laig__=39",
    "Referer": "http://www.xuehaiziyuan.com/page_11.html",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": null,
  "method": "GET"
});
'''