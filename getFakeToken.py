import requests
import json
import time
from getproxy import getProxy

def shareToken(token,unique_name,expires_in = 0):
    url = "https://ai.fakeopen.com/token/register"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ai.fakeopen.com",
        "Referer": "https://ai.fakeopen.com/token",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "unique_name": unique_name ,
        "access_token": token,
        "expires_in": expires_in,
        "site_limit": None,
        "show_conversation": "false",
    }
    for i in range(3):
        try:
            response = requests.post(url, headers=headers, data=data,proxies=getProxy())
            if response.status_code != 200:
                print(f"账号{unique_name}请求失败，状态码{response.status_code}, 返回值{response.json()}\n")
                break
            return response
        except requests.exceptions.HTTPError as e:
            print("请求失败: ", e)
            print("正在重试...")
            time.sleep(3)
        
    return response


#openai请求地址: api.openai.com/v1/engines/davinci/completions