import re
from datetime import datetime
import requests
from collections import defaultdict

PATH = './'
PROXYIP = f'{PATH}proxyip.txt'
GOOD_PROXYIP = f'{PATH}proxyip_good.txt'
IPURL = f'{PATH}ipurl.txt'
IPURL_TESTSPEED = f'{PATH}ip/ipurl.txt'

session = requests.Session()

# =====================
# IP归属查询
# =====================
#f'https://ip125.com/api/{ip}?lang=zh-CN'
#f'https://api.ip.sb/geoip/{ip}'
def get_address(ip):
    try:
        return session.get(
            f'http://ip-api.com/json/{ip}?lang=zh-CN',
            timeout=8
        ).json().get('countryCode', '未知')
    except:
        return '未知'

# =====================
# 更新 good proxy
# =====================
def update_goodproxyip():
    with open(PROXYIP, 'r', encoding='utf-8') as f:
        proxy_list = [x.strip() for x in f.read().splitlines() if x.strip()]

    with open(GOOD_PROXYIP, 'r', encoding='utf-8') as f:
        good_list = [x.strip() for x in f.read().splitlines() if x.strip()]

    now = datetime.today().strftime('%Y%m%d')
    newlist = []

    # ===== 更新 or 新增 =====
    for ip in proxy_list:
        found = False

        for g in good_list:
            if ip in g and '--' in g:
                base = g.split("--")[0]
                newlist.append(base + '--' + now)
                found = True
                break

        if not found:
            cc = get_address(ip)
            newlist.append(f"{ip}#{cc}======{now}--{now}")

    # ===== 分组 =====
    groups = defaultdict(list)

    for x in newlist:
        if '#HK' in x or '#TW' in x or '#CN' in x:
            groups['HK'].append(x)
        elif '#SG' in x:
            groups['SG'].append(x)
        elif '#JP' in x:
            groups['JP'].append(x)
        elif '#KR' in x:
            groups['KR'].append(x)
        elif '#US' in x:
            groups['US'].append(x)
        else:
            groups['OTHER'].append(x)

    # ===== 输出 =====
    out = []

    for k in ['HK', 'SG', 'JP', 'KR', 'US']:
        out.append(f'#{k.lower()}')
        out.extend(groups[k])

    out.append('#other')
    out.extend(groups['OTHER'])

    with open(GOOD_PROXYIP, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))


# =====================
# 更新 ipurl.txt
# =====================
def up_goodip_to_ipUrl(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        ipurl = [x.strip() for x in f if x.strip()]

    with open(GOOD_PROXYIP, 'r', encoding='utf-8') as f:
        good = [x.strip() for x in f if x.strip()]

    print("修改前:")
    print('\n'.join(ipurl))

    def pick_ip(tag):
        for g in good:
            if tag in g and '======' in g:
                return g.split(tag)[0]
        return None

    for i, line in enumerate(ipurl):

        m = re.findall(r'@(.*?):443', line)
        if not m:
            continue

        old_ip = m[0]

        # ===== 国家映射（核心优化点）=====
        rules = [
            ('hk.txt', 'HK', None),
            ('tw.txt', 'HK', None),
            ('cn.txt', 'HK', None),
            ('sg.txt', 'SG', None),
            ('jp.txt', 'JP', 'SG'),
            ('kr.txt', 'KR', 'JP'),
            ('us.txt', 'US', 'SG')
        ]

        for file_key, primary, fallback in rules:

            if file_key not in line:
                continue

            target = primary if any(primary in g for g in good) else fallback

            if not target:
                break

            new_ip = pick_ip(f'#{target}')
            if new_ip:
                ipurl[i] = re.sub(old_ip, new_ip, line)
            break

    print("修改后:")
    print('\n'.join(ipurl))

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ipurl))


# =====================
# 主程序
# =====================
if __name__ == "__main__":
    update_goodproxyip()
    up_goodip_to_ipUrl(IPURL)
    up_goodip_to_ipUrl(IPURL_TESTSPEED)
