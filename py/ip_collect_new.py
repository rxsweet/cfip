import os
import requests
from concurrent.futures import ThreadPoolExecutor

iplist = {
    'hk': 'HK',
    'sg': 'SG',
    'kr': 'KR',
    'jp': 'JP',
    'us': 'US',
}


urls = [
    "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
    "https://raw.githubusercontent.com/mdsdtech/chonky-orange-cat/refs/heads/main/Orange/alivecat.txt",
    "https://raw.githubusercontent.com/afrcloud07/ListProxy/refs/heads/main/proxyip.txt",
    "https://raw.githubusercontent.com/papapapapdelesia/Emilia/refs/heads/main/Data/alive.txt",
    "https://raw.githubusercontent.com/SherlyKinan/proxy-check/refs/heads/main/dead.txt",
    "https://raw.githubusercontent.com/SherlyKinan/proxy-check/refs/heads/main/active.txt",
]
"""
urls = [
    "https://ghraw.eu.org/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
    "https://ghraw.eu.org/mdsdtech/chonky-orange-cat/refs/heads/main/Orange/alivecat.txt",
    "https://ghraw.eu.org/afrcloud07/ListProxy/refs/heads/main/proxyip.txt",
    "https://ghraw.eu.org/papapapapdelesia/Emilia/refs/heads/main/Data/alive.txt",
    "https://ghraw.eu.org/SherlyKinan/proxy-check/refs/heads/main/dead.txt",
    "https://ghraw.eu.org/SherlyKinan/proxy-check/refs/heads/main/active.txt",
]
"""
SAVE_DIR = "./ip/rx"
os.makedirs(SAVE_DIR, exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

result = {k: {} for k in iplist}


def fetch(url):
    try:
        print("获取:", url)
        return session.get(url, timeout=20).text
    except Exception as e:
        print("失败:", url, e)
        return ""


with ThreadPoolExecutor(max_workers=10) as pool:
    for text in pool.map(fetch, urls):

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")

            if len(parts) < 3:
                continue

            ip = parts[0].strip()
            port = parts[1].strip()
            country = parts[2].strip().upper()

            for name, code in iplist.items():

                if country != code:
                    continue

                # 按IP去重
                if ip not in result[name]:
                    result[name][ip] = f"{ip}:{port}#{name}"

                break

for name, ips in result.items():

    outfile = os.path.join(SAVE_DIR, f"{name}.txt")

    with open(outfile, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(ips.values())))

    print(f"{name}.txt -> {len(ips)} 条")

print("完成")
