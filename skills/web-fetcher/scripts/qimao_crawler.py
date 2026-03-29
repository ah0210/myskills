#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawl Qimao novel site for hot novels analysis."""

import urllib.request
import json
import re
import sys
from datetime import datetime

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

def fetch_url(url: str, timeout: int = 20) -> str:
    headers = {
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', errors='replace')

def extract_initial_state(html: str):
    """Extract __INITIAL_STATE__ JSON from HTML."""
    pattern = r'window\.__INITIAL_STATE__\s*=\s*(\{.+?\});?\s*</script>'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        try:
            json_str = match.group(1)
            # Fix trailing commas
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            return json.loads(json_str)
        except Exception as e:
            print(f"  [JSON Error] {e}")
    return None

def find_all_novels_in_json(data, novels=None):
    """Recursively find all novel entries in JSON data."""
    if novels is None:
        novels = []
    
    if isinstance(data, dict):
        # Check if this is a novel entry
        if 'bookId' in data or 'bookName' in data or 'title' in data:
            novel = {
                'id': data.get('bookId') or data.get('id') or data.get('novelId'),
                'title': data.get('bookName') or data.get('title') or data.get('name'),
                'author': data.get('author') or data.get('authorName'),
                'category': data.get('category') or data.get('categoryId'),
                'words': data.get('wordCount') or data.get('words'),
                'status': data.get('status') or data.get('serializeStatus'),
                'intro': data.get('intro') or data.get('description'),
            }
            if novel['title']:
                novels.append(novel)
        
        # Recurse into values
        for v in data.values():
            find_all_novels_in_json(v, novels)
    
    elif isinstance(data, list):
        for item in data:
            find_all_novels_in_json(item, novels)
    
    return novels

def parse_html_for_novels(html: str) -> list:
    """Parse novels from HTML using multiple patterns."""
    novels = []
    
    # Pattern 1: JSON-like structures in script tags
    json_patterns = [
        r'"bookId"\s*:\s*"?(\d+)"?\s*,\s*"bookName"\s*:\s*"([^"]+)"',
        r'"id"\s*:\s*(\d+)\s*,\s*"title"\s*:\s*"([^"]+)"',
        r'"novelId"\s*:\s*(\d+)\s*,\s*"novelName"\s*:\s*"([^"]+)"',
        r'"book_id"\s*:\s*"?(\d+)"?\s*,\s*"book_name"\s*:\s*"([^"]+)"',
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, html)
        for m in matches:
            novels.append({'id': m[0], 'title': m[1], 'source': 'json_pattern'})
    
    # Pattern 2: HTML links
    html_pattern = r'<a[^>]*href="/shuku/(\d+)"[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</a>'
    matches = re.findall(html_pattern, html)
    for m in matches:
        novels.append({'id': m[0], 'title': m[1].strip(), 'source': 'html_link'})
    
    # Pattern 3: data attributes
    data_pattern = r'data-book-id="(\d+)"[^>]*data-book-name="([^"]+)"'
    matches = re.findall(data_pattern, html)
    for m in matches:
        novels.append({'id': m[0], 'title': m[1], 'source': 'data_attr'})
    
    return novels

def main():
    print("=" * 60)
    print("七猫小说网男频热门小说抓取分析")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    url = "https://www.qimao.com"
    print(f"\n[1] 抓取首页: {url}")
    
    try:
        html = fetch_url(url)
        print(f"    成功获取 {len(html)} 字符")
        
        # Method 1: Try to parse __INITIAL_STATE__
        print("\n[2] 解析页面数据...")
        initial_state = extract_initial_state(html)
        
        all_novels = []
        
        if initial_state:
            print(f"    找到 __INITIAL_STATE__，包含 {len(initial_state)} 个顶级键")
            print(f"    键名: {list(initial_state.keys())[:15]}")
            
            # Find all novels in the JSON
            novels_from_json = find_all_novels_in_json(initial_state)
            print(f"    从 JSON 中找到 {len(novels_from_json)} 本小说")
            all_novels.extend(novels_from_json)
        
        # Method 2: Parse HTML directly
        novels_from_html = parse_html_for_novels(html)
        print(f"    从 HTML 中找到 {len(novels_from_html)} 本小说")
        all_novels.extend(novels_from_html)
        
        # Deduplicate
        seen = set()
        unique_novels = []
        for n in all_novels:
            key = (n.get('id'), n.get('title'))
            if key not in seen and n.get('title'):
                seen.add(key)
                unique_novels.append(n)
        
        print(f"\n[3] 分析结果")
        print(f"    去重后共 {len(unique_novels)} 本小说")
        
        if unique_novels:
            print("\n" + "=" * 60)
            print("热门小说列表 (前 50 本)")
            print("=" * 60)
            for i, n in enumerate(unique_novels[:50], 1):
                title = n.get('title', 'Unknown')
                author = n.get('author', '')
                extra = f" - {author}" if author else ""
                print(f"  {i:2d}. {title}{extra}")
        else:
            print("\n[警告] 未找到小说数据，尝试显示页面结构片段...")
            # Find male/female section
            for keyword in ['男频', '女频', 'ranking', 'rank', '热门']:
                if keyword in html:
                    idx = html.find(keyword)
                    print(f"\n  发现关键词 '{keyword}' 位置: {idx}")
                    # Extract surrounding context
                    start = max(0, idx - 50)
                    end = min(len(html), idx + 150)
                    snippet = html[start:end]
                    # Clean up
                    snippet = re.sub(r'\s+', ' ', snippet)
                    print(f"  上下文: {snippet[:200]}")
                    break
        
    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
