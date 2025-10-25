import re
import requests
import json


#保存路径
NiREvil_SAVE_PATH = './ip/nirevil/'
Exball_SAVE_PATH = './ip/exball/'
#https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/HK.txt
#https://ghraw.eu.org/6Kmfi6HP/proxy_files/main/HK.txt
"""
#大佬不更新,暂时用NiREvil大佬的
apiList={
  'hk':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/HK.txt',
  'tw':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/TW.txt',
  'jp':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/JP.txt',
  'sg':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/SG.txt',
  'kr':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/KR.txt',
  'us':'https://raw.githubusercontent.com/6Kmfi6HP/proxy_files/main/US.txt',
  }
"""
NiREvil_apiList={
  'hk':'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/HK.txt',
  'tw':'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/TW.txt',
  'cn':'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/CN.txt',
  'jp':'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/JP.txt',
  'sg':'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/SG.txt',
  'kr':'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/KR.txt',
  'us':'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/US.txt',
  }
exball_apiList={
  'hk':'https://raw.githubusercontent.com/exball/sing-box-config/refs/heads/Master/proxy-scaner/proxy_list/proxyList_HK.txt',
  'tw':'https://raw.githubusercontent.com/exball/sing-box-config/refs/heads/Master/proxy-scaner/proxy_list/proxyList_TW.txt',
  'jp':'https://raw.githubusercontent.com/exball/sing-box-config/refs/heads/Master/proxy-scaner/proxy_list/proxyList_JP.txt',
  'sg':'https://raw.githubusercontent.com/exball/sing-box-config/refs/heads/Master/proxy-scaner/proxy_list/proxyList_SG.txt',
  'kr':'https://raw.githubusercontent.com/exball/sing-box-config/refs/heads/Master/proxy-scaner/proxy_list/proxyList_KR.txt',
  'us':'https://raw.githubusercontent.com/exball/sing-box-config/refs/heads/Master/proxy-scaner/proxy_list/proxyList_US.txt',
  }


#get ip: https://github.com/exball
def Exball_saveIP():#整理保存
    try:
        configList = fetchUrlContent(exball_apiList)
        if not configList:
            print("failed: exball no ip was collected! ")
            return

    except:
        print("exball ip collect Error!")
        return
    allip = []
    port443 = []
    for key,value in configList.items():
        #保存区域
        try:
            #添加区域标注
            new_list = []
            ip_list = re.split(r'\n+',value)
            for ip in ip_list:
                ipinfo = ip.split(',')
                ipaddr = ipinfo[0]
                port   = ipinfo[1]
                country= ipinfo[2]
                new_list.append(ipaddr+':'+port+'#'+key+'_'+'Exball')
            
            new_ip_list = '\n'.join(new_list)
            #print(new_ip_list)
            with open(f'{Exball_SAVE_PATH}{key}.txt', 'w', encoding='utf-8') as f:
                f.write(new_ip_list)
            print(f'save {key}.txt 完成！')
            allip.append(new_ip_list)
        except requests.exceptions.RequestException as e:  
            #print(e)
            print(F'获取{key}写入错误!')
            pass

    #将IP合并保存
    allip = ''.join(allip)
    with open(f'{Exball_SAVE_PATH}allip.txt', 'w', encoding='utf-8') as f:
        f.write(allip)
    print(f'save allip.txt 完成！')
    
    allip = re.split(r'\n+',allip)
    #筛选443端口IP
    for ip in allip:
        if ':443' in ip and '#us' not in ip:
            #print(ip + 'haha' + '\n')
            ip = ip.split(":")[0]
            port443.append(ip)
    #保存443端口IP
    port443 = '\n'.join(port443)
    with open(f'{Exball_SAVE_PATH}port443.txt', 'w', encoding='utf-8') as f:
        f.write(port443)
    print(f'save port443.txt 完成！')

#get ip: https://github.com/NiREvil
def NiREvil_saveIP():#整理保存
    try:
        configList = fetchUrlContent(NiREvil_apiList)
        if not configList:
            print("failed: NiREvil no ip was collected! ")
            return
    except:
        print("NiREvil ip collect Error!")
        return
    allip = []
    port443 = []
    for key,value in configList.items():
        #保存区域
        try:
            #将IP和端口中间的空格替换成‘:’,方便使用
            value = re.sub(' ',':',value)
            #添加区域标注
            ip_list = re.split(r'\n+',value)
            new_ip_list = f'#{key+"_NiREvil"}\n'.join(ip_list)#加注释 #HK等
            with open(f'{NiREvil_SAVE_PATH}{key}.txt', 'w', encoding='utf-8') as f:
                f.write(new_ip_list)
            print(f'save {key}.txt 完成！')
            allip.append(new_ip_list)
        except requests.exceptions.RequestException as e:  
            #print(e)
            print(F'获取{key}写入错误!')
            pass

    #将IP合并保存
    allip = ''.join(allip)
    with open(f'{NiREvil_SAVE_PATH}allip.txt', 'w', encoding='utf-8') as f:
        f.write(allip)
    print(f'save allip.txt 完成！')
    
    allip = re.split(r'\n+',allip)
    #筛选443端口IP
    for ip in allip:
        if ':443' in ip and '#us' not in ip:
            #print(ip + 'haha' + '\n')
            ip = ip.split(":")[0]
            port443.append(ip)
    #保存443端口IP
    port443 = '\n'.join(port443)
    with open(f'{NiREvil_SAVE_PATH}port443.txt', 'w', encoding='utf-8') as f:
        f.write(port443)
    print(f'save port443.txt 完成！')

        
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

def fetchUrlContent(apiList):#获取列表网站的ip内容
    ipList={}
    for key,value in apiList.items():
        config=getContent(value)
        if config:
            ipList[key]=config
    return ipList


#ip列表去重
def ip_list_rm(urlList):#列表去重
    begin = 0
    rm = 0
    length = len(urlList)
    print(f'-----去重开始-----')
    while begin < length:
        proxy_compared = urlList[begin]
        begin_2 = begin + 1
        repeat = 0 #单个重复数
        while begin_2 <= (length - 1):
            ip = re.split(r':',urlList[begin_2])
            if ip[0] in proxy_compared:
                urlList.pop(begin_2)
                length -= 1
                begin_2 -= 1
                rm += 1
                repeat = repeat + 1
            begin_2 += 1
        #给去重后的元素添加重复数
        if repeat > 0:
             urlList[begin]= urlList[begin] + '_'+ str(repeat)
        begin += 1
    print(f'重复数量 {rm}\n-----去重结束-----')
    print(f'剩余总数 {str(len(urlList))}')
    return urlList


#合并IP文件
def mergeIP():
    #需要合并的IP添加到下面ipfiles中
    ipfiles = {
    'hk':[],
    'jp':[],
    'kr':[],
    'sg':[],
    'us':[],
    'port443':[],
    }
    for key,value in ipfiles.items():
        try:
            with open(f'{NiREvil_SAVE_PATH}{key}.txt', 'r', encoding='utf-8') as f:
                content1 = f.read()
            with open(f'{Exball_SAVE_PATH}{key}.txt', 'r', encoding='utf-8') as f:
                content2 = f.read()
            ip_list = re.split(r'\n',content1)
            value.extend(ip_list) 
            ip_list = re.split(r'\n',content2)
            value.extend(ip_list)
            print(f'{key}.txt准备去重:')
            value = ip_list_rm(value)
            ipall = '\n'.join(value)
            with open(f'./ip/{key}.txt', 'w', encoding='utf-8') as f:
                f.write(ipall)
            print(f'合并(merge) {key}.txt 完成！\n')
        except:
            print(f"{key}.txt ip collect Error!\n")

if "__name__==__main__":#主程序开始
    NiREvil_saveIP()
    Exball_saveIP()
    mergeIP()
