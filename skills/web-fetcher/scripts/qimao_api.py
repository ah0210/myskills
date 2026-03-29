#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawl Qimao novel API for hot novels."""

import urllib.request
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def fetch_json(url: str, timeout: int = 15) -> dict:
    headers = {
        'User-Agent': UA,
        'Accept': 'application/json',
        'Referer': 'https://www.qimao.com/',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

def main():
    print("=" * 70)
    print("七猫小说网 - 男频热门小说分析报告")
    print(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 七猫小说排行榜 API
    # 尝试多个可能的 API 端点
    apis = [
        # 男频热榜
        ("男频热度榜", "https://api-bc.wtzw.com/api/v1/rank/male/hot?count=50"),
        ("男频畅销榜", "https://api-bc.wtzw.com/api/v1/rank/male/sell?count=50"),
        ("男频完结榜", "https://api-bc.wtzw.com/api/v1/rank/male/end?count=50"),
        ("男频新书榜", "https://api-bc.wtzw.com/api/v1/rank/male/new?count=50"),
        # 通用排行榜
        ("全站热榜", "https://api-bc.wtzw.com/api/v1/rank/hot?count=50"),
        # 分类排行榜
        ("都市热榜", "https://api-bc.wtzw.com/api/v1/rank/category/1/hot?count=30"),
        ("玄幻热榜", "https://api-bc.wtzw.com/api/v1/rank/category/2/hot?count=30"),
        ("仙侠热榜", "https://api-bt.wtzw.com/api/v3/rank/channel/male/hot"),
    ]
    
    all_novels = []
    successful_apis = []
    
    for name, url in apis:
        print(f"\n[{name}] 尝试: {url[:50]}...")
        try:
            data = fetch_json(url)
            
            if data.get('data'):
                novels = data['data']
                if isinstance(novels, list):
                    print(f"    ✓ 成功获取 {len(novels)} 本小说")
                    successful_apis.append((name, url))
                    for n in novels:
                        n['_source'] = name
                    all_novels.extend(novels)
                elif isinstance(novels, dict) and 'list' in novels:
                    novel_list = novels['list']
                    print(f"    ✓ 成功获取 {len(novel_list)} 本小说")
                    successful_apis.append((name, url))
                    for n in novel_list:
                        n['_source'] = name
                    all_novels.extend(novel_list)
                else:
                    print(f"    数据结构: {type(novels)}")
            else:
                print(f"    响应: {str(data)[:100]}")
                
        except Exception as e:
            print(f"    ✗ 失败: {str(e)[:60]}")
    
    # 分析结果
    if all_novels:
        print("\n" + "=" * 70)
        print("分析结果")
        print("=" * 70)
        
        # 去重
        seen = set()
        unique_novels = []
        for n in all_novels:
            novel_id = n.get('id') or n.get('book_id') or n.get('novelId')
            if novel_id and novel_id not in seen:
                seen.add(novel_id)
                unique_novels.append(n)
        
        print(f"\n📊 统计数据:")
        print(f"   - 成功 API 数: {len(successful_apis)}")
        print(f"   - 总获取数: {len(all_novels)}")
        print(f"   - 去重后数: {len(unique_novels)}")
        
        # 分析题材分布
        categories = {}
        for n in unique_novels:
            cat = n.get('category_name') or n.get('category') or n.get('typeName') or '未知'
            categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            print(f"\n📚 题材分布:")
            sorted_cats = sorted(categories.items(), key=lambda x: -x[1])
            for cat, count in sorted_cats[:10]:
                bar = '█' * (count // 2)
                print(f"   {cat}: {count} {bar}")
        
        # 热门小说列表
        print(f"\n📖 男频热门小说 Top 50:")
        print("-" * 70)
        
        # 按热度排序（如果有热度值）
        def get_hot(n):
            return int(n.get('hot') or n.get('heat') or n.get('popularity') or 0)
        
        sorted_novels = sorted(unique_novels, key=get_hot, reverse=True)
        
        for i, n in enumerate(sorted_novels[:50], 1):
            title = n.get('title') or n.get('name') or n.get('book_name') or '未知'
            author = n.get('author') or n.get('author_name') or ''
            words = n.get('words') or n.get('word_count') or 0
            cat = n.get('category_name') or n.get('category') or ''
            source = n.get('_source', '')
            
            # 格式化字数
            if isinstance(words, int) or (isinstance(words, str) and words.isdigit()):
                words = int(words)
                if words >= 10000:
                    words_str = f"{words//10000}万字"
                else:
                    words_str = f"{words}字"
            else:
                words_str = str(words)
            
            info = f"{title}"
            if author:
                info += f" | {author}"
            if cat:
                info += f" | {cat}"
            if words_str and words_str != '0':
                info += f" | {words_str}"
            
            print(f"   {i:2d}. {info}")
        
        # 保存数据
        print(f"\n💾 数据已保存到内存")
        
    else:
        print("\n❌ 未能获取任何数据")
        print("尝试备用方案...")
        
        # 备用：解析网页
        try:
            import urllib.request
            url = "https://www.qimao.com/shuku/boy-hot"
            headers = {'User-Agent': UA}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8', errors='replace')
            print(f"  获取网页 {len(html)} 字符")
            
            # 查找小说数据
            import re
            # 尝试多种模式
            patterns = [
                r'"book_id"\s*:\s*"(\d+)"[^}]*"book_name"\s*:\s*"([^"]+)"',
                r'"id"\s*:\s*(\d+)[^}]*"title"\s*:\s*"([^"]+)"',
            ]
            
            found = []
            for pattern in patterns:
                matches = re.findall(pattern, html)
                found.extend(matches)
            
            if found:
                print(f"\n从网页解析到 {len(found)} 本小说:")
                for i, (bid, title) in enumerate(found[:30], 1):
                    print(f"   {i}. {title} (ID: {bid})")
            
        except Exception as e:
            print(f"  网页解析失败: {e}")

if __name__ == "__main__":
    main()
