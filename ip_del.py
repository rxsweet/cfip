import re

if "__name__==__main__":#主程序开始

    with open('./ip/ALLIP.txt', 'r', encoding='utf-8') as f:
        ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)

    with open('ip_node.txt', 'r', encoding='utf-8') as f:
        ip_node_all = f.read()
    ip_node_list = re.split(r'\n+',ip_node_all)
    
    new_ip_list = []
    for ip in ip_list:
        if ip == '':
            continue
        if '#' in ip:
            ipaddr = ip.split("#")[0]
        else:
            ipaddr = ip
        for node in ip_node_list:
            if ipaddr in node:
                new_ip_list.append(ip)
                print(ip)
                continue
    #去重后保存
    ip_del = '\n'.join(new_ip_list)
    with open(f'./ip/ip_node.txt', 'w', encoding='utf-8') as f:
        f.write(ip_del)
    
