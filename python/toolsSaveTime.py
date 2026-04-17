
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime, timezone
from github import Github
import requests
from notificationTool import notificationTool

# 计算时间差值
class TimeTracker:
  def save_current_time(self,repo, file_path):
      """保存当前时间到目标仓库"""
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      #datetime.now().isoformat()
      
      try:
          contents = repo.get_contents(file_path)
          repo.update_file(
              path=file_path,
              message=f"Update timestamp: {current_time}",
              content=current_time,
              sha=contents.sha
          )
          # markDown(current_time, )
          # print(f"Successfully updated timestamp file: {current_time}")
          
      except Exception:
          repo.create_file(
              path=file_path,
              message=f"Create timestamp file: {current_time}",
              content=current_time
          )
          print(f"Successfully created timestamp file: {current_time}")
          

  def load_last_time(self,repo, file_path):
      """从目标仓库加载上次执行时间"""
      try:
          contents = repo.get_contents(file_path)
          last_time_str = contents.decoded_content.decode('utf-8')
          return datetime.fromisoformat(last_time_str)
      except Exception:
          print("No previous timestamp found")
          return None

  def calculate_time_difference(self,last_time, current_time):
      """计算时间差"""
      if last_time:
          diff = current_time - last_time
          return diff.total_seconds()
      return None

  def setTimes(self, filename):
      target_repo = self.commonWay()
      # 定义时间戳文件路径
      timestamp_file = filename + '.txt'
      self.save_current_time(target_repo, timestamp_file)
      
  def getTimes(self, filename):
      target_repo = self.commonWay()
      # 定义时间戳文件路径
      timestamp_file = filename + '.txt'
      
      # 加载上次执行时间
      last_time = self.load_last_time(target_repo, timestamp_file)
      
      current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      # 计算时间差
      time_diff = self.calculate_time_difference(last_time, current_time)

      print('time_tracker获取时间差值：{},保存文件地址:{}'.format(time_diff,filename))
      
      return time_diff
  
  def commonWay(self):
  # def main(self, filename):
      # 获取环境变量
      source_token = os.environ.get('GITHUB_TOKEN')
      target_repo_name = os.environ.get('TARGET_REPO')
      target_token = os.environ.get('TARGET_TOKEN')
      
      if not source_token or not target_repo_name or not target_token:
          raise ValueError("Missing required environment variables")
      
      # 初始化GitHub客户端
      # source_g = Github(source_token)
      target_g = Github(target_token)
      
      # 获取源仓库信息
      # source_repo_name = os.environ.get('GITHUB_REPOSITORY')
      # source_repo = source_g.get_repo(source_repo_name)
      
      # 获取目标仓库对象
      target_repo = target_g.get_repo(target_repo_name)


      return target_repo
      
     
      
# if __name__ == "__main__":
#     TimeTracker().main()
