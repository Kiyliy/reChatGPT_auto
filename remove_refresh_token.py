import requests

def remove_refresh_token(refresh_token,proxy_address):
    proxies = {
        #本地127.0.0.1:7890
        "http": "http://"+proxy_address,
        "https": "http://"+proxy_address,
    }
    url = "https://auth0.openai.com/oauth/revoke"
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200",
}
    data = {
        "client_id":  "pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh",
        "token": refresh_token
    }
    
    try:
        response = requests.post(url=url, data=data,headers = headers,proxies=proxies)
        print(response)
        if response.status_code == 200:
            print("DEBUG: 成功吊销refresh_token")
            
        return response

    except Exception as e:
        print(f"remove_token err: {e}")
