
# -*- coding: utf-8 -*-
import os

from datetime import datetime, timezone


from github import Github


# 计算时间差值

class FileTracker:
  
  def saveContent(self, fileName,message):
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      repo = self.initDataBase()
      print(f"FileTracker saveContent fileName====:{fileName} current_time====:{current_time} message====:{message}")
      try:
          contents = repo.get_contents(fileName)
          response = repo.update_file(
              path=contents.path,
              message=f"Update {fileName} timestamp: {current_time}",
              content=message,
              sha=contents.sha
          )
          print(f"FileTracker saveContent response ====:{response}")
      except Exception:
          repo.create_file(
              path=fileName,
              message=f"Update {fileName} timestamp: {current_time}",
              content=current_time
          )
          print(f"FileTracker saveContent Successfully created file: {fileName},  timestamp: {current_time} error:{e}")


  def getContent(self, fileName):
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      print(f"FileTracker getContent fileName====:{fileName} current_time====:{current_time}")
      
      repo = self.initDataBase()
      try:
          contents = repo.get_contents(fileName)
          print(f"FileTracker---getContent---file:{fileName} value:{contents}. timestamp:{current_time}")
          str = contents.decoded_content.decode('utf-8')
          if str in None or len(str) == 0:
              str = ''
          print(f"FileTracker---getContent---file:{fileName} value:{str}. timestamp:{current_time}")
          return str
      except Exception as e:
          print(f"FileTracker---getContent---file:{fileName} No Found. timestamp:{current_time} error:{e}")
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
