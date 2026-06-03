import os
import requests
from concurrent.futures import ThreadPoolExecutor

# ================= 配置 =================

# 元素名 -> 国家代码
IP_LIST = {
    'hk': 'HK',
    'sg': 'SG',
    'kr': 'KR',
    'jp': 'JP',
    'us': 'US',
}

# 数据源
URLS = [
    "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
    "https://raw.githubusercontent.com/mdsdtech/chonky-orange-cat/refs/heads/main/Orange/alivecat.txt",
    "https://raw.githubusercontent.com/afrcloud07/ListProxy/refs/heads/main/proxyip.txt",
    "https://raw.githubusercontent.com/papapapapdelesia/Emilia/refs/heads/main/Data/alive.txt",
    "https://raw.githubusercontent.com/SherlyKinan/proxy-check/refs/heads/main/active.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/active-proxy-history.txt",
]
"""
URLS = [
    "https://ghraw.eu.org/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
    "https://ghraw.eu.org/mdsdtech/chonky-orange-cat/refs/heads/main/Orange/alivecat.txt",
    "https://ghraw.eu.org/afrcloud07/ListProxy/refs/heads/main/proxyip.txt",
    "https://ghraw.eu.org/papapapapdelesia/Emilia/refs/heads/main/Data/alive.txt",
    "https://ghraw.eu.org/SherlyKinan/proxy-check/refs/heads/main/dead.txt",
    "https://ghraw.eu.org/SherlyKinan/proxy-check/refs/heads/main/active.txt",
]
"""

# 保存目录
SAVE_DIR = "./ip/rx"

# ================= 网络请求 =================

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


def fetch(url):
    """
    下载文本内容
    """
    try:
        return session.get(url, timeout=20).text
    except Exception as e:
        print(f"[失败] {url} -> {e}")
        return ""


# ================= 数据处理 =================

def parse(text, result, country_map):
    """
    解析代理列表

    格式:
    IP,PORT,COUNTRY,...

    转换:
    IP:PORT#元素名

    同IP自动去重
    """
    for line in text.splitlines():

        try:
            ip, port, country, *_ = map(str.strip, line.split(","))
        except ValueError:
            continue

        name = country_map.get(country.upper())
        if not name:
            continue

        # 同IP仅保留第一条
        result[name].setdefault(
            ip,
            f"{ip}:{port}#{name}"
        )


def save(result):
    """
    保存国家文件及总文件
    """
    os.makedirs(SAVE_DIR, exist_ok=True)

    all_ips = []

    for name, ips in result.items():

        data = sorted(ips.values())
        all_ips.extend(data)

        with open(
            f"{SAVE_DIR}/{name}.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write("\n".join(data))

        print(f"{name}.txt -> {len(data)}")

    # 汇总文件
    all_ips = sorted(set(all_ips))

    with open(
        f"{SAVE_DIR}/allip.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write("\n".join(all_ips))

    print(f"allip.txt -> {len(all_ips)}")


# ================= 主程序 =================

def main():

    # 国家代码 -> 元素名
    country_map = {
        v: k
        for k, v in IP_LIST.items()
    }

    # 存储结果
    result = {
        k: {}
        for k in IP_LIST
    }

    # 并发下载
    with ThreadPoolExecutor(max_workers=len(URLS)) as pool:

        for text in pool.map(fetch, URLS):
            parse(text, result, country_map)

    save(result)

    print("完成")


if __name__ == "__main__":
    main()
