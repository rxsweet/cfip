import re
import requests
import json

def get_address(ip):
    tap_url = f'https://ip125.com/api/{ip}?lang=zh-CN'
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Cookie': '_ga=GA1.2.348223593.1668760697; _ga_XYJPKQNDKR=GS1.1.1669809730.4.1.1669809752.0.0.0; __gads=ID=e9cb6076c0188403-228d0f367edf00b9:T=1683097828:RT=1701660864:S=ALNI_MZoNQcRpP-66ZZidp6BAlct92mbOw; __gpi=UID=00000c011afd3f29:T=1683097828:RT=1701660864:S=ALNI_MZSTguCSNwyc6d4WgMIcm7m-Xepvg'
    }
    try:
        country_info = requests.get(tap_url, headers=head).json()
        #return country_info['countryCode'] + country_info['country']
        return country_info['countryCode']
    except Exception as e:#万能异常
        print(str(e) + 'Exception_出现异常')
        pass
        return '未知'

def list_rm(urlList):#列表去重
    begin = 0
    rm = 0
    length = len(urlList)
    print(f'\n-----去重开始-----\n')
    while begin < length:
        proxy_compared = urlList[begin]
        begin_2 = begin + 1
        while begin_2 <= (length - 1):
            if proxy_compared == urlList[begin_2]:
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

    with open('ip.txt', 'r', encoding='utf-8') as f:
        ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)
    #去重
    ip_list = list_rm(ip_list)
    
    #去重后保存
    #ip_rm = '\n'.join(ip_list)
    #with open(f'./ip/ip_rm.txt', 'w', encoding='utf-8') as f:
        #f.write(ip_rm)
    
    
    ALLIP = []
    HKIP = []
    TWIP = []
    JPIP = []
    SGIP = []
    KRIP = []
    USIP = []
    otherIP= []
    for i in range(len(ip_list)):
        try:
            if ip_list[i] == '':
                continue
            ipaddr = ip_list[i].split("#")[0]
            if ':' in ipaddr:
                ipaddr = ip_list[i].split(":")[0]
            #print(ipaddr)
            country_info = get_address(ipaddr)
            ip_list[i] = ip_list[i] + '#' + country_info
            
            if country_info == 'HK':
                HKIP.append(ip_list[i])
            elif country_info == 'TW':
                TWIP.append(ip_list[i])
            elif country_info == 'JP':
                JPIP.append(ip_list[i])
            elif country_info == 'SG':
                SGIP.append(ip_list[i])
            elif country_info == 'KR':
                KRIP.append(ip_list[i])
            elif country_info == 'US':
                USIP.append(ip_list[i])
            else:
                ip_list[i] = ip_list[i] + '_other'
                otherIP.append(ip_list[i])
            #ALLIP.append(ip_list[i])#需要按国家排序的话,#号掉这个开启下面的"""
            print(ip_list[i])
        except Exception as e:#万能异常
            print(f'{ip_list[i]}出现错误,错误内容如下：\n{e}')
            pass

    #"""
    #按地区顺序排列
    ALLIP = []
    ALLIP.extend(HKIP)
    ALLIP.extend(TWIP)
    ALLIP.extend(JPIP)
    ALLIP.extend(SGIP)
    ALLIP.extend(KRIP)
    ALLIP.extend(USIP)
    ALLIP.extend(otherIP)
    #"""
    
    ALLIP = '\n'.join(ALLIP)
    with open(f'./ip/ALLIP.txt', 'w', encoding='utf-8') as f:
        f.write(ALLIP)
    #按区域保存
    HKIP = '\n'.join(HKIP)
    with open(f'./ip/HKIP.txt', 'w', encoding='utf-8') as f:
        f.write(HKIP)
    TWIP = '\n'.join(TWIP)
    with open(f'./ip/TWIP.txt', 'w', encoding='utf-8') as f:
        f.write(TWIP)
    JPIP = '\n'.join(JPIP)
    with open(f'./ip/JPIP.txt', 'w', encoding='utf-8') as f:
        f.write(JPIP)
    SGIP = '\n'.join(SGIP)
    with open(f'./ip/SGIP.txt', 'w', encoding='utf-8') as f:
        f.write(SGIP)
    KRIP = '\n'.join(KRIP)
    with open(f'./ip/KRIP.txt', 'w', encoding='utf-8') as f:
        f.write(KRIP)
    USIP = '\n'.join(USIP)
    with open(f'./ip/USIP.txt', 'w', encoding='utf-8') as f:
        f.write(USIP)

