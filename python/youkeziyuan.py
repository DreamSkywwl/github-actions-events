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

defaultRepeatCount = 0



# -------------------类------------------------

class youkeziyuan:
      
    # 初始化---->
    def run(self):
        # 初始化全局变量
        global defaultContent
        defaultContent = '' #
        global defaultTotalPages
        defaultTotalPages = 3

        global defaultRepeatCount
        defaultRepeatCount = 0



        defaultFile = 'xuehaiziyuan.txt'
        
        print(f"defaultFile====:{defaultFile}")
        
        global defaultNetContent
        defaultNetContent = FileTracker().getContent(defaultFile)
        # self.log(f"defaultNetContent====: {defaultNetContent}")
        self.test_xuehaiziyuan()
        self.log(f'一共{defaultTotalPages}页')

        for index in range(defaultTotalPages):
            # 临时解锁一下
            if defaultRepeatCount >= 3:
               break
            time.sleep(10)
            self.log(f"正在解析第{index+1}页")
            self.getMainHtml(index + 1)

        arrContent = defaultContent.split(' |a|a| ')
        printContent = []
        if len(arrContent) == 0:
           print('arrContent======数据为空')
        else:
          # self.log(arrContent)
          for item in arrContent:
            if item not in defaultNetContent:
                defaultNetContent = f"{defaultNetContent}\n{item}"
                printContent.append(item)
          
          self.writeContent(printContent)
          # print(f"save to last defaultNetContent====:{defaultNetContent}")
          FileTracker().saveContent(defaultFile, defaultNetContent)


    #  获取数据内容
    def getContent(self, content):
        return content in defaultNetContent
    #  写入内容
    def writeContent(self, content):
        if len(content) == 0:
           self.log("writeContent content empty 无法消息通知")
           return
        if len(content) >= 15:
           self.log("writeContent content empty 网盘分享内容更新太多")
           return
        arr = []
        for item in content:
           arrStr = item.split(',')
           if len(arrStr) >= 2:
              arr.append(f"标题：{arrStr[0]} \n网盘地址：{arrStr[len(arrStr) - 1]}\n=========我是分割线=========\n")

        str = '\n'.join(arr)
        print(f"writeContent str====:{str}")
        
        notificationTool().main(titleMsg='网盘分享内容更新', message=str)


      
    # 获取网页内容
    def test_xuehaiziyuan(self):
      content = ''
      if defaultTest:
         content = self.testHtml()
      else:
        url = 'http://www.youkeziyuan.com/?page=1'
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "upgrade-insecure-requests": "1",
            "cookie": "__51cke__=; timezone=8; __tins__21995819=%7B%22sid%22%3A%201768876943491%2C%20%22vd%22%3A%2039%2C%20%22expires%22%3A%201768880497282%7D; __51laig__=39",
            "Referer": "http://www.youkeziyuan.com/page_11.html",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        html_content = requests.get(headers=headers,url=url)
        content = html_content.text
      self.getTotalPage(content)

    # 获取网页内容
    def getMainHtml(self,index):
      content = ''
      if defaultTest:
         self.log(f'getMainHtml测试')
         content = self.testHtml()
      else:
        url = f'http://www.youkeziyuan.com/page_{index}/'
        if index == 1:
          url = 'http://www.youkeziyuan.com/?page=1'
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "upgrade-insecure-requests": "1",
            "cookie": "__51cke__=; timezone=8; __tins__21995819=%7B%22sid%22%3A%201768876943491%2C%20%22vd%22%3A%2039%2C%20%22expires%22%3A%201768880497282%7D; __51laig__=39",
            "Referer": "http://www.youkeziyuan.com/page_11.html",
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
          # tzt-media-box_title
          title_elements = product.xpath('.//h3[@class="tzt-media-box_title"]/text()')
          title = title_elements[0].strip() if title_elements else "未找到标题"
          # if title in defaultContent and title not in '未找到标题':
          if self.getContent(title) or title in '未找到标题' :
            global defaultRepeatCount
            defaultRepeatCount += 1
            self.log(f"忽略 title====:{title}")
          else:
            link = product.get('href', "未找到链接")
            timeArr = product.xpath('.//div[@class="tzt-media-box_time"]/text()')

            productTag = ''
            productTime = ''
            if len(timeArr) == 2:
              productTag = timeArr[0]
              productTime = timeArr[1]
            lastContent = ','.join([title,link, productTag,productTime])
            if not self.getContent(lastContent):
              self.getHtmlNext(link, lastContent)
              # self.log('sleep 3s')
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
          "Referer": "http://www.youkeziyuan.com/page_11.html",
          "Referrer-Policy": "strict-origin-when-cross-origin"
      }

      html_content = requests.get(headers=headers,url=url)
      
      
      self.log(f'执行下一步网页：{url} 接口返回：{html_content.status_code}')
      self.nextPageDetail(html_content.text, message)


    def nextPageDetail(self,content, saveMessage):
      # self.log(f"XPath解析:nextPageDetail:{content}")
      tree = html.fromstring(content)
      lists = tree.xpath('.//div[@id="viewer"]/p')
      for idx, listItem in enumerate(lists, 1):
        linkKeyWord = listItem.xpath('.//span/text()')
        link = listItem.xpath('.//a/text()')
        # xuehaiziyuan====:详情页   linkKeyWord：['https://pan.quark.cn/s/2700ecfb78a4']--------link[]
        self.log(f"详情页   linkKeyWord：{linkKeyWord}--------link{link}")
        # status = len(linkKeyWord) >= 1 and len(link) >= 1 and 'https://' in link[0].strip() and '链接' in linkKeyWord[0].strip()
        status = len(linkKeyWord) >= 1 and (any('https://pan.quark.cn' in element for element in linkKeyWord))
        
        if status == True:
          linkValue = linkKeyWord[0].strip()
          if len(linkKeyWord) >= 2 and 'https://pan.quark.cn' in linkKeyWord[1].strip():
             linkValue = linkKeyWord[1].strip()
          self.log(f"详情页网盘链接地址：{linkValue}")
          newMessage = ','.join([saveMessage, linkValue])
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
          print(f"xuehaiziyuan====:{content}")
       else:
          print(f"xuehaiziyuan====:{content}")
        



youkeziyuan().run()


# https://github.com/DreamSkywwl/github-actions-events/actions/workflows/sharePan-python.yml