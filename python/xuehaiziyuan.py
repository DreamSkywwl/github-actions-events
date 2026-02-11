# -*- coding: utf-8 -*-
from lxml import html
import requests
import os
import time
from notificationTool import notificationTool 
from toolsSaveFile import FileTracker


# https://github.com/DreamSkywwl/github-actions-events/actions/workflows/sharePan-python.yml


# -------------------常量------------------------
defaultContent = '' # 初始数据
defaultNetContent = '' # 初始数据
defaultTotalPages = 12 # 总页码初始化值
defaultIndex = 1  # 页码初始化值

defaultTest = False


defaultFile = 'xuehaiziyuan.txt'

# -------------------类------------------------

class xuehaiziyuan:
      
    # 初始化---->
    def run(self):
        global defaultContent
        defaultContent = '' #
        global defaultTotalPages
        defaultTotalPages = 12
        
        
        print(f"xuehaiziyuan defaultFile====:{defaultFile}")
        # global defaultFile
        # defaultFile = 'xuehaiziyuan.txt'
        global defaultNetContent
        defaultNetContent = FileTracker().getContent(defaultFile)
        self.test_xuehaiziyuan()
        self.log(f'一共{defaultTotalPages}页')

        if defaultTest:
           defaultTotalPages = 1

        for index in range(defaultTotalPages):
            time.sleep(10)
            self.getMainHtml(index + 1)

        arrContent = defaultContent.split(' |a|a| ')
        if len(arrContent) == 0:
           print('arrContent======数据为空')
        else:
          self.log(arrContent)
          for item in arrContent:
            if item not in defaultNetContent:
                defaultNetContent = f"{defaultNetContent}\n{item}"
          
          self.writeContent(arrContent)
          FileTracker().saveContent(defaultFile, defaultNetContent)


        

    #  获取数据内容
    def getContent(self, contentFile):
        return contentFile not in defaultNetContent
    #  写入内容
    def writeContent(self, content):
        self.log(f'aaa:{content}')
        arr = []
        for item in content:
           arrStr = item.split(',')
           if len(arrStr) >= 2:
              arr.append(f"标题：{arrStr[0]} \n网盘地址：{arrStr[len(arrStr) - 1]}\n=========我是分割线=========\n")

        
        str = '\n'.join(arr)
        
        notificationTool().main(titleMsg='网盘分享内容更新', message=str)


        
    
   
    # 获取网页内容
    def test_xuehaiziyuan(self):
      content = ''
      if defaultTest:
         content = self.testHtml()
      else:
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
        content = html_content.text
      self.getTotalPage(content)

    # 获取网页内容
    def getMainHtml(self,index):
      content = ''
      if defaultTest:
         self.log(f'正在解析{index}页')
         content = self.testHtml()
      else:
        url = f'http://www.xuehaiziyuan.com/page_{index}.html'
        if index == 1:
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
        content = html_content.text
      self.analysisHtml(content)

    # 解析网页内容
    def analysisHtml(self,content):
      tree = html.fromstring(content)
      # 方法1：使用XPath提取列表项
      products = tree.xpath('//a[@class="tzt-media-box"]')
      for idx, product in enumerate(products, 1):
          title_elements = product.xpath('.//h3[@class="tzt-media-box_title"]/text()')
          title = title_elements[0].strip() if title_elements else "未找到标题"
          # if title in defaultContent and title not in '未找到标题':
          if self.getContent(title) and title not in '未找到标题':
             self.log(f"title====:{title}")
             break
          link = product.get('href', "未找到链接")
          timeArr = product.xpath('.//div[@class="tzt-media-box_time"]/text()')

          productTag = ''
          productTime = ''
          if len(timeArr) == 2:
            productTag = timeArr[0]
            productTime = timeArr[1]
          lastContent = ','.join([title,link, productTag,productTime])
          if self.getContent(lastContent):
            self.getHtmlNext(link, lastContent)
            self.log('sleep 3s')
            time.sleep(3)
            
          
    # 获取默认页码
    def getTotalPage(self,content):
      tree = html.fromstring(content)
      lists = tree.xpath('//ul[@class="tzt-pagination"]/li')
      endLists = lists[len(lists) - 1].xpath('./a/text()')
      if len(endLists) >= 1:
        endPage = endLists[0].strip().replace('共','').replace('页','')
        global defaultTotalPages
        defaultTotalPages = int(endPage)


    # 获取网页内容
    def getHtmlNext(self,url,message):
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
      
      
      self.log('执行下一步网页：',html_content.status_code)
      self.nextPageDetail(html_content.text, message)


    def nextPageDetail(self,content, saveMessage):
      self.log("XPath解析:nextPageDetail")
      tree = html.fromstring(content)
      lists = tree.xpath('.//div[@id="viewer"]/p')
      for idx, listItem in enumerate(lists, 1):
        linkKeyWord = listItem.xpath('.//span/text()')
        link = listItem.xpath('.//a/text()')
        
        status = len(linkKeyWord) >= 1 and len(link) >= 1 and 'https://' in link[0].strip() and '链接' in linkKeyWord[0].strip()
        
        if status == True:
          newMessage = ','.join([saveMessage, link[0]])
          global defaultContent
          defaultContent = f"{defaultContent} |a|a| {newMessage}"
          break

    def testHtml(self):
      address = r'D:\Code\github-actions-events\test\Tmp_first.html'
      content = ''
        # 判断文件是否存在，如果不存在则创建
      if not os.path.exists(address):
          with open(address, 'w', encoding='utf-8') as f:
              f.write('')
      
      # 读取文件内容
      with open(address, 'r',encoding='utf-8') as f:
          content = f.read()
      # self.log(f'content:{content}')
      return content

    def log(self, content, index = 1):
       if defaultTest and index == 1:
          print(f"run====={content}=====")
       elif defaultTest and index != 1:
          print(f"====:{content}")
        



xuehaiziyuan().run()