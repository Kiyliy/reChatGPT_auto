# 需要安装此依赖
# pip install requests
import requests

def getProxy():
    # 发送给服务器的标识
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/532.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    # 代理api，，更换为您生成的代理API连接
    proxyUrl = "http://api.3ip.cn/dmgetip.asp?apikey=3b47f560&pwd=99b0037ed12a47c71c09a7a3406b3486&getnum=1&httptype=0&geshi=1&fenge=1&fengefu=&Contenttype=1&operate=all"
    # 请求代理url，获取代理ip 
    outPutProxy = getProxyip(proxyUrl, userAgent)
    if len(outPutProxy)==0:
        # 没有获取到代理
        return
    try:
        # 从列表中取出一个代理出来
        px = outPutProxy.pop(0)  
        proxy = {
            "http": "http://"+px,
            "https": "http://"+px
        }
        return proxy
    
    except Exception as e:
        print(e)
        if (len(outPutProxy) == 0):
            # 如果发现没有代理了，就去获取下。
            outPutProxy = getProxyip(proxyUrl, userAgent)
            px = outPutProxy.pop(0)
            proxy = {
                "http": "http://"+px,
                "https": "http://"+px
            }
            return proxy

def getProxyip(proxyUrl, userAgent):
    proxyIps=""
    outPutProxy = []
    try:
        proxyIps = requestGet(proxyUrl, userAgent, None)
        print(proxyIps)
        # {"code":3002,"data":[],"msg":"error!用户名或密码错误","success":false}
        if "{" in proxyIps:
            raise Exception("[错误]"+proxyIps)
        outPutProxy = proxyIps.split("\n")     
    except Exception as e:
        print(e)
    print("总共获取了"+str(len(outPutProxy))+"个代理")
    return outPutProxy

def requestGet(url, userAgent, proxy):
    headers = {
        "User-Agent": userAgent
    }
    response = None
    if (proxy):
        # 有代理的时候走这个
        response = requests.get(url, headers=headers, timeout=5, proxies=proxy) 
    else:
        # 没有代理走这个
        response = requests.get(url, headers=headers, timeout=5)
    # 设置编码，防止乱码
    # requests 库会帮我们自动分析这个网页的字符编码
    response.encoding = response.apparent_encoding
    return response.text

print(getProxy())