import re
import requests
import json

SOURCE = 'ip.txt'

def list_rm(urlList):#列表去重
    begin = 0
    rm = 0
    length = len(urlList)
    print(f'\n-----去重开始-----\n')
    while begin < length:
        proxy_compared = urlList[begin]
        begin_2 = begin + 1
        while begin_2 <= (length - 1):
            ip = re.split(r'#',urlList[begin_2])
            if ip[0] in proxy_compared:
                urlList.pop(begin_2)
                length -= 1
                begin_2 -= 1
                rm += 1
            begin_2 += 1
        begin += 1
    print(f'重复数量 {rm}\n-----去重结束-----\n')
    print(f'剩余总数 {str(len(urlList))}\n')
    return urlList
    
if "__name__==__main__":#主程序开始

    with open(SOURCE, 'r', encoding='utf-8') as f:
        ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)
    #去重
    ip_list = list_rm(ip_list)
    
    ip_list = '\n'.join(ip_list)
    with open(SOURCE, 'w', encoding='utf-8') as f:
        f.write(ip_list)
