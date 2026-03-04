"""
高级用法示例
演示 WebParser 的高级功能
"""

import sys
import os
import asyncio

# 添加父目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_parser import WebParser, JinaReader, Crawl4AIParser


async def example_1_extract_links():
    """
    示例 1：提取网页中的所有链接
    """
    print("=" * 50)
    print("示例 1：提取网页中的所有链接")
    print("=" * 50)
    
    parser = Crawl4AIParser()
    url = "https://example.com"
    
    try:
        links = await parser.extract_links(url)
        print(f"成功提取 {len(links)} 个链接")
        
        # 显示前 5 个链接
        for i, link in enumerate(links[:5]):
            print(f"{i+1}. {link.get('text', 'N/A')}: {link.get('href', 'N/A')}")
        
        if len(links) > 5:
            print(f"... 还有 {len(links) - 5} 个链接")
    except Exception as e:
        print(f"提取失败: {e}")
    
    print()


async def example_2_extract_images():
    """
    示例 2：提取网页中的所有图片
    """
    print("=" * 50)
    print("示例 2：提取网页中的所有图片")
    print("=" * 50)
    
    parser = Crawl4AIParser()
    url = "https://example.com"
    
    try:
        images = await parser.extract_images(url)
        print(f"成功提取 {len(images)} 张图片")
        
        # 显示前 5 张图片
        for i, img in enumerate(images[:5]):
            print(f"{i+1}. {img.get('alt', 'N/A')}: {img.get('src', 'N/A')}")
        
        if len(images) > 5:
            print(f"... 还有 {len(images) - 5} 张图片")
    except Exception as e:
        print(f"提取失败: {e}")
    
    print()


async def example_3_custom_css_selector():
    """
    示例 3：使用自定义 CSS 选择器提取内容
    """
    print("=" * 50)
    print("示例 3：使用自定义 CSS 选择器提取内容")
    print("=" * 50)
    
    parser = Crawl4AIParser()
    url = "https://example.com"
    
    # 使用自定义 CSS 选择器
    try:
        result = await parser.extract_custom(
            url,
            css_selector="body"  # 提取 body 内容
        )
        print(f"成功提取内容")
        print(f"内容长度: {len(result['content'])} 字符")
        print(f"内容预览: {result['content'][:200]}...")
    except Exception as e:
        print(f"提取失败: {e}")
    
    print()


async def example_4_structured_data():
    """
    示例 4：提取结构化数据
    """
    print("=" * 50)
    print("示例 4：提取结构化数据")
    print("=" * 50)
    
    parser = Crawl4AIParser()
    url = "https://example.com"
    
    try:
        metadata = await parser.extract_with_metadata(url)
        
        # 提取结构化数据
        structured_data = {
            "url": metadata["url"],
            "engine": metadata["engine"],
            "content_length": len(metadata["content"]),
            "links_count": len(metadata.get("links", [])),
            "images_count": len(metadata.get("images", [])),
            "media_count": len(metadata.get("media", []))
        }
        
        print("结构化数据:")
        for key, value in structured_data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"提取失败: {e}")
    
    print()


def example_5_error_handling():
    """
    示例 5：错误处理和重试机制
    """
    print("=" * 50)
    print("示例 5：错误处理和重试机制")
    print("=" * 50)
    
    # 创建 Jina Reader，设置重试次数
    reader = JinaReader(timeout=10, retry_times=5)
    
    # 测试无效 URL
    invalid_url = "https://this-url-does-not-exist-12345.com"
    
    try:
        content = reader.extract(invalid_url)
        print(f"成功提取: {len(content)} 字符")
    except Exception as e:
        print(f"提取失败（预期行为）: {type(e).__name__}")
        print(f"错误信息: {str(e)[:100]}...")
    
    print()


def example_6_engine_fallback():
    """
    示例 6：引擎降级机制
    """
    print("=" * 50)
    print("示例 6：引擎降级机制")
    print("=" * 50)
    
    # 创建解析器，设置首选引擎为 Jina Reader
    parser = WebParser(prefer_engine="jina")
    
    # 检查 Jina Reader 是否可用
    if parser.is_jina_available():
        print("Jina Reader 可用，将优先使用")
    else:
        print("Jina Reader 不可用，将自动降级到 Crawl4AI")
    
    # 解析网页（会自动选择最佳引擎）
    url = "https://example.com"
    try:
        content = parser.parse(url)
        print(f"成功解析网页: {url}")
        print(f"内容长度: {len(content)} 字符")
    except Exception as e:
        print(f"解析失败: {e}")
    
    print()


async def example_7_async_processing():
    """
    示例 7：异步处理多个网页
    """
    print("=" * 50)
    print("示例 7：异步处理多个网页")
    print("=" * 50)
    
    parser = Crawl4AIParser()
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    async def process_url(url):
        try:
            content = await parser.extract(url)
            return {"url": url, "success": True, "length": len(content)}
        except Exception as e:
            return {"url": url, "success": False, "error": str(e)}
    
    # 并发处理多个 URL
    results = await asyncio.gather(*[process_url(url) for url in urls])
    
    print(f"处理了 {len(results)} 个网页")
    for result in results:
        if result["success"]:
            print(f"  ✓ {result['url']}: {result['length']} 字符")
        else:
            print(f"  ✗ {result['url']}: {result['error']}")
    
    print()


def example_8_custom_timeout():
    """
    示例 8：自定义超时设置
    """
    print("=" * 50)
    print("示例 8：自定义超时设置")
    print("=" * 50)
    
    # 创建解析器，设置不同的超时时间
    reader_fast = JinaReader(timeout=5)
    reader_slow = JinaReader(timeout=60)
    
    print("快速解析器（5秒超时）")
    print("慢速解析器（60秒超时）")
    
    print()


async def main():
    """
    运行所有示例
    """
    print("\n" + "=" * 50)
    print("WebParser 高级用法示例")
    print("=" * 50 + "\n")
    
    await example_1_extract_links()
    await example_2_extract_images()
    await example_3_custom_css_selector()
    await example_4_structured_data()
    example_5_error_handling()
    example_6_engine_fallback()
    await example_7_async_processing()
    example_8_custom_timeout()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
