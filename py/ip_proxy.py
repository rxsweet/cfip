import re

PATH = './'
PROXYIP = f'{PATH}proxyip.txt'
IPURL = f'{PATH}ipurl.txt'
IPURL_TESTSPEED = f'{PATH}ip/ipurl.txt'


# =====================
# 解析 proxyip.txt
# =====================
def load_proxy():
    data = {}

    with open(PROXYIP, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # 提取 IP 和国家字段
            m = re.match(r'(.+?)#([A-Z_]+)', line)
            if not m:
                continue

            ip = m.group(1)
            country = m.group(2)

            # HK_US / HK_CN → HK
            if 'HK' in country or 'TW' in country or 'CN' in country:
                country = 'HK'
            elif 'SG' in country:
                country = 'SG'
            elif 'JP' in country:
                country = 'JP'
            elif 'KR' in country:
                country = 'KR'
            elif 'US' in country:
                country = 'US'
            else:
                country = 'OTHER'

            data[ip] = country

    return data


# =====================
# 更新 ipurl.txt
# =====================
def update_ipurl(ip_map, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [x.strip() for x in f if x.strip()]

    print("\n修改前:")
    print('\n'.join(lines))

    def replace_ip(old_ip, new_ip, line):
        return re.sub(old_ip, new_ip, line)

    for i, line in enumerate(lines):

        m = re.findall(r'@(.*?):443', line)
        if not m:
            continue

        old_ip = m[0]

        # 匹配规则（按文件）
        rules = {
            'hk.txt': ['HK', 'SG'],
            'tw.txt': ['HK', 'SG'],
            'cn.txt': ['HK', 'SG'],
            'sg.txt': ['SG', 'HK'],
            'jp.txt': ['JP', 'SG'],
            'kr.txt': ['KR', 'JP'],
            'us.txt': ['US', 'SG'],
        }

        for file_key, prefer_list in rules.items():

            if file_key not in line:
                continue

            # 找可用IP
            new_ip = None

            for cc in prefer_list:
                for ip, c in ip_map.items():
                    if c == cc:
                        new_ip = ip
                        break
                if new_ip:
                    break

            if new_ip:
                lines[i] = replace_ip(old_ip, new_ip, line)

            break

    print("\n修改后:")
    print('\n'.join(lines))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# =====================
# 主程序
# =====================
if __name__ == "__main__":

    ip_map = load_proxy()

    update_ipurl(ip_map, IPURL)
    update_ipurl(ip_map, IPURL_TESTSPEED)
