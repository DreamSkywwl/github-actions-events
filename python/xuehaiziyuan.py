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
FileTracker().saveContent(fileName=defaultFile,message="aaaaaaaaaaa")
print(FileTracker.getContent(fileName=defaultFile))
