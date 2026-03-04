"""
调试版本 - 七猫小说抓取
输出详细信息，帮助定位问题
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler import WebCrawler


def debug_crawl_qimao(url: str):
    """
    调试版本抓取
    
    Args:
        url: 小说章节 URL
    """
    print(f"开始调试抓取: {url}")
    print("=" * 60)
    
    with WebCrawler(headless=False) as crawler:
        # 步骤 1: 打开页面
        print("\n[步骤 1] 打开页面...")
        if not crawler.open_url(url, wait_time=5):
            print("❌ 无法打开 URL")
            return
        print("✅ 页面加载成功")
        
        # 步骤 2: 滚动页面
        print("\n[步骤 2] 滚动页面...")
        for i in range(3):
            crawler.page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(2)
            print(f"  滚动 {i+1}/3 完成")
        print("✅ 滚动完成")
        
        # 步骤 3: 等待内容加载
        print("\n[步骤 3] 等待内容加载...")
        time.sleep(3)
        print("✅ 等待完成")
        
        # 步骤 4: 尝试不同的选择器
        print("\n[步骤 4] 尝试不同的选择器...")
        
        selectors = [
            ("段落", "p"),
            ("文章", "article"),
            ("内容区域", ".content"),
            ("章节内容", ".chapter-content"),
            ("阅读内容", ".read-content"),
            ("文本内容", ".text-content"),
            ("所有文本", "body"),
        ]
        
        for name, selector in selectors:
            print(f"\n尝试选择器: {name} ({selector})")
            elements = crawler.extract_elements(selector)
            print(f"  找到 {len(elements)} 个元素")
            
            if elements:
                # 显示前3个元素
                for i, elem in enumerate(elements[:3]):
                    text = elem['text'].strip()
                    print(f"  元素 {i+1}: {text[:100]}..." if len(text) > 100 else f"  元素 {i+1}: {text}")
                
                # 如果是段落，统计有效段落
                if selector == "p":
                    valid = [e for e in elements if len(e['text'].strip()) > 20]
                    print(f"  有效段落（>20字符）: {len(valid)} 个")
                    
                    if valid:
                        print("\n✅ 找到有效内容！")
                        print("=" * 60)
                        print("小说内容预览:")
                        print("=" * 60)
                        for i, p in enumerate(valid[:5]):
                            print(f"\n段落 {i+1}:")
                            print(p['text'][:200])
                        
                        # 保存结果
                        output_dir = "output"
                        os.makedirs(output_dir, exist_ok=True)
                        
                        import datetime
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"debug_novel_{timestamp}.txt"
                        filepath = os.path.join(output_dir, filename)
                        
                        content = "\n\n".join([p['text'] for p in valid])
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(f"URL: {url}\n")
                            f.write(f"抓取时间: {datetime.datetime.now()}\n")
                            f.write(f"段落数: {len(valid)}\n")
                            f.write("=" * 60 + "\n\n")
                            f.write(content)
                        
                        print(f"\n✅ 内容已保存到: {filepath}")
                        return
        
        # 如果所有选择器都没找到内容
        print("\n❌ 所有选择器都未找到有效内容")
        print("\n[调试信息]")
        
        # 获取整个页面的文本
        full_text = crawler.get_text_content()
        print(f"页面文本长度: {len(full_text)} 字符")
        
        if full_text:
            print("\n页面文本预览（前500字符）:")
            print(full_text[:500])
            
            # 保存完整文本
            with open("debug_full_text.txt", "w", encoding="utf-8") as f:
                f.write(full_text)
            print("\n完整文本已保存到: debug_full_text.txt")
        
        # 获取页面 HTML
        html = crawler.get_page_content()
        print(f"\n页面 HTML 长度: {len(html)} 字符")
        
        # 保存 HTML
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("页面 HTML 已保存到: debug_page_source.html")
        
        print("\n💡 建议:")
        print("1. 查看 debug_page_source.html 找到正确的选择器")
        print("2. 查看 debug_full_text.txt 确认页面是否有内容")
        print("3. 可能需要登录才能查看完整内容")


def main():
    """
    主函数
    """
    # 七猫小说示例 URL
    url = "https://www.qimao.com/shuku/1834789-17167752050011/"
    
    debug_crawl_qimao(url)


if __name__ == "__main__":
    main()
