#!/usr/bin/env python3
import asyncio, aiohttp, csv

INPUT = './ip/port443.txt'  # 输入文件路径，假设 IP 地址都在 ip.txt 中
OUTPUT = './ip/results_async.csv'  # 输出文件路径
OUTPUT_GOOD = './ip/goodproxyip.txt'  # 输出文件路径
CONCURRENCY = 200  # 控制并发请求数
TIMEOUT = 10  # 设置超时时间
URL = 'https://check.proxyip.cmliussss.net/check?proxyip={}'  # 请求的 URL

async def fetch(session, ipraw, sem):
    if ':' not in ipraw:
        ipraw = ipraw + ':443'  # 如果没有端口，默认加上 :443
    async with sem:
        try:
            async with session.get(URL.format(ipraw), timeout=TIMEOUT) as r:
                text = await r.text()
                try:
                    data = await r.json()  # 尝试解析为 JSON
                except:
                    data = {"raw": text}  # 如果解析失败，保存原始响应
                return ipraw, data
        except Exception as e:
            return ipraw, {"error": str(e)}
			
async def main():
    ips = [line.strip() for line in open(INPUT) if line.strip()]  # 读取 IP 文件，去除空行
    sem = asyncio.Semaphore(CONCURRENCY)  # 设置并发数限制
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)  # 设置总超时
    async with aiohttp.ClientSession(timeout=timeout) as sess:
        tasks = [fetch(sess, ip, sem) for ip in ips]  # 为每个 IP 创建请求任务
        results = await asyncio.gather(*tasks)  # 并发执行请求
    
    goodips = []
    for ipraw, data in results:
        if data.get('success', '') == 'True':
            goodips.append(ipraw)
    goodips_str = '\n'.join(goodips)
    with open(OUTPUT_GOOD, 'w', encoding='utf-8') as f:
        f.write(goodips_str)
    """
    # 保存结果到 CSV 文件
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['input', 'proxyIP', 'portRemote', 'success', 'colo', 'responseTime', 'message', 'timestamp', 'error', 'raw'])
        for ipraw, data in results:
            if isinstance(data, dict):
                writer.writerow([
                    ipraw,
                    data.get('proxyIP', ''),
                    data.get('portRemote', ''),
                    data.get('success', ''),
                    data.get('colo', ''),
                    data.get('responseTime', ''),
                    data.get('message', ''),
                    data.get('timestamp', ''),
                    data.get('error', ''),
                    str(data.get('raw', data))  # 保留原始数据
                ])
            else:
                writer.writerow([ipraw, '', '', '', '', '', '', '', 'unexpected', ''])
	
    print("done ->", OUTPUT)  # 输出文件生成提示
	"""
if __name__ == "__main__":
    asyncio.run(main())  # 启动异步任务
