"""
基础使用示例
演示 WebParser 的基本功能
"""

import sys
import os

# 添加父目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_parser import WebParser, JinaReader, Crawl4AIParser


def example_1_basic_parsing():
    """
    示例 1：基础网页解析
    """
    print("=" * 50)
    print("示例 1：基础网页解析")
    print("=" * 50)
    
    # 创建解析器实例（自动选择引擎）
    parser = WebParser()
    
    # 解析网页
    url = "https://example.com"
    try:
        content = parser.parse(url)
        print(f"成功解析网页: {url}")
        print(f"内容长度: {len(content)} 字符")
        print(f"内容预览: {content[:200]}...")
    except Exception as e:
        print(f"解析失败: {e}")
    
    print()


def example_2_specify_engine():
    """
    示例 2：指定引擎解析
    """
    print("=" * 50)
    print("示例 2：指定引擎解析")
    print("=" * 50)
    
    parser = WebParser()
    url = "https://example.com"
    
    # 使用 Jina Reader
    try:
        content = parser.parse(url, engine="jina")
        print(f"Jina Reader 解析成功")
        print(f"内容长度: {len(content)} 字符")
    except Exception as e:
        print(f"Jina Reader 解析失败: {e}")
    
    print()
    
    # 使用 Crawl4AI
    try:
        content = parser.parse(url, engine="crawl4ai")
        print(f"Crawl4AI 解析成功")
        print(f"内容长度: {len(content)} 字符")
    except Exception as e:
        print(f"Crawl4AI 解析失败: {e}")
    
    print()


def example_3_get_metadata():
    """
    示例 3：获取元数据
    """
    print("=" * 50)
    print("示例 3：获取元数据")
    print("=" * 50)
    
    parser = WebParser()
    url = "https://example.com"
    
    try:
        metadata = parser.parse_with_metadata(url)
        print(f"URL: {metadata['url']}")
        print(f"引擎: {metadata['engine']}")
        print(f"内容长度: {len(metadata['content'])} 字符")
        
        if 'links' in metadata:
            print(f"链接数: {len(metadata['links'])}")
        
        if 'images' in metadata:
            print(f"图片数: {len(metadata['images'])}")
    except Exception as e:
        print(f"解析失败: {e}")
    
    print()


def example_4_jina_reader_only():
    """
    示例 4：单独使用 Jina Reader
    """
    print("=" * 50)
    print("示例 4：单独使用 Jina Reader")
    print("=" * 50)
    
    # 创建 Jina Reader 实例
    reader = JinaReader(timeout=30, retry_times=3)
    
    # 检查服务是否可用
    if reader.is_available():
        print("Jina Reader 服务可用")
    else:
        print("Jina Reader 服务不可用")
    
    # 提取网页内容
    url = "https://example.com"
    try:
        content = reader.extract(url)
        print(f"成功提取网页: {url}")
        print(f"内容长度: {len(content)} 字符")
    except Exception as e:
        print(f"提取失败: {e}")
    
    print()


def example_5_crawl4ai_only():
    """
    示例 5：单独使用 Crawl4AI
    """
    print("=" * 50)
    print("示例 5：单独使用 Crawl4AI")
    print("=" * 50)
    
    # 创建 Crawl4AI 解析器实例
    parser = Crawl4AIParser(headless=True, timeout=30)
    
    # 同步方式提取内容
    url = "https://example.com"
    try:
        content = parser.extract_sync(url)
        print(f"成功提取网页: {url}")
        print(f"内容长度: {len(content)} 字符")
    except Exception as e:
        print(f"提取失败: {e}")
    
    print()


def example_6_prefer_engine():
    """
    示例 6：设置首选引擎
    """
    print("=" * 50)
    print("示例 6：设置首选引擎")
    print("=" * 50)
    
    # 创建解析器，设置首选引擎为 Jina Reader
    parser_jina = WebParser(prefer_engine="jina")
    print("首选引擎: Jina Reader")
    
    # 创建解析器，设置首选引擎为 Crawl4AI
    parser_crawl4ai = WebParser(prefer_engine="crawl4ai")
    print("首选引擎: Crawl4AI")
    
    # 创建解析器，自动选择引擎
    parser_auto = WebParser(prefer_engine="auto")
    print("首选引擎: 自动选择")
    
    print()


def main():
    """
    运行所有示例
    """
    print("\n" + "=" * 50)
    print("WebParser 基础使用示例")
    print("=" * 50 + "\n")
    
    example_1_basic_parsing()
    example_2_specify_engine()
    example_3_get_metadata()
    example_4_jina_reader_only()
    example_5_crawl4ai_only()
    example_6_prefer_engine()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
