import os,re,requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed

# ========= 配置 =========

URLS=[
    "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/main/proxyList.txt",
    "https://raw.githubusercontent.com/mdsdtech/chonky-orange-cat/main/Orange/alivecat.txt",
    "https://raw.githubusercontent.com/afrcloud07/ListProxy/main/proxyip.txt",
    "https://raw.githubusercontent.com/papapapapdelesia/Emilia/main/Data/alive.txt",
    "https://raw.githubusercontent.com/SherlyKinan/proxy-check/main/active.txt",
    "https://raw.githubusercontent.com/NiREvil/vless/main/sub/country_proxies/03_proxies.txt",
    "https://raw.githubusercontent.com/exball/sing-box-config/Master/proxy-scaner/active-proxy-history.txt",
    "https://raw.githubusercontent.com/rxsweet/scan-proxyip/Master/proxy-scaner/active-proxy-history.txt",
    #"https://zip.cm.edu.kg/all.txt"
]


TARGET={"US","JP","KR","HK","SG"}
SAVE_DIR="ip"

DOWNLOAD_THREADS=12
GEO_THREADS=50

os.makedirs(SAVE_DIR,exist_ok=True)

# ========= Session =========

session=requests.Session()

# ========= 正则 =========

R1=re.compile(r"^(\d+\.\d+\.\d+\.\d+),(\d+),([A-Z]{2})")
R2=re.compile(r"^(\d+\.\d+\.\d+\.\d+):(\d+)#([A-Z]{2})")
R3=re.compile(r"^(\d+\.\d+\.\d+\.\d+)(?:\s+(\d+))?$")

# ========= 工具 =========

def save(name,data):
    with open(
        os.path.join(SAVE_DIR,name),
        "w",
        encoding="utf-8"
    ) as f:
        f.write("\n".join(data))

def fetch(url):
    try:
        return session.get(url,timeout=30).text.splitlines()
    except:
        return []

def query_country(ip):
    try:
        c=session.get(
            f"https://get.geojs.io/v1/ip/geo/{ip}.json",
            timeout=8
        ).json().get("country_code","").upper()
    except:
        c=""
    return ip,c

# ========= 主程序 =========

def main():

    print("下载数据中...")

    lines=[]

    with ThreadPoolExecutor(DOWNLOAD_THREADS) as pool:
        for data in pool.map(fetch,URLS):
            lines.extend(data)

    print(f"总行数: {len(lines)}")

    ip_data={}
    need_query={}
    query_ips=set()

    # ========= 第一轮解析 =========

    for line in lines:

        line=line.strip()
        if not line:
            continue

        m=R1.match(line)
        if m:
            ip,port,country=m.groups()
            ip_data[ip]=(int(port),country.upper())
            continue

        m=R2.match(line)
        if m:
            ip,port,country=m.groups()
            ip_data[ip]=(int(port),country.upper())
            continue

        m=R3.match(line)
        if m:
            ip,port=m.groups()
            port=int(port or 443)

            old=need_query.get(ip)

            if not old:
                need_query[ip]=port
            elif old!=443 and port==443:
                need_query[ip]=443

            query_ips.add(ip)

    # ========= 查询归属 =========

    total_query=len(query_ips)

    print(f"需要查询归属地IP: {total_query}")

    country_cache={}
    done=0

    if total_query:

        with ThreadPoolExecutor(GEO_THREADS) as pool:

            futures=[
                pool.submit(query_country,ip)
                for ip in query_ips
            ]

            for future in as_completed(futures):

                ip,country=future.result()
                country_cache[ip]=country

                done+=1

                if (
                    done<=20
                    or done%100==0
                    or done==total_query
                ):
                    pct=done*100/total_query

                    print(
                        f"\r归属查询: "
                        f"{done}/{total_query} "
                        f"({pct:.1f}%)",
                        end="",
                        flush=True
                    )

        print()

    # ========= 合并数据 =========

    for ip,port in need_query.items():

        country=country_cache.get(ip,"")

        if not country:
            continue

        old=ip_data.get(ip)

        if old:
            if old[0]!=443 and port==443:
                ip_data[ip]=(port,country)
        else:
            ip_data[ip]=(port,country)

    # ========= 过滤国家 =========

    raw=defaultdict(list)
    us443=[]
    nonus443=[]

    for ip,(port,country) in ip_data.items():

        if country not in TARGET:
            continue

        raw[country].append((ip,port))

        if port==443:
            if country=="US":
                us443.append(ip)
            else:
                nonus443.append(ip)

    # ========= 输出 =========

    allip=[]
    total=0

    for country in sorted(TARGET):

        items=sorted(
            raw[country],
            key=lambda x:(
                tuple(map(int,x[0].split("."))),
                x[1]
            )
        )

        result=[
            f"{ip}:{port}#{country}_{i}"
            for i,(ip,port) in enumerate(items,1)
        ]

        save(
            f"{country.lower()}.txt",
            result
        )

        allip.extend(result)
        total+=len(result)

        print(f"{country}: {len(result)}")

    save("allip.txt",allip)
    save("us443.txt",sorted(set(us443)))
    save("port443.txt",sorted(set(nonus443)))

    # ========= 统计 =========

    print("-"*40)
    print(f"唯一IP: {total}")
    print(f"US443: {len(set(us443))}")
    print(f"非US443: {len(set(nonus443))}")
    print(f"查询归属IP: {total_query}")
    print(f"输出目录: {os.path.abspath(SAVE_DIR)}")

if __name__=="__main__":
    main()
