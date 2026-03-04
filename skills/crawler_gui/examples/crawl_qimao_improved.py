"""
七猫小说网站抓取示例（改进版）
增加滚动加载和更长的等待时间
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler import WebCrawler


def crawl_qimao_novel_improved(url: str):
    """
    抓取七猫小说内容（改进版）
    
    Args:
        url: 小说章节 URL
    """
    print(f"开始抓取: {url}")
    print("=" * 60)
    
    with WebCrawler(headless=False) as crawler:
        # 打开 URL，增加等待时间
        if crawler.open_url(url, timeout=30, wait_time=5):
            print("页面加载成功")
            
            # 滚动页面以加载更多内容
            print("滚动页面加载更多内容...")
            for i in range(3):
                crawler.page.evaluate("window.scrollBy(0, 1000)")
                time.sleep(2)
                print(f"  滚动 {i+1}/3")
            
            # 等待小说内容加载
            print("等待小说内容加载...")
            time.sleep(3)
            
            # 尝试提取所有段落
            print("提取小说内容...")
            paragraphs = crawler.extract_elements("p")
            
            if paragraphs:
                # 过滤掉空段落和太短的段落
                valid_paragraphs = [
                    p['text'] for p in paragraphs 
                    if p['text'] and len(p['text'].strip()) > 20
                ]
                
                if valid_paragraphs:
                    content = "\n\n".join(valid_paragraphs)
                    
                    print("\n" + "=" * 60)
                    print(f"成功提取到 {len(valid_paragraphs)} 个段落")
                    print("=" * 60)
                    print("小说内容预览:")
                    print("=" * 60)
                    print(content[:500] + "..." if len(content) > 500 else content)
                    print("=" * 60)
                    print(f"总字符数: {len(content)}")
                    
                    # 保存到文件
                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"novel_improved_{timestamp}.txt"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"URL: {url}\n")
                        f.write(f"抓取时间: {datetime.datetime.now()}\n")
                        f.write(f"段落数: {len(valid_paragraphs)}\n")
                        f.write("=" * 60 + "\n\n")
                        f.write(content)
                    
                    print(f"\n内容已保存到: {filepath}")
                else:
                    print("未找到有效的段落内容")
            else:
                print("未找到任何段落")
                
                # 获取整个页面的文本内容
                print("\n尝试获取整个页面的文本内容...")
                full_text = crawler.get_text_content()
                
                if full_text:
                    print(f"页面文本长度: {len(full_text)} 字符")
                    print("文本预览:")
                    print(full_text[:500])
                    
                    # 保存完整文本
                    with open("full_page_text.txt", "w", encoding="utf-8") as f:
                        f.write(full_text)
                    print("\n完整文本已保存到: full_page_text.txt")
        else:
            print("无法打开 URL")


def main():
    """
    主函数
    """
    # 七猫小说示例 URL
    url = "https://www.qimao.com/shuku/1834789-17167752040008/"
    
    crawl_qimao_novel_improved(url)


if __name__ == "__main__":
    main()
