import re
from datetime import datetime
import requests
import json


PATH = './'
IPURL = './ipurl.txt'


def get_address(ip):#得到IP归属地
    #tap_url = f'https://ip125.com/api/{ip}?lang=zh-CN'
    #tap_url = f'https://api.ip.sb/geoip/{ip}'
    tap_url = f'http://ip-api.com/json/{ip}?lang=zh-CN'
    head = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Cookie': '_ga=GA1.2.348223593.1668760697; _ga_XYjpKQNDkr=GS1.1.1669809730.4.1.1669809752.0.0.0; __gads=ID=e9cb6076c0188403-228d0f367edf00b9:T=1683097828:RT=1701660864:S=ALNI_MZoNQcRpP-66ZZidp6BAlct92mbOw; __gpi=UID=00000c011afd3f29:T=1683097828:RT=1701660864:S=ALNI_MZSTguCSNwyc6d4WgMIcm7m-Xepvg'
    }
    try:
        country_info = requests.get(tap_url, headers=head).json()
        #return country_info['countryCode'] + country_info['country']
        return country_info['countryCode']
    except Exception as e:#万能异常
        print(str(e) + 'Exception_出现异常')
        pass
        return '未知'

if "__name__==__main__":#主程序开始

    with open(f'{PATH}proxyip.txt', 'r', encoding='utf-8') as f:
        proxyip_all = f.read()
    proxyip_list = re.split(r'\n+',proxyip_all)
    #print('\n'.join(proxyip_list))

    with open(f'{PATH}proxyip_good.txt', 'r', encoding='utf-8') as f:
        proxyip_good_all = f.read()
    proxyip_good_list = re.split(r'\n+',proxyip_good_all)

    nowtime = datetime.today().strftime('%Y%m%d')

    
    newlist = []
    for ip in proxyip_list:
        t = False
        for good in proxyip_good_list:
            if ip in good and '--' in good:
                newip = good.split("--")[0]
                newip = newip + '--' + nowtime
                newlist.append(newip)
                t = True
                break
        if t == False:
            country_info = get_address(ip)
            ipinfo = ip + '#' + country_info + '======' + nowtime + '--' + nowtime
            newlist.append(ipinfo)
    #将IP分区域排序
    hkip = []
    sgip = []
    jpip = []
    krip = []
    other = []
    for ip in newlist:
        if '#hk' in ip or '#tw' in ip or 'cn' in ip or '#HK' in ip or '#TW' in ip or 'CN' in ip :
            hkip.append(ip)
        elif '#sg' in ip or '#SG' in ip :
            sgip.append(ip)
        elif '#jp' in ip or '#JP' in ip :
            jpip.append(ip)
        elif '#kr' in ip or '#KR' in ip :
            krip.append(ip)
        elif '======' in ip:
            other.append(ip)
    allip = []
    allip.append('#hk')
    allip.extend(hkip)
    allip.append('#sg')
    allip.extend(sgip)
    allip.append('#jp')
    allip.extend(jpip)
    allip.append('#kr')
    allip.extend(krip)
    allip.append('#other')
    allip.extend(other)
    allip_str = '\n'.join(allip)
    with open(f'{PATH}/proxyip_good.txt', 'w', encoding='utf-8') as f:
        f.write(allip_str)

    #更新到ipUrl.txt
    with open(IPURL, 'r', encoding='utf-8') as f:
        ipurl_all = f.read()
    ipurl_list = re.split(r'\n+',ipurl_all)
    plist = '\n'.join(ipurl_list)
    print(f"修改前:\n{plist}")
    for i in range(len(ipurl_list)):
        #如果内容是空
        if ipurl_list[i] == '':
            continue
        ip = re.findall(r'@(.*?):443',ipurl_list[i])
        #print(f'原ip = {ip}')
        if ip[0] not in allip:
            if 'hk.txt' in ipurl_list[i] or 'tw.txt' in ipurl_list[i] or 'cn.txt' in ipurl_list[i]::
                for goodip in allip:
                    if '#hk' in goodip and '======' in goodip:
                        use_ip = re.split(r'#hk',goodip)
                        ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                        #print(f'use_ip[0] = {use_ip[0]}')
                        #print(f"ipurl_list[i] = {ipurl_list[i]}")
                        break
            elif 'sg.txt' in ipurl_list[i]:
                for goodip in allip:
                    if '#sg' in goodip and '======' in goodip:
                        use_ip = re.split(r'#sg',goodip)
                        ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                        break
            elif 'jp.txt' in ipurl_list[i]:
                if any('#jp' in item for item in allip):
                    for goodip in allip:
                        if '#jp' in goodip and '======' in goodip:
                            use_ip = re.split(r'#jp',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
                else:
                    for goodip in allip:
                        if '#sg' in goodip and '======' in goodip:
                            use_ip = re.split(r'#sg',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
            elif 'kr.txt' in ipurl_list[i]:
                if any('#kr' in item for item in allip):
                    for goodip in allip:
                        if '#kr' in goodip and '======' in goodip:
                            use_ip = re.split(r'#kr',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
                else:
                    for goodip in allip:
                        if '#hk' in goodip and '======' in goodip:
                            use_ip = re.split(r'#hk',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
            elif 'us.txt' in ipurl_list[i]:
                if any('#us' in item for item in allip):
                    for goodip in allip:
                        if '#us' in goodip and '======' in goodip:
                            use_ip = re.split(r'#us',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
                else:
                    for goodip in allip:
                        if '#sg' in goodip and '======' in goodip:
                            use_ip = re.split(r'#sg',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break

    ipurl_list = '\n'.join(ipurl_list)
    print(f'修改后:\n{ipurl_list}')
    with open(IPURL, 'w', encoding='utf-8') as f:
        f.write(ipurl_list)
    
    #下面代码自己测速使用，可用删除
    #更新到'./ip/ipurl.txt'，用于自己测速IP时使用
    print(f'下面是自己测速时使用')
    with open('./ip/ipurl.txt', 'r', encoding='utf-8') as f:
        ipurl_all = f.read()
    ipurl_list = re.split(r'\n+',ipurl_all)
    plist = '\n'.join(ipurl_list)
    print(f"修改前:\n{plist}")
    for i in range(len(ipurl_list)):
        #如果内容是空
        if ipurl_list[i] == '':
            continue
        ip = re.findall(r'@(.*?):443',ipurl_list[i])
        #print(f'原ip = {ip}')
        if ip[0] not in allip:
            if 'hk.txt' in ipurl_list[i] or 'tw.txt' in ipurl_list[i] or 'cn.txt' in ipurl_list[i]:
                for goodip in allip:
                    if '#hk' in goodip and '======' in goodip:
                        use_ip = re.split(r'#hk',goodip)
                        ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                        #print(f'use_ip[0] = {use_ip[0]}')
                        #print(f"ipurl_list[i] = {ipurl_list[i]}")
                        break
            elif 'sg.txt' in ipurl_list[i]:
                for goodip in allip:
                    if '#sg' in goodip and '======' in goodip:
                        use_ip = re.split(r'#sg',goodip)
                        ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                        break
            elif 'jp.txt' in ipurl_list[i]:
                if any('#jp' in item for item in allip):
                    for goodip in allip:
                        if '#jp' in goodip and '======' in goodip:
                            use_ip = re.split(r'#jp',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
                else:
                    for goodip in allip:
                        if '#sg' in goodip and '======' in goodip:
                            use_ip = re.split(r'#sg',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
            elif 'kr.txt' in ipurl_list[i]:
                if any('#kr' in item for item in allip):
                    for goodip in allip:
                        if '#kr' in goodip and '======' in goodip:
                            use_ip = re.split(r'#kr',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
                else:
                    for goodip in allip:
                        if '#hk' in goodip and '======' in goodip:
                            use_ip = re.split(r'#hk',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
            elif 'us.txt' in ipurl_list[i]:
                if any('#us' in item for item in allip):
                    for goodip in allip:
                        if '#us' in goodip and '======' in goodip:
                            use_ip = re.split(r'#us',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break
                else:
                    for goodip in allip:
                        if '#sg' in goodip and '======' in goodip:
                            use_ip = re.split(r'#sg',goodip)
                            ipurl_list[i] = re.sub(ip[0],use_ip[0],ipurl_list[i])
                            break

    ipurl_list = '\n'.join(ipurl_list)
    print(f'修改后:\n{ipurl_list}')
    with open('./ip/ipurl.txt', 'w', encoding='utf-8') as f:
        f.write(ipurl_list)
