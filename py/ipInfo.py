import re
import requests
import json

#SOURCE = 'ip.txt'
SOURCE = './ip/checked/node_ip.txt'
SAVE_PATH = './ip/area/'

#要筛选哪个地区直接在此添加
IP_YAML = {
    'allip':[],
    'hk':[],
    'tw':[],
    'jp':[],
    'sg':[],
    'kr':[],
    'us':[],
    'other':[],
}

def get_address(ip):#得到IP归属地
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

    with open(SOURCE, 'r', encoding='utf-8') as f:
        ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)
    #去重
    ip_list = list_rm(ip_list)
    
    #去重后保存
    #ip_rm = '\n'.join(ip_list)
    #with open(f'./ip/ip_rm.txt', 'w', encoding='utf-8') as f:
        #f.write(ip_rm)

    #查询IP区域
    for ip in ip_list:
        try:
            if ip == '':#如果是空跳过
                continue
            ipaddr = ip.split("#")[0]
            if ':' in ipaddr:
                ipaddr = ip.split(":")[0]
            #print(ipaddr)
            country_info = get_address(ipaddr)
            if country_info in IP_YAML:
                ipinfo = ip + '#' + country_info
                IP_YAML[country_info].append(ipinfo)
            else:
                ipinfo = ip + '#' + country_info + '_other'
                IP_YAML['other'].append(ipinfo)
            
            IP_YAML['allip'].append(ipinfo)#需要按国家排序的话,使用下面的for
            print(ipinfo)
        except Exception as e:#万能异常
            print(f'{ip}出现错误,错误内容如下：\n{e}')
            pass
    #按地区排序
    """
    for key,value in IP_YAML.items():
        if key != 'allip':
            IP_YAML['allip'].extend(value)
    """
    #保存IP
    for key,value in IP_YAML.items():
        value = '\n'.join(value)
        with open(f'{SAVE_PATH}{key}.txt', 'w', encoding='utf-8') as f:
            f.write(value)
