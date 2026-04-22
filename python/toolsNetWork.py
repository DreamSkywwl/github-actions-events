import json
import requests
def safe_request(url, method='GET',type="json" **kwargs):
# def get_requests(item):
    try:
        # 发送请求示例，请替换为你实际的请求逻辑
        # respose = requests.request(method=method, url=url,**kwargs)
        requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        s = requests.session()
        s.keep_alive = False # 关闭多余连接
        respose = s.request(method=method, url=url,**kwargs)
        
        # 显式检查状态码
        respose.raise_for_status()  # 如果状态码不是 200-299，会抛出 HTTPError
        
        # 检查内容是否为空
        if not respose.text.strip():
            raise ValueError("Empty response received")
        if type == 'json':
          return respose.json()
        else:
          return respose.text
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decode error: {json_err}")
        print(f"Invalid content: {respose.text[:200]}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    
    return None # 返回默认值或重新抛出异常



# requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        # s = requests.session()
        # s.keep_alive = False # 关闭多余连接
        # respose = s.post(url=urlValueJueJin,headers=headers,data=json.dumps(data))
        # # --- 修改后的调试代码 ---
        # print(f"Status Code: {respose.status_code}")
        # print(f"Response Headers: {respose.headers}")
        # print(f"Response Text (first 500 chars): {respose.text[:500]}")