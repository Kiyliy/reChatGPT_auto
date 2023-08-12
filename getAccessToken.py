from multiprocessing import Value
import requests
import json
import threading
from writeExcle import WriteAccessTokenToFile
from getFakeToken import shareToken
from queue import Queue
import config
import openpyxl
from remove_refresh_token import remove_refresh_token


def GetAccessToken(
    username : str,
    password : str,
    cnt: Value
):
    """
    函数:
        输入: username 和 password, cnt计数器
        返回:response
        功能:获取token
    """
    if username == None or password == None or username == "" or password == "":
        return None
    url = "https://ai.fakeopen.com/auth/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://ai.fakeopen.com",
        "Referer": "https://ai.fakeopen.com/auth1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
        "X-Requested-With": "XMLHttpRequest"
        }
    data = {
        "username": username,
        "password": password,
        # "mfa_code": "",
    }
    try:
        response = requests.post(url, headers=headers, data=data)
    except Exception as e:
        return e

    with cnt.get_lock():
        cnt.value += 1
        if response.status_code != 200:
            print(f"{cnt.value}:账号{username}请求失败，状态码{response.status_code}, 返回值{response.json()}\n")
            return response
        else:
            print(f"{cnt.value}账号{username}:{200}\n")
            return response
    
  
class GetAccessTokenThread(threading.Thread):
    def __init__(
            self,
            lock: threading.Lock,
            xlsxQueue: Queue,
            AccessTokensWorksheet : openpyxl.worksheet.worksheet.Worksheet,
            cnt: Value,
            errorWorksheet
        ):
        """
        继承: threading.Thread 多线程任务
        参数: lock锁, xlseGenerator: 队列
            AccessTokenWorksheet: 工作表对象
            cnt: 计数器
        
        """
        threading.Thread.__init__(self)
        self.lock = lock
        self.xlsxQueue = xlsxQueue
        self.AccessTokensWorksheet = AccessTokensWorksheet
        self.cnt = cnt
        self.errorWorksheet = errorWorksheet
    def run(self):
        """
        参数: None
        返回值:None
        功能: 运行多线程, 从队列中获取账号密码, 通过GetAccessToken获取token, 将token获取fk,再写入文件中 
        """
        while not self.xlsxQueue.empty():
            try:
                self.lock.acquire()
                if self.xlsxQueue.empty():
                    print("队列为空")
                    self.lock.release()
                    break
                row =self.xlsxQueue.get() ##核心代码, 从队列中获取账号密码
                self.lock.release()
                username , password = row
                response = GetAccessToken(username, password,self.cnt) #response状态码如果是200，说明请求失败, 在write的时候处理
                if response.status_code == 200:
                    fkresponse = shareToken(response.json()["access_token"],username)
                    if config.remove_refresh_token == True:
                        remove_refresh_token(response.json()["refresh_token"],config.remove_refresh_token_proxy_address)
                else:
                    fkresponse =None
                self.lock.acquire()
                WriteAccessTokenToFile(username, password, response, self.AccessTokensWorksheet,fkresponse,self.errorWorksheet)
                self.lock.release()
                if(config.debug_mode==True and self.cnt.value >= 30):
                    break
                # raise Exception("测试异常")
            except Exception as e:
                print(f"Get Access Token thread出现错误!,err:{e}")
                WriteAccessTokenToFile(username, password, str(e), self.AccessTokensWorksheet,None,self.errorWorksheet)
                continue
        return
    
      
      