import re
import os
from datetime import datetime

#获取当前目录位置
PATH = os.path.dirname(os.path.abspath(__file__))
# 自动生成当天日期
date_str = datetime.now().strftime("%Y%m%d")

input_file  = f'{PATH}/node.txt'
output_file = f'{PATH}/aliveip/aliveip_{date_str}.txt'

if "__name__==__main__":#主程序开始
    #收集暂存
    result = []
    
    #开始收集
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 提取 @ 后面的 IP:端口 和 # 后面的备注
            match = re.search(r"@([^:]+:\d+).*#(.+)$", line)

            if match:
                ip_port = match.group(1)
                name = match.group(2)

                result.append(f"{ip_port}#{name}")

    # 写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    #记录收集个数和存放位置
    print(f"完成，共写入 {len(result)} 条")
    //print(f"文件：{output_file}")
