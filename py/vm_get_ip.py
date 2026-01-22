import os
import requests


ip_Api_links = [
    #Mingyu维护
    'https://ipdb.api.030101.xyz/?type=bestcf&country=true',
    'https://ipdb.api.030101.xyz/?type=bestproxy&country=true',
    #CM维护
    'https://addressesapi.090227.xyz/ct',
    'https://addressesapi.090227.xyz/cmcc',
    'https://addressesapi.090227.xyz/CloudFlareYes',
    'https://addressesapi.090227.xyz/ip.164746.xyz',
    #第三方维护
    #'https://stock.hostmonit.com/CloudFlareYes，https://ip.164746.xyz',
    #OTC维护
    #'https://cn.xxxxxxxx.tk/',
    #'https://ct.xxxxxxxx.tk/',
    #'https://cm.xxxxxxxx.tk/',
    #'https://cu.xxxxxxxx.tk/'
    ]

ip_file = './addressesapi.txt'

def fetchIP(ip_Api_links):
    all_IP = []
    for link in ip_Api_links:
        response = requests.get(link)
        ip_text = response.text
        all_IP.append(ip_text)
    return all_IP

def main():
    fetch_all_IP = fetchIP(ip_Api_links)
    # 将列表内容，以行写入字符串
    str_all_ip = '\n'.join(fetch_all_IP) 
    print(str_all_ip)
    with open(ip_file, 'w') as f:
        f.write(str_all_ip)
        f.close()



if __name__ == "__main__":
    main()
