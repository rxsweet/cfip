import re
from datetime import datetime

PATH = './ip_proxy/'
    
if "__name__==__main__":#主程序开始
    
    with open(f'{PATH}proxyip.txt', 'r', encoding='utf-8') as f:
        proxyip_all = f.read()
    proxyip_list = re.split(r'\n+',proxyip_all)

    with open(f'{PATH}proxyip_good.txt', 'r', encoding='utf-8') as f:
        proxyip_good_all = f.read()
    proxyip_good_list = re.split(r'\n+',proxyip_good_all)

    nowtime = datetime.today().strftime('%Y%m%d')

    newip= []
    for ip in proxyip_list:
        t = False
        for i in range(len(proxyip_good_list)):
            if ip in proxyip_good_list[i] and '--' in proxyip_good_list[i]:
                base = proxyip_good_list[i].split("--")[0]
                proxyip_good_list[i] = base + '--' + nowtime
                print(proxyip_good_list[i])
                t = True
                break
            #print(proxyip_good_list[i])
        if t == False:
            print(ip)
            newip.append(ip + '#' + nowtime + '--')
    #去重后保存
    proxyip_good_list.extend(newip)
    proxyip_good_list = '\n'.join(proxyip_good_list)
    with open(f'{PATH}/proxyip_good.txt', 'w', encoding='utf-8') as f:
        f.write(proxyip_good_list)
