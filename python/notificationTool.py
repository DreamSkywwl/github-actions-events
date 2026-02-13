# -*- coding: utf-8 -*-
# 消息推送功能
from datetime import datetime
import requests
import os



class notificationTool:
    def main(self,titleMsg, message):
        showdocPin = os.environ.get('SHOWDOC_PIN')
        showdocToken = os.environ.get('SHOWDOC_TOKEN')
        letserverToken = os.environ.get('LETSERVER_TOKEN')
        
        
        if not showdocPin or not showdocToken or not letserverToken:
          raise ValueError("notificationTool Missing required environment variables")
        
        self.notificationWe_showdoc(showdocPin,showdocToken,titleMsg, message)
        self.notificationWe_letserver(letserverToken,titleMsg)

    def notificationWe_showdoc(self,showdocPin,showdocToken,titleMsg, message):
        url = "https://push.showdoc.com.cn/server/api/push/" + showdocPin
        
        payload = {
            "title": titleMsg,
            "content": message,
            "user_token": showdocToken
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
        print(f'notificationWe_showdoc error:{response.text}')
          
    
    def notificationWe_letserver(self,letserverToken,titleMsg):
        url = "https://api.letserver.run/message/info?token=" + letserverToken + '&msg=' + titleMsg
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.get(url, headers=headers)

        print(f'notificationWe_letserver error:{response.text}')
          

 