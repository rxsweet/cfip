import os
import requests
from concurrent.futures import ThreadPoolExecutor

# ================= 配置区 =================

IP_MAP = {
    "hk": "HK",
    "sg": "SG",
    "kr": "KR",
    "jp": "JP",
    "us": "US",
}

URLS = [
    "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
    "https://raw.githubusercontent.com/mdsdtech/chonky-orange-cat/refs/heads/main/Orange/alivecat.txt",
    "https://raw.githubusercontent.com/afrcloud07/ListProxy/refs/heads/main/proxyip.txt",
    "https://raw.githubusercontent.com/papapapapdelesia/Emilia/refs/heads/main/Data/alive.txt",
    "https://raw.githubusercontent.com/SherlyKinan/proxy-check/refs/heads/main/active.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/refs/heads/Master/proxy-scaner/active-proxy-history.txt",
]

SAVE_DIR = "./ip/rx"
os.makedirs(SAVE_DIR, exist_ok=True)

# ================= 网络层 =================

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})


def fetch(url):
    """下载文本"""
    try:
        return session.get(url, timeout=20).text
    except:
        return ""


# ================= 解析 + 收集 =================

def build_country_map():
    """SG -> sg 映射"""
    return {v: k for k, v in IP_MAP.items()}


def process_line(line, country_map, result):
    """解析单行数据"""
    try:
        ip, port, country, *_ = map(str.strip, line.split(","))
    except:
        return

    name = country_map.get(country.upper())
    if not name:
        return

    # IP去重
    result[name].setdefault(ip, f"{ip}:{port}#{name}")


def collect():
    """主收集逻辑"""
    country_map = build_country_map()
    result = {k: {} for k in IP_MAP}

    with ThreadPoolExecutor(max_workers=len(URLS)) as pool:
        for text in pool.map(fetch, URLS):
            for line in text.splitlines():
                process_line(line, country_map, result)

    return result


# ================= 保存逻辑 =================

def save_files(result):
    """保存所有文件"""

    all_ips = []
    port443_all = []
    us443 = []

    # 遍历国家
    for name, data in result.items():

        lines = sorted(data.values())
        all_ips.extend(lines)

        with open(f"{SAVE_DIR}/{name}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        # 统计443
        for line in lines:
            try:
                ip_port = line.split("#")[0]
                ip, port = ip_port.split(":")
            except:
                continue

            if port == "443":

                if name == "us":
                    us443.append(line)
                else:
                    port443_all.append(line)

        print(f"{name}.txt -> {len(lines)}")

    # ===== allip 去重 =====
    all_ips = sorted(set(all_ips))
    port443_all = sorted(set(port443_all))
    us443 = sorted(set(us443))

    # ===== 写文件 =====
    def write(name, data):
        with open(f"{SAVE_DIR}/{name}", "w", encoding="utf-8") as f:
            f.write("\n".join(data))

    write("allip.txt", all_ips)
    write("port443.txt", port443_all)
    write("us443.txt", us443)

    print(f"allip.txt -> {len(all_ips)}")
    print(f"port443.txt -> {len(port443_all)}")
    print(f"us443.txt -> {len(us443)}")


# ================= 主程序 =================

def main():
    result = collect()
    save_files(result)
    print("完成")


if __name__ == "__main__":
    main()
