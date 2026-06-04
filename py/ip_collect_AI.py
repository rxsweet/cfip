import os
import re
import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# ======================
# 配置
# ======================

URLS = [
    "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
    "https://raw.githubusercontent.com/mdsdtech/chonky-orange-cat/refs/heads/main/Orange/alivecat.txt",
    "https://raw.githubusercontent.com/afrcloud07/ListProxy/refs/heads/main/proxyip.txt",
    "https://raw.githubusercontent.com/papapapapdelesia/Emilia/refs/heads/main/Data/alive.txt",
    "https://raw.githubusercontent.com/SherlyKinan/proxy-check/refs/heads/main/active.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/active-proxy-history.txt",
    "https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/country_proxies/03_proxies.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/proxy_list/proxyList_HK.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/proxy_list/proxyList_JP.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/proxy_list/proxyList_SG.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/proxy_list/proxyList_KR.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/proxy_list/proxyList_US.txt",
    "https://zip.cm.edu.kg/all.txt",
]

TARGET_COUNTRIES = {"US", "JP", "KR", "HK", "SG"}

SAVE_DIR = "ip"
os.makedirs(SAVE_DIR, exist_ok=True)

# ======================
# 缓存
# ======================

country_cache = {}
lock_cache = set()

ip_data = {}  # ip -> {country, port}

# ======================
# GeoJS 查询
# ======================

def get_country(ip):
    if ip in country_cache:
        return country_cache[ip]

    try:
        r = requests.get(
            f"https://get.geojs.io/v1/ip/geo/{ip}.json",
            timeout=10
        )
        country = r.json().get("country_code", "").upper()
    except:
        country = ""

    country_cache[ip] = country
    return country

# ======================
# 解析函数
# ======================

re_format1 = re.compile(r"^(\d+\.\d+\.\d+\.\d+),(\d+),([A-Z]{2})")
re_format2 = re.compile(r"^(\d+\.\d+\.\d+\.\d+):(\d+)#([A-Z]{2})")
re_format3 = re.compile(r"^(\d+\.\d+\.\d+\.\d+)(?:\s+(\d+))?$")

def parse_line(line):
    line = line.strip()
    if not line:
        return []

    results = []

    # format1
    m = re_format1.match(line)
    if m:
        ip, port, country = m.groups()
        results.append((ip, int(port), country))
        return results

    # format2
    m = re_format2.match(line)
    if m:
        ip, port, country = m.groups()
        results.append((ip, int(port), country))
        return results

    # format3
    m = re_format3.match(line)
    if m:
        ip, port = m.groups()
        port = int(port) if port else 443
        country = get_country(ip)
        if country:
            results.append((ip, port, country))
        return results

    return []

# ======================
# 下载单个源
# ======================

def fetch(url):
    try:
        r = requests.get(url, timeout=30)
        return r.text.splitlines()
    except:
        return []

# ======================
# 主处理
# ======================

def main():
    print("下载数据中...")

    lines = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        for res in pool.map(fetch, URLS):
            lines.extend(res)

    print(f"总行数: {len(lines)}")

    # 解析
    for line in lines:
        for ip, port, country in parse_line(line):

            if country not in TARGET_COUNTRIES:
                continue

            # 去重 + 443优先
            if ip in ip_data:
                old = ip_data[ip]

                if old["port"] != 443 and port == 443:
                    ip_data[ip] = {"port": port, "country": country}
                continue

            ip_data[ip] = {"port": port, "country": country}

    # ======================
    # 分类
    # ======================

    by_country = defaultdict(list)
    port443_non_us = []
    us443 = []

    for ip, info in ip_data.items():
        country = info["country"].lower()
        port = info["port"]

        line = f"{ip}:{port}#{country}"
        by_country[country].append(line)

        # 443分类
        if port == 443:
            if country == "us":
                us443.append(ip)
            else:
                port443_non_us.append(ip)

    # ======================
    # 保存国家文件
    # ======================

    for c in sorted(TARGET_COUNTRIES):
        c_low = c.lower()
        path = os.path.join(SAVE_DIR, f"{c_low}.txt")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(by_country[c_low])))

        print(f"{c_low}.txt -> {len(by_country[c_low])}")

    # ======================
    # allip.txt
    # ======================

    all_list = []
    for c in sorted(TARGET_COUNTRIES):
        c_low = c.lower()
        all_list.extend(sorted(by_country[c_low]))

    with open(os.path.join(SAVE_DIR, "allip.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_list))

    # ======================
    # port443 非US
    # ======================

    with open(os.path.join(SAVE_DIR, "port443.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(set(port443_non_us))))

    # ======================
    # US 443
    # ======================

    with open(os.path.join(SAVE_DIR, "us443.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(set(us443))))

    # ======================
    # 统计
    # ======================

    print("\n完成统计:")
    print(f"唯一IP: {len(ip_data)}")
    print(f"US443: {len(us443)}")
    print(f"非US 443: {len(port443_non_us)}")
    print(f"输出目录: {os.path.abspath(SAVE_DIR)}")


if __name__ == "__main__":
    main()
