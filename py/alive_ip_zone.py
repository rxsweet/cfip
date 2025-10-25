import re

PATH = './'
ALIVE = f'{PATH}aliveip.txt'
    
if "__name__==__main__":#主程序开始
    ipfiles = {
    'hk':[],
    'jp':[],
    'kr':[],
    'sg':[],
    'us':[],
    }
    with open(ALIVE, 'r', encoding='utf-8') as f:
        ip_all = f.read()
    ip_list = re.split(r'\n+',ip_all)

    for key,value in ipfiles.items():
        for ip in ip_list: 
            if key in ip:
                value.append(ip)
            if key == 'hk':
                if 'tw' in ip or 'cn' in ip:
                    value.append(ip)
        ipall = '\n'.join(value)
        with open(f'{PATH}{key}.txt', 'w', encoding='utf-8') as f:
            f.write(ipall)
        print(f'可用 {key}.txt 写入完成！\n')
    #保存allIP
    ip_list = '\n'.join(ip_list)
    with open(f'{PATH}all.txt', 'w', encoding='utf-8') as f:
        f.write(ip_list)
    print(f'可用 all.txt 写入完成！\n')
