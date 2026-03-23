# -*- coding: utf-8 -*-

# 设置常用方法

import requests

default_headers = {
  'accept':'*/*',
  "Content-Type": "application/json",
  'accept-language':'zh-CN,zh;q=0.9',
  'content-type':'application/json',
  'priority':'u=1, i',
  'sec-ch-ua':'"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
  'sec-ch-ua-mobile':'?0',
  'sec-ch-ua-platform':'"Windows"',
  'sec-fetch-dest':'empty',
  'sec-fetch-mode':'cors',
  'sec-fetch-site':'same-site',
  'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

def get(url,data = None):
    response = requests.get(url,headers=default_headers, data=data)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.HTTPError as err:
        print(f"Utils get 错误发生: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Utils get 请求异常: {err}")
        return None

'''class Utils:
  def get(url,data = None):
    response = requests.get(url,headers=default_headers, data=data)
    try:
        response.raise_for_status()
        print("请求成功!")
        return response.content
    except requests.exceptions.HTTPError as err:
        print(f"Utils get 错误发生: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Utils get 请求异常: {err}")
        return None'''