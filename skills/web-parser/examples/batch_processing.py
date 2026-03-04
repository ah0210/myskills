"""
批量处理示例
演示如何批量处理多个网页
"""

import sys
import os
import concurrent.futures
import asyncio
from typing import List, Dict, Any

# 添加父目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_parser import WebParser, JinaReader, Crawl4AIParser


def example_1_sequential_processing():
    """
    示例 1：顺序处理多个网页
    """
    print("=" * 50)
    print("示例 1：顺序处理多个网页")
    print("=" * 50)
    
    parser = WebParser()
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    print(f"开始处理 {len(urls)} 个网页...")
    
    results = []
    for i, url in enumerate(urls, 1):
        try:
            content = parser.parse(url)
            results.append({"url": url, "success": True, "content": content})
            print(f"  [{i}/{len(urls)}] ✓ {url}: {len(content)} 字符")
        except Exception as e:
            results.append({"url": url, "success": False, "error": str(e)})
            print(f"  [{i}/{len(urls)}] ✗ {url}: {str(e)[:50]}...")
    
    print(f"完成！成功: {sum(1 for r in results if r['success'])}/{len(results)}")
    print()


def example_2_thread_pool_processing():
    """
    示例 2：使用线程池并发处理
    """
    print("=" * 50)
    print("示例 2：使用线程池并发处理")
    print("=" * 50)
    
    parser = WebParser()
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net",
        "https://example.edu"
    ]
    
    print(f"开始并发处理 {len(urls)} 个网页...")
    
    def process_url(url):
        try:
            content = parser.parse(url)
            return {"url": url, "success": True, "content": content}
        except Exception as e:
            return {"url": url, "success": False, "error": str(e)}
    
    # 使用线程池并发处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_url, urls))
    
    for i, result in enumerate(results, 1):
        if result["success"]:
            print(f"  [{i}/{len(results)}] ✓ {result['url']}: {len(result['content'])} 字符")
        else:
            print(f"  [{i}/{len(results)}] ✗ {result['url']}: {result['error'][:50]}...")
    
    print(f"完成！成功: {sum(1 for r in results if r['success'])}/{len(results)}")
    print()


async def example_3_async_processing():
    """
    示例 3：使用异步处理
    """
    print("=" * 50)
    print("示例 3：使用异步处理")
    print("=" * 50)
    
    parser = Crawl4AIParser()
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    print(f"开始异步处理 {len(urls)} 个网页...")
    
    async def process_url(url):
        try:
            content = await parser.extract(url)
            return {"url": url, "success": True, "content": content}
        except Exception as e:
            return {"url": url, "success": False, "error": str(e)}
    
    # 并发处理多个 URL
    results = await asyncio.gather(*[process_url(url) for url in urls])
    
    for i, result in enumerate(results, 1):
        if result["success"]:
            print(f"  [{i}/{len(results)}] ✓ {result['url']}: {len(result['content'])} 字符")
        else:
            print(f"  [{i}/{len(results)}] ✗ {result['url']}: {result['error'][:50]}...")
    
    print(f"完成！成功: {sum(1 for r in results if r['success'])}/{len(results)}")
    print()


def example_4_batch_with_engine_selection():
    """
    示例 4：批量处理并指定引擎
    """
    print("=" * 50)
    print("示例 4：批量处理并指定引擎")
    print("=" * 50)
    
    parser = WebParser()
    urls = [
        ("https://example.com", "jina"),
        ("https://example.org", "crawl4ai"),
        ("https://example.net", "auto")
    ]
    
    print(f"开始处理 {len(urls)} 个网页...")
    
    for i, (url, engine) in enumerate(urls, 1):
        try:
            content = parser.parse(url, engine=engine)
            print(f"  [{i}/{len(urls)}] ✓ {url} ({engine}): {len(content)} 字符")
        except Exception as e:
            print(f"  [{i}/{len(urls)}] ✗ {url} ({engine}): {str(e)[:50]}...")
    
    print()


