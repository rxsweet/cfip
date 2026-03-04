import re
import os
import requests
from datetime import datetime

PATH = os.path.dirname(os.path.abspath(__file__))


def getUrlContent(url):  
    print(f'获取all_ip:{url}')
    headers={
        "User-Agent":"okhttp/3.15",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
    try:
        r=requests.get(url,headers=headers, timeout=3.0)
        #print(r.text)
        if r.status_code==200:
            r.encoding='utf-8'    #编码方式
            #print(r.text)
            print('获取成功！')
            return r.text
    except requests.exceptions.RequestException as e:  
        print(e)
        print('getUrlContent()功能中出现的错误！获取ip失败，或者打开网址错误!')
        return ''

if "__name__==__main__":#主程序开始
    
    #使用在线获取all ip，不用自己手动复制了
    ip_all = getUrlContent('https://ghraw.eu.org/rxsweet/cfip/main/ip/allip.txt')
    #关闭了下面的读取allip文件，使用了上面的，需要使用时打开
    #with open(f'{PATH}allip.txt', 'r', encoding='utf-8') as f:
        #ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)

    with open(f'{PATH}/node.txt', 'r', encoding='utf-8') as f:
        ip_node_all = f.read()
    ip_node_list = re.split(r'\n+',ip_node_all)
    
    alive_ip = []
    for ip in ip_list:
        if ip == '' or ip == '\n':
            continue
        if '#' in ip:
            ipaddr = ip.split("#")[0]
        else:
            ipaddr = ip
        for node in ip_node_list:
            if ipaddr in node:
                alive_ip.append(ip)
                print(ip)
                continue
    #保存
    nowtime = datetime.today().strftime('%Y%m%d')
    alive_ip_str = '\n'.join(alive_ip)
    with open(f'{PATH}/aliveip/aliveip_{nowtime}.txt', 'w', encoding='utf-8') as f:
        f.write(alive_ip_str)

    #暂时不需要分区了
    """
    #分区域
    hkip = []
    jpip = []
    sgip = []
    krip = []
    usip = []
    for ip in alive_ip:
        if 'hk' in ip or 'tw' in ip or 'cn' in ip or 'HK' in ip or 'TW' in ip or 'CN' in ip:
            hkip.append(ip)
        if 'jp' in ip or 'JP' in ip:
            jpip.append(ip)
        if 'sg' in ip or 'SG' in ip:
            sgip.append(ip)
        if 'kr' in ip or 'KR' in ip:
            krip.append(ip)
        if 'us' in ip or 'US' in ip:
            usip.append(ip)
    #保存
    if hkip:
        hkip = '\n'.join(hkip)
        with open(f'{PATH}/checked/hk.txt', 'w', encoding='utf-8') as f:
            f.write(hkip)
    if jpip:
        jpip = '\n'.join(jpip)
        with open(f'{PATH}/checked/jp.txt', 'w', encoding='utf-8') as f:
            f.write(jpip)
    if sgip:
        sgip = '\n'.join(sgip)
        with open(f'{PATH}/checked/sg.txt', 'w', encoding='utf-8') as f:
            f.write(sgip)
    if krip:
        krip = '\n'.join(krip)
        with open(f'{PATH}/checked/kr.txt', 'w', encoding='utf-8') as f:
            f.write(krip)
    if usip:
        usip = '\n'.join(usip)
        with open(f'{PATH}/checked/us.txt', 'w', encoding='utf-8') as f:
            f.write(usip)
    """
