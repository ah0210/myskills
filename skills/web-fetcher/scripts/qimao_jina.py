#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch Qimao novel ranking via Jina Reader."""

import urllib.request
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def fetch_via_jina(url: str) -> str:
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        'User-Agent': UA,
        'Accept': 'text/markdown',
    }
    req = urllib.request.Request(jina_url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8')

def main():
    print("=" * 70)
    print("七猫小说网 - 男频热门小说分析")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 尝试多个页面
    pages = [
        ("男频热榜", "https://www.qimao.com/shuku/boy-hot"),
        ("男频书库", "https://www.qimao.com/shuku/boy"),
        ("排行榜页", "https://www.qimao.com/rank"),
        ("书库首页", "https://www.qimao.com/shuku"),
    ]
    
    for name, url in pages:
        print(f"\n[{name}] {url}")
        try:
            content = fetch_via_jina(url)
            print(f"获取成功: {len(content)} 字符")
            print("-" * 50)
            # 显示前 2000 字符
            print(content[:2000])
            print("-" * 50)
            
            # 尝试提取小说标题
            import re
            # 常见的小说标题模式
            patterns = [
                r'\*\*([^*]{2,30})\*\*',  # Markdown 加粗
                r'《([^》]{2,30})》',     # 书名号
                r'^\d+\.\s*(.+)$',        # 序号列表
            ]
            
            titles = []
            for pattern in patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                titles.extend(matches)
            
            if titles:
                print(f"\n提取到 {len(titles)} 个可能的书名:")
                for t in titles[:20]:
                    print(f"  - {t}")
            
        except Exception as e:
            print(f"失败: {e}")

if __name__ == "__main__":
    main()
