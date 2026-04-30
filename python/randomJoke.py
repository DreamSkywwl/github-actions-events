# -*- coding: utf-8 -*-

import os
from lxml import html

from notificationTool import notificationTool 
from toolsNetWork import safe_request

def testHtml():
      address = r'D:\\Code\\github-actions-events\\test\\Tmp_third.html'
      content = ''
        # 判断文件是否存在，如果不存在则创建
      if not os.path.exists(address):
          with open(address, 'w', encoding='utf-8') as f:
              print('write-----')
              f.write('')
      
      # 读取文件内容
      with open(address, 'r',encoding='utf-8') as f:
          print('read-----')
          content = f.read()
      # self.log(f'content:{content}')
      return content

def asyncContent(content):
  tree = html.fromstring(content)
  target_div_xpath = tree.xpath('//span[@id="duanzi-text"]/text()')
  resultValue = '\n'.join(target_div_xpath).replace('yduanzi.com', '')
  return resultValue

if __name__ == '__main__':
  url = 'https://www.yduanzi.com/'
  headers = {
              "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
              "accept-language": "zh-CN,zh;q=0.9",
              "cache-control": "no-cache",
              "pragma": "no-cache",
              "upgrade-insecure-requests": "1",
              "cookie": "__51cke__=; timezone=8; __tins__21995819=%7B%22sid%22%3A%201768876943491%2C%20%22vd%22%3A%2039%2C%20%22expires%22%3A%201768880497282%7D; __51laig__=39",
              "Referer": url,
              "Referrer-Policy": "strict-origin-when-cross-origin"
          }
  content = safe_request(url=url,type='text', headers=headers)

  result = asyncContent(content)

  notificationTool().main(titleMsg='Joke', message=result)
