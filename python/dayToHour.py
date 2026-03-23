
import requests
from xml.etree import ElementTree as ET
from urllib.parse import urljoin

def fetch_rss_with_headers(url, headers=None):
    """
    获取RSS源并添加请求头信息
    
    Args:
        url (str): RSS源URL
        headers (dict): 请求头信息
    
    Returns:
        list: 解析后的RSS条目列表
    """
    # 如果没有提供headers，则使用默认的User-Agent
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    try:
        # 发送GET请求，包含请求头
        response = requests.get(url, headers=headers, timeout=10)
        
        # 检查响应状态码
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return []
        
        # 显式设置编码为utf-8
        response.encoding = 'utf-8'
        
        # 检查Content-Type是否为XML类型
        content_type = response.headers.get('content-type', '')
        if 'xml' not in content_type.lower() and 'rss' not in content_type.lower():
            print(f"警告: 内容类型不是XML或RSS: {content_type}")
        
        # 解析XML内容
        root = ET.fromstring(response.text)
        
        # 根据RSS类型解析条目
        items = []
        
        # 处理RSS 2.0格式
        if root.tag == 'rss':
            channel = root.find('channel')
            if channel is not None:
                for item in channel.findall('item'):
                    title = item.findtext('title', '')
                    link = item.findtext('link', '')
                    pub_date = item.findtext('pubDate', '')
                    description = item.findtext('description', '')
                    
                    items.append({
                        'title': title,
                        'link': link,
                        'pub_date': pub_date,
                        'description': description
                    })
        
        # 处理Atom格式
        elif root.tag == '{http://www.w3.org/2005/Atom}feed':
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.findtext('{http://www.w3.org/2005/Atom}title', '')
                link_elem = entry.find('{http://www.w3.org/2005/Atom}link')
                link = link_elem.get('href') if link_elem is not None else ''
                pub_date = entry.findtext('{http://www.w3.org/2005/Atom}published', '')
                description = entry.findtext('{http://www.w3.org/2005/Atom}summary', '')
                
                items.append({
                    'title': title,
                    'link': link,
                    'pub_date': pub_date,
                    'description': description
                })
        
        return items
        
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return []
    except ET.ParseError as e:
        print(f"XML解析错误: {e}")
        return []
    except Exception as e:
        print(f"未知错误: {e}")
        return []

# 示例使用
if __name__ == "__main__":
    # RSS源URL
    rss_url = "https://feeds.bbci.co.uk/news/rss.xml"
    
    # 自定义请求头
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml;q=0.9, */*;q=0.8'
    }
    
    # 获取RSS内容
    rss_items = fetch_rss_with_headers(rss_url, custom_headers)
    print(f"====:{rss_items}")
    