def example_5_save_to_file():
    """
    示例 5：批量处理并保存到文件
    """
    print("=" * 50)
    print("示例 5：批量处理并保存到文件")
    print("=" * 50)
    
    parser = WebParser()
    urls = [
        "https://example.com",
        "https://example.org"
    ]
    
    print(f"开始处理 {len(urls)} 个网页...")
    
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, url in enumerate(urls, 1):
        try:
            content = parser.parse(url)
            
            # 生成文件名
            filename = f"page_{i}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # 保存到文件
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"URL: {url}\n")
                f.write(f"{'=' * 50}\n\n")
                f.write(content)
            
            print(f"  [{i}/{len(urls)}] ✓ {url}: 已保存到 {filename}")
        except Exception as e:
            print(f"  [{i}/{len(urls)}] ✗ {url}: {str(e)[:50]}...")
    
    print(f"完成！文件保存在 {output_dir} 目录")
    print()


def example_6_process_from_file():
    """
    示例 6：从文件读取 URL 列表并处理
    """
    print("=" * 50)
    print("示例 6：从文件读取 URL 列表并处理")
    print("=" * 50)
    
    # 创建示例 URL 文件
    urls_file = "urls.txt"
    sample_urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    with open(urls_file, "w", encoding="utf-8") as f:
        for url in sample_urls:
            f.write(url + "\n")
    
    print(f"已创建示例 URL 文件: {urls_file}")
    
    # 从文件读取 URL
    with open(urls_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"从文件读取了 {len(urls)} 个 URL")
    
    # 处理 URL
    parser = WebParser()
    results = []
    
    for i, url in enumerate(urls, 1):
        try:
            content = parser.parse(url)
            results.append({"url": url, "success": True, "content": content})
            print(f"  [{i}/{len(urls)}] ✓ {url}: {len(content)} 字符")
        except Exception as e:
            results.append({"url": url, "success": False, "error": str(e)})
            print(f"  [{i}/{len(urls)}] ✗ {url}: {str(e)[:50]}...")
    
    print(f"完成！成功: {sum(1 for r in results if r['success'])}/{len(results)}")
    print()


def example_7_progress_tracking():
    """
    示例 7：带进度跟踪的批量处理
    """
    print("=" * 50)
    print("示例 7：带进度跟踪的批量处理")
    print("=" * 50)
    
    parser = WebParser()
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net",
        "https://example.edu",
        "https://example.gov"
    ]
    
    total = len(urls)
    success_count = 0
    fail_count = 0
    
    print(f"开始处理 {total} 个网页...")
    print()
    
    for i, url in enumerate(urls, 1):
        try:
            content = parser.parse(url)
            success_count += 1
            
            # 显示进度条
            progress = int((i / total) * 50)
            bar = "█" * progress + "░" * (50 - progress)
            print(f"\r[{bar}] {i}/{total} ({i/total*100:.1f}%) - 成功: {success_count}, 失败: {fail_count}", end="")
        except Exception as e:
            fail_count += 1
            
            # 显示进度条
            progress = int((i / total) * 50)
            bar = "█" * progress + "░" * (50 - progress)
            print(f"\r[{bar}] {i}/{total} ({i/total*100:.1f}%) - 成功: {success_count}, 失败: {fail_count}", end="")
    
    print()
    print(f"\n完成！成功: {success_count}/{total}, 失败: {fail_count}/{total}")
    print()


def example_8_rate_limited_processing():
    """
    示例 8：限速批量处理
    """
    print("=" * 50)
    print("示例 8：限速批量处理")
    print("=" * 50)
    
    import time
    
    parser = WebParser()
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    rate_limit = 1  # 每秒最多 1 个请求
    
    print(f"开始处理 {len(urls)} 个网页（限速: {rate_limit} 请求/秒）...")
    
    for i, url in enumerate(urls, 1):
        try:
            content = parser.parse(url)
            print(f"  [{i}/{len(urls)}] ✓ {url}: {len(content)} 字符")
        except Exception as e:
            print(f"  [{i}/{len(urls)}] ✗ {url}: {str(e)[:50]}...")
        
        # 限速：等待一段时间
        if i < len(urls):
            time.sleep(1 / rate_limit)
    
    print("完成！")
    print()


async def main():
    """
    运行所有示例
    """
    print("\n" + "=" * 50)
    print("WebParser 批量处理示例")
    print("=" * 50 + "\n")
    
    example_1_sequential_processing()
    example_2_thread_pool_processing()
    await example_3_async_processing()
    example_4_batch_with_engine_selection()
    example_5_save_to_file()
    example_6_process_from_file()
    example_7_progress_tracking()
    example_8_rate_limited_processing()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
