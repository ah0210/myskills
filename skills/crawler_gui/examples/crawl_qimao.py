"""
七猫小说网站抓取示例
演示如何抓取动态加载的小说内容
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler import WebCrawler


def crawl_qimao_novel(url: str):
    """
    抓取七猫小说内容
    
    Args:
        url: 小说章节 URL
    """
    print(f"开始抓取: {url}")
    print("=" * 60)
    
    with WebCrawler(headless=False) as crawler:  # 使用有头模式查看浏览器行为
        # 打开 URL，增加等待时间
        if crawler.open_url(url, timeout=30, wait_time=5):
            print("页面加载成功")
            
            # 等待小说内容加载
            print("等待小说内容加载...")
            
            # 尝试多个可能的内容选择器
            content_selectors = [
                ".chapter-content",  # 常见的章节内容类名
                ".content-text",     # 内容文本类名
                ".read-content",     # 阅读内容类名
                "article",           # article 标签
                ".text-content",     # 文本内容类名
                "p",                 # 段落标签
            ]
            
            content = ""
            for selector in content_selectors:
                print(f"尝试选择器: {selector}")
                if crawler.wait_for_content(selector, timeout=5):
                    content = crawler.extract_text_from_selector(selector)
                    if content and len(content) > 100:
                        print(f"成功找到内容，使用选择器: {selector}")
                        break
            
            if content:
                print("\n" + "=" * 60)
                print("小说内容:")
                print("=" * 60)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("=" * 60)
                print(f"总字符数: {len(content)}")
                
                # 保存到文件
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"novel_{timestamp}.txt"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"URL: {url}\n")
                    f.write(f"抓取时间: {datetime.datetime.now()}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(content)
                
                print(f"\n内容已保存到: {filepath}")
            else:
                print("未能提取到小说内容")
                print("提示: 可能需要查看页面源代码找到正确的选择器")
                
                # 获取整个页面的 HTML
                html = crawler.get_page_content()
                print(f"\n页面 HTML 长度: {len(html)} 字符")
                
                # 保存 HTML 用于分析
                with open("page_source.html", "w", encoding="utf-8") as f:
                    f.write(html)
                print("页面 HTML 已保存到: page_source.html")
        else:
            print("无法打开 URL")


def main():
    """
    主函数
    """
    # 七猫小说示例 URL
    url = "https://www.qimao.com/shuku/1834789-17167752040008/"
    
    crawl_qimao_novel(url)


if __name__ == "__main__":
    main()
