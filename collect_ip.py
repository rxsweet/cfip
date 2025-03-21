import re
import requests
import json

#https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/HK.txt
apiList={
  'HK':'https://ghraw.eu.org/6Kmfi6HP/proxy_files/main/HK.txt',
  'TW':'https://ghraw.eu.org/6Kmfi6HP/proxy_files/main/TW.txt',
  'JP':'https://ghraw.eu.org/6Kmfi6HP/proxy_files/main/JP.txt',
  'SG':'https://ghraw.eu.org/6Kmfi6HP/proxy_files/main/SG.txt',
  'KR':'https://ghraw.eu.org/6Kmfi6HP/proxy_files/main/KR.txt',
  'US':'https://ghraw.eu.org/6Kmfi6HP/proxy_files/main/US.txt',
  }
"""
apiList={
  'HK':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/HK.txt',
  'TW':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/TW.txt',
  'JP':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/JP.txt',
  'SG':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/SG.txt',
  'KR':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/KR.txt',
  'US':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/US.txt',
  }
"""
def saveIP(configList):#整理保存

    for key,value in configList.items():
        #将IP和端口中间的空格替换成‘:’,方便使用
        value = re.sub(' ',':',value)
        #添加区域标注
        ip_list = re.split(r'\n+',value)
        new_ip_list = f'#{key}\n'.join(ip_list)#加注释 #HK等
        
        #保存
        try:
            with open(f'./ips/{key}.txt', 'w', encoding='utf-8') as f:
                f.write(new_ip_list)
            print(f'save {key}.txt 完成！')
        except requests.exceptions.RequestException as e:  
            #print(e)
            print(F'获取{key}写入错误!')
            pass

    
def getContent(url):#获取网站的内容，将获取的内容返回
    headers={
    "User-Agent":"okhttp/3.15",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    try:
        r=requests.get(url,headers=headers, timeout=5.0)
        if r.status_code==200:
            r.encoding='utf-8'    #编码方式
            print(f'{url}网站收集IP完成。')
            return r.text
    except requests.exceptions.RequestException as e:  
        #print(e)
        print(F'getContent()功能中出现的错误！获取{url}内容失败，或者打开网址错误!')
        pass

def fetchIP(apiList):#获取列表网站的ip内容
    ipList={}
    for key,value in apiList.items():
        config=getContent(value)
        if config:
            ipList[key]=config
    return ipList
    
if "__name__==__main__":#主程序开始
    #收集IP
    configList = fetchIP(apiList)
    #整理保存
    saveIP(configList)
    
    
