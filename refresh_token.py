import json
import requests
#######################测试
proxy_address = "socks5://kimi3099:kimi3099_country-us@geo.iproyal.com:32325"

########################
#请求地址为: openai
def refreshToken(
    refresh_token : str,
    proxy_address: str = ""
    ):
  
  url = "https://auth0.openai.com/oauth/token"
  proxy_socks = {
      'http': proxy_address,
      'https': proxy_address
  }
  headers = {'content-type': 'application/json'}
  data = {
    "redirect_uri": "com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback",
    "grant_type": "refresh_token",
    "client_id": "pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh",
    "refresh_token": refresh_token,
  }
  if proxy_address != "":
    try:
      print("DEBUG: 正在尝试使用代理请求: ")
      req = requests.post(url,headers=headers, data=json.dumps(data),proxies=proxy_socks)
    except:
      print("DEBUG: 代理请求失败!, 请检查代理设置!")
  else:
    print("DEBUG: 正在尝试不使用代理请求: ")
    req = requests.post(url,headers=headers, data=json.dumps(data))
  return req
