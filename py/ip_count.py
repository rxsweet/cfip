# ip_count.py   
import os
from collections import Counter

# 当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 存放 aliveip_*.txt 文件的子目录
ALIVEIP_DIR = os.path.join(BASE_DIR, "aliveip")

# 输出文件也放在 aliveip 文件夹下
OUTPUT_FILE = os.path.join(ALIVEIP_DIR, "ip_good.txt")

# 支持的国家/地区前缀（小写）
COUNTRY_PREFIXES = {"hk", "jp", "kr", "sg", "us", "ca"}

def main():
    if not os.path.isdir(ALIVEIP_DIR):
        print(f"错误：目录不存在 → {ALIVEIP_DIR}")
        print("请先创建 aliveip 文件夹，并把 aliveip_ 开头的 txt 文件放进去")
        return

    ip_counter = Counter()
    ip_lines = {}  # ip:port → 原始整行（第一次出现的）

    # 1. 读取 aliveip 文件夹下所有以 aliveip_ 开头的 .txt 文件
    for filename in os.listdir(ALIVEIP_DIR):
        if not filename.startswith("aliveip_") or not filename.endswith(".txt"):
            continue

        filepath = os.path.join(ALIVEIP_DIR, filename)
        print(f"正在处理: {filename}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '#' not in line:
                        continue

                    ip_port_part, _ = line.split('#', 1)
                    ip_port_part = ip_port_part.strip()

                    if ':' not in ip_port_part:
                        continue

                    ip_counter[ip_port_part] += 1
                    if ip_port_part not in ip_lines:
                        ip_lines[ip_port_part] = line

        except Exception as e:
            print(f"处理 {filename} 时出错: {e}")

    # 2. 按国家分组，只保留出现次数 >= 2 的
    country_groups = {k: [] for k in COUNTRY_PREFIXES}

    for ip_port, count in ip_counter.most_common():
        if count < 2:
            continue

        original_line = ip_lines.get(ip_port, ip_port)
        new_line = f"{original_line}+{count}"

        found = False
        lower_line = original_line.lower()
        for prefix in COUNTRY_PREFIXES:
            if f"#{prefix}_" in lower_line:
                country_groups[prefix].append(new_line)
                found = True
                break

    # 3. 写入文件（保存到 aliveip/ip_good.txt）
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        wrote_anything = False
        for country in sorted(country_groups.keys()):
            lines = country_groups[country]
            if not lines:
                continue

            f.write(f"{country}\n")
            for line in lines:
                f.write(line + "\n")
            f.write("\n")
            wrote_anything = True

        if not wrote_anything:
            f.write("没有找到出现 2 次及以上的 IP（或没有匹配到 hk/jp/kr/sg/us/ca 标记）\n")

    total_valid_ips = sum(len(lines) for lines in country_groups.values())
    print(f"统计完成，结果已保存至：{OUTPUT_FILE}")
    print(f"共找到 {total_valid_ips} 个出现 2 次及以上的 IP:port")


if __name__ == "__main__":
    main()
