#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch Qimao ranking page via Jina Reader."""

import urllib.request
import sys
import re
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
    print("七猫小说网 - 排行榜分析")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 排行榜页面
    url = "https://www.qimao.com/paihang"
    print(f"\n[访问] {url}")
    
    try:
        content = fetch_via_jina(url)
        print(f"[成功] 获取 {len(content)} 字符")
        print("\n" + "=" * 70)
        print("页面内容:")
        print("=" * 70)
        print(content)
        
        # 提取小说标题
        print("\n" + "=" * 70)
        print("提取小说信息:")
        print("=" * 70)
        
        # 匹配模式
        patterns = [
            (r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', '表格'),
            (r'\*\*([^*]{2,30})\*\*', '加粗'),
            (r'《([^》]+)》', '书名号'),
            (r'\d+\.\s*(.+?)(?:\n|$)', '列表'),
        ]
        
        novels = []
        for pattern, name in patterns:
            matches = re.findall(pattern, content)
            if matches:
                print(f"\n[{name}模式] 找到 {len(matches)} 个:")
                for m in matches[:20]:
                    print(f"  {m}")
                novels.extend(matches)
        
    except Exception as e:
        print(f"[失败] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
