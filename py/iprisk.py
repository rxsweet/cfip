import re
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ================= 配置 =================

SOURCE_URL = (
    #"https://ghraw.eu.org/rxsweet/cfip/refs/heads/main/ip/port443.txt"
    #"https://ghraw.eu.org/rxsweet/cfip/refs/heads/main/ip/us443.txt"
    "https://ips.1985.de5.net"
)

MAX_WORKERS = 50

# iprisk页面表格匹配
TD_RE = re.compile(
    r"<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>",
    re.S
)

# ================= 网络 =================

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


# ================= 功能函数 =================

score_re = re.compile(r"\((\d+)/100")
def get_score(line):
    m = score_re.search(line)
    return int(m.group(1)) if m else -1
    
def get_ip_list():
    """
    获取IP列表
    """
    text = session.get(SOURCE_URL, timeout=30).text

    ips = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        try:
            ip = line.split(":", 1)[0]
            ips.append((ip, line))
        except:
            pass

    return ips


def parse_iprisk(ip):
    """
    查询iprisk.top
    返回:
    [国家][(纯净度_风险等级)(IP类型)]
    """

    try:

        html = session.get(
            f"https://iprisk.top/ip/{ip}",
            timeout=15
        ).text

        data = {
            re.sub(r"<.*?>", "", k).strip():
            re.sub(r"<.*?>", "", v).strip()
            for k, v in TD_RE.findall(html)
        }

        cc = data.get("国家", "UN")
        clean = data.get("纯净度评分", "0/100")
        risk = data.get("风险等级", "Unknown")
        typ = data.get("IP 类型", "Unknown")

    except Exception:

        cc = "UN"
        clean = "0/100"
        risk = "Unknown"
        typ = "Unknown"

    return f"[{cc}][({clean}_{risk})({typ})]"


def process(item):
    """
    单IP处理
    """

    ip, raw_line = item

    info = parse_iprisk(ip)

    return f"{raw_line} {info}"


def save(lines):
    """
    保存结果
    """

    outfile = datetime.now().strftime(
        "%Y_%m_%d_%H_%M_%S.txt"
    )

    with open(
        outfile,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("\n".join(lines))

    print(f"\n保存完成 -> {outfile}")
    print(f"总数: {len(lines)}")


# ================= 主程序 =================

def main():

    ips = get_ip_list()

    print(f"获取IP: {len(ips)}")

    results = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as pool:

        for i, line in enumerate(
            pool.map(process, ips),
            1
        ):
            if line:
                results.append(line)

            print(
                f"\r处理中 {i}/{len(ips)}",
                end=""
            )

    # 分数高→低排序
    results.sort(
        key=get_score,
        reverse=True
    )

    save(results)

if __name__ == "__main__":
    main()
