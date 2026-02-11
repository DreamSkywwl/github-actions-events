
# -*- coding: utf-8 -*-
import os

from datetime import datetime, timezone

from github import Github


# 计算时间差值

class FileTracker:
  
  def saveContent(self, fileName,message):
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      repo = self.initDataBase(fileName)
      try:
          contents = repo.get_contents(fileName)
          repo.update_file(
              path=fileName,
              message=f"Update {fileName} timestamp: {current_time}",
              content=message,
              sha=contents.sha
          )
      except Exception:
          repo.create_file(
              path=fileName,
              message=f"Update {fileName} timestamp: {current_time}",
              content=current_time
          )
          print(f"Successfully created file: {fileName},  timestamp: {current_time}")


  def getContent(self, fileName):
      if None in fileName or len(fileName) == 0:
          print(f"getContent fileName None")
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      print(f"getContent fileName====:{fileName}")
      repo = self.initDataBase()
      try:
          contents = repo.get_contents(fileName)
          str = contents.decoded_content.decode('utf-8')
          return str
      except Exception:
          print(f"file:{fileName} No Found. timestamp:{current_time}")
          return ''
  
  # 初始化环境变量
  def initDataBase(self):
      # 获取环境变量
      source_token = os.environ.get('GITHUB_TOKEN')
      target_repo_name = os.environ.get('TARGET_REPO')
      target_token = os.environ.get('TARGET_TOKEN')
      
      if not source_token or not target_repo_name or not target_token:
          raise ValueError("Missing required environment variables")
      

      # 初始化GitHub客户端
      target_g = Github(target_token)
      
      # 获取目标仓库对象
      target_repo = target_g.get_repo(target_repo_name)

      return target_repo
      
     
      # 加载上次执行时间
      # last_time = self.load_last_time(target_repo, fileName)
     


# if __name__ == "__main__":
#     TimeTracker().main()
