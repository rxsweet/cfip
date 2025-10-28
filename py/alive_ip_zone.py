import re

PATH = './'
ALIVE = f'{PATH}aliveip.txt'

#ip列表去重
def ip_list_rm(urlList):#列表去重
    begin = 0
    rm = 0
    length = len(urlList)
    print(f'-----去重开始-----')
    while begin < length:
        proxy_compared = urlList[begin]
        begin_2 = begin + 1
        repeat = 0 #单个重复数
        while begin_2 <= (length - 1):
            ip = re.split(r':',urlList[begin_2])
            if ip[0] in proxy_compared:
                urlList.pop(begin_2)
                length -= 1
                begin_2 -= 1
                rm += 1
                repeat = repeat + 1
            begin_2 += 1
        #给去重后的元素添加重复数
        if repeat > 0:
            #判断有#号备注，再添加
            if '#' in urlList[begin]:
                urlList[begin]= urlList[begin] + '_'+ str(repeat)
        begin += 1
    print(f'重复数量 {rm}')
    print(f'剩余总数 {str(len(urlList))}\n-----去重结束-----')
    return urlList



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
    ip_list = ip_list_rm(ip_list)
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
    
    
