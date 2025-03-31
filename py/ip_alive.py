import re

PATH = './ip/'
    
if "__name__==__main__":#主程序开始

    with open(f'{PATH}ALLIP.txt', 'r', encoding='utf-8') as f:
        ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)

    with open(f'{PATH}node.txt', 'r', encoding='utf-8') as f:
        ip_node_all = f.read()
    ip_node_list = re.split(r'\n+',ip_node_all)
    
    alive_ip = []
    for ip in ip_list:
        if ip == '':
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
    #去重后保存
    alive_ip = '\n'.join(alive_ip)
    with open(f'{PATH}/checked/node_ip.txt', 'w', encoding='utf-8') as f:
        f.write(alive_ip)
    
