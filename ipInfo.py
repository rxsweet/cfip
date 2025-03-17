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


if "__name__==__main__":#主程序开始

    with open('ip.txt', 'r', encoding='utf-8') as f:
        ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)
    
    ALLIP = []
    HKIP = []
    SGIP = []
    CAIP = []
    USIP = []
    KRIP = []
    RUIP = []
    GBIP = []
    NLIP = []
    DEIP = []
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
            elif country_info == 'SG':
                SGIP.append(ip_list[i])
            elif country_info == 'CA':
                CAIP.append(ip_list[i])
            elif country_info == 'US':
                USIP.append(ip_list[i])
            elif country_info == 'KR':
                KRIP.append(ip_list[i])
            elif country_info == 'RU':
                RUIP.append(ip_list[i])
            elif country_info == 'GB':
                GBIP.append(ip_list[i])
            elif country_info == 'NL':
                NLIP.append(ip_list[i])
            elif country_info == 'DE':
                DEIP.append(ip_list[i])
            else:
                ip_list[i] = ip_list[i] + '_other'
                otherIP.append(ip_list[i])
            ALLIP.append(ip_list[i])#需要按国家排序的话,#号掉这个开启下面的"""
            print(ip_list[i])
        except Exception as e:#万能异常
            print(f'{ip_list[i]}出现错误,错误内容如下：\n{e}')
            pass

    """
    #按国家顺序排列
    ALLIP = []
    ALLIP.extend(HKIP)
    ALLIP.extend(SGIP)
    ALLIP.extend(CAIP)
    ALLIP.extend(USIP)
    ALLIP.extend(RUIP)
    ALLIP.extend(KRIP)
    ALLIP.extend(GBIP)
    ALLIP.extend(NLIP)
    ALLIP.extend(DEIP)
    ALLIP.extend(otherIP)
    """
    
    ALLIP = '\n'.join(ALLIP)
    with open(f'./ip/ALLIP.txt', 'w', encoding='utf-8') as f:
        f.write(ALLIP)
    #按区域保存
    HKIP = '\n'.join(HKIP)
    with open(f'./ip/HKIP.txt', 'w', encoding='utf-8') as f:
        f.write(HKIP)
    SGIP = '\n'.join(SGIP)
    with open(f'./ip/SGIP.txt', 'w', encoding='utf-8') as f:
        f.write(SGIP)
    USIP = '\n'.join(USIP)
    with open(f'./ip/USIP.txt', 'w', encoding='utf-8') as f:
        f.write(USIP)
    KRIP = '\n'.join(KRIP)
    with open(f'./ip/KRIP.txt', 'w', encoding='utf-8') as f:
        f.write(KRIP)
