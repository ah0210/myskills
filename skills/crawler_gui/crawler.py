"""
Playwright 网页抓取核心功能
提供网页抓取、分页处理和内容选择功能
"""

from playwright.sync_api import sync_playwright
from typing import Dict, List, Optional, Any
import time


class WebCrawler:
    """
    Playwright 网页抓取器
    支持基本抓取、分页抓取和内容选择
    """
    
    def __init__(self, headless: bool = True):
        """
        初始化网页抓取器
        
        Args:
            headless: 是否使用无头浏览器
        """
        self.headless = headless
        self.browser = None
        self.page = None
    
    def __enter__(self):
        """
        进入上下文管理器
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=100  # 慢动作，便于调试
        )
        self.page = self.browser.new_page()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文管理器
        """
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def open_url(self, url: str, timeout: int = 30, wait_time: int = 3) -> bool:
        """
        打开指定 URL
        
        Args:
            url: 目标 URL
            timeout: 超时时间（秒）
            wait_time: 页面加载后等待时间（秒），用于动态内容加载
            
        Returns:
            是否成功打开
        """
        try:
            self.page.goto(url, timeout=timeout * 1000, wait_until="networkidle")
            time.sleep(wait_time)
            return True
        except Exception as e:
            print(f"打开 URL 失败: {e}")
            return False
    
    def get_page_content(self) -> str:
        """
        获取当前页面的 HTML 内容
        
        Returns:
            HTML 内容
        """
        try:
            return self.page.content()
        except Exception as e:
            print(f"获取页面内容失败: {e}")
            return ""
    
    def get_text_content(self) -> str:
        """
        获取当前页面的文本内容
        
        Returns:
            文本内容
        """
        try:
            return self.page.inner_text("body")
        except Exception as e:
            print(f"获取文本内容失败: {e}")
            return ""
    
    def extract_elements(self, selector: str) -> List[Dict[str, str]]:
        """
        提取指定选择器的元素
        
        Args:
            selector: CSS 选择器
            
        Returns:
            元素列表，每个元素包含文本和属性
        """
        try:
            elements = self.page.query_selector_all(selector)
            result = []
            for element in elements:
                try:
                    text = element.inner_text()
                    href = element.get_attribute("href") or ""
                    src = element.get_attribute("src") or ""
                    result.append({
                        "text": text,
                        "href": href,
                        "src": src,
                        "tag": element.tag_name()
                    })
                except Exception:
                    continue
            return result
        except Exception as e:
            print(f"提取元素失败: {e}")
            return []
    
    def extract_text_from_selector(self, selector: str) -> str:
        """
        提取指定选择器的文本内容
        
        Args:
            selector: CSS 选择器
            
        Returns:
            文本内容
        """
        try:
            element = self.page.query_selector(selector)
            if element:
                return element.inner_text()
            return ""
        except Exception as e:
            print(f"提取文本失败: {e}")
            return ""
    
    def wait_for_content(self, selector: str, timeout: int = 10) -> bool:
        """
        等待指定内容出现
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间（秒）
            
        Returns:
            是否成功等待到内容
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout * 1000, state="visible")
            return True
        except Exception as e:
            print(f"等待内容失败: {e}")
            return False
    
    def click_element(self, selector: str) -> bool:
        """
        点击指定元素
        
        Args:
            selector: CSS 选择器
            
        Returns:
            是否成功点击
        """
        try:
            element = self.page.query_selector(selector)
            if element:
                element.click()
                time.sleep(1)  # 等待页面加载
                return True
            return False
        except Exception as e:
            print(f"点击元素失败: {e}")
            return False
    
    def fill_input(self, selector: str, text: str) -> bool:
        """
        填充输入框
        
        Args:
            selector: CSS 选择器
            text: 要填充的文本
            
        Returns:
            是否成功填充
        """
        try:
            element = self.page.query_selector(selector)
            if element:
                element.fill(text)
                return True
            return False
        except Exception as e:
            print(f"填充输入框失败: {e}")
            return False
    
    def wait_for_selector(self, selector: str, timeout: int = 10) -> bool:
        """
        等待指定选择器出现
        
        Args:
            selector: CSS 选择器
            timeout: 超时时间（秒）
            
        Returns:
            是否成功等待到元素
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout * 1000)
            return True
        except Exception as e:
            print(f"等待选择器失败: {e}")
            return False
    
    def next_page(self, next_button_selector: str) -> bool:
        """
        点击下一页按钮
        
        Args:
            next_button_selector: 下一页按钮的 CSS 选择器
            
        Returns:
            是否成功翻页
        """
        return self.click_element(next_button_selector)
    
    def crawl_pagination(self, 
                        url: str, 
                        next_button_selector: str, 
                        content_selector: str, 
                        max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        分页抓取
        
        Args:
            url: 起始 URL
            next_button_selector: 下一页按钮的 CSS 选择器
            content_selector: 内容选择器
            max_pages: 最大抓取页数
            
        Returns:
            抓取的内容列表
        """
        results = []
        current_page = 1
        
        try:
            # 打开起始页，增加等待时间
            if not self.open_url(url, wait_time=5):
                return results
            
            while current_page <= max_pages:
                print(f"抓取第 {current_page} 页...")
                
                # 滚动页面以加载更多内容
                for i in range(3):
                    self.page.evaluate("window.scrollBy(0, 1000)")
                    time.sleep(2)
                
                # 等待内容加载
                time.sleep(3)
                
                # 提取内容
                elements = self.extract_elements(content_selector)
                
                # 如果是段落，过滤掉太短的
                if content_selector == "p" and elements:
                    elements = [e for e in elements if len(e['text'].strip()) > 20]
                
                results.extend(elements)
                
                # 尝试翻页
                if current_page < max_pages:
                    if not self.next_page(next_button_selector):
                        print("没有更多页面")
                        break
                    time.sleep(2)  # 等待新页面加载
                
                current_page += 1
                    
        except Exception as e:
            print(f"分页抓取失败: {e}")
        
        return results
    
    def crawl_with_options(self, 
                          url: str, 
                          content_selectors: Dict[str, str], 
                          next_button_selector: Optional[str] = None, 
                          max_pages: int = 1) -> List[Dict[str, Any]]:
        """
        带选项的抓取
        
        Args:
            url: 目标 URL
            content_selectors: 内容选择器字典，键为内容类型，值为 CSS 选择器
            next_button_selector: 下一页按钮的 CSS 选择器
            max_pages: 最大抓取页数
            
        Returns:
            抓取的内容列表
        """
        results = []
        current_page = 1
        
        try:
            # 打开 URL
            if not self.open_url(url):
                return results
            
            while current_page <= max_pages:
                print(f"抓取第 {current_page} 页...")
                
                # 提取各种内容
                page_content = {}
                for content_type, selector in content_selectors.items():
                    elements = self.extract_elements(selector)
                    page_content[content_type] = elements
                
                results.append({
                    "page": current_page,
                    "url": self.page.url,
                    "content": page_content
                })
                
                # 尝试翻页
                if next_button_selector and current_page < max_pages:
                    if not self.next_page(next_button_selector):
                        print("没有更多页面")
                        break
                else:
                    break
                
                current_page += 1
                
        except Exception as e:
            print(f"抓取失败: {e}")
        
        return results


def example_usage():
    """
    示例用法
    """
    with WebCrawler(headless=False) as crawler:
        # 基本抓取
        crawler.open_url("https://example.com")
        content = crawler.get_text_content()
        print(f"页面内容长度: {len(content)}")
        
        # 提取元素
        links = crawler.extract_elements("a")
        print(f"找到 {len(links)} 个链接")
        for link in links[:5]:
            print(f"{link['text']}: {link['href']}")


if __name__ == "__main__":
    example_usage()
