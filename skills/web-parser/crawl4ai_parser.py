"""
Crawl4AI 网页解析器
提供强大的网页爬取和结构化数据提取功能
"""

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from typing import Optional, Dict, Any, List
import asyncio


class Crawl4AIParser:
    """
    Crawl4AI 网页解析器
    
    支持动态渲染、结构化数据提取和自定义提取规则
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        """
        初始化 Crawl4AI 解析器
        
        Args:
            headless: 是否使用无头浏览器
            timeout: 超时时间（秒）
        """
        self.headless = headless
        self.timeout = timeout
        self.browser_config = BrowserConfig(
            headless=headless,
            verbose=False
        )
    
    async def extract(self, url: str) -> str:
        """
        提取网页内容（Markdown 格式）
        
        Args:
            url: 目标网页 URL
            
        Returns:
            Markdown 格式的网页内容
        """
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url)
            return result.markdown
    
    async def extract_with_metadata(self, url: str) -> Dict[str, Any]:
        """
        提取网页内容并返回元数据
        
        Args:
            url: 目标网页 URL
            
        Returns:
            包含内容和元数据的字典
        """
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url)
            
            return {
                "content": result.markdown,
                "html": result.html,
                "url": url,
                "links": result.links,
                "images": result.images,
                "media": result.media,
                "engine": "crawl4ai"
            }
    
    async def extract_custom(self, url: str, css_selector: Optional[str] = None) -> Dict[str, Any]:
        """
        使用自定义选择器提取网页内容
        
        Args:
            url: 目标网页 URL
            css_selector: CSS 选择器
            
        Returns:
            提取的自定义数据
        """
        config = CrawlerRunConfig()
        
        if css_selector:
            config.css_selector = css_selector
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url, config=config)
            
            return {
                "content": result.markdown,
                "html": result.html,
                "url": url,
                "engine": "crawl4ai-custom"
            }
    
    async def extract_links(self, url: str) -> List[Dict[str, str]]:
        """
        提取网页中的所有链接
        
        Args:
            url: 目标网页 URL
            
        Returns:
            链接列表
        """
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url)
            return result.links
    
    async def extract_images(self, url: str) -> List[Dict[str, str]]:
        """
        提取网页中的所有图片
        
        Args:
            url: 目标网页 URL
            
        Returns:
            图片列表
        """
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url)
            return result.images
    
    def extract_sync(self, url: str) -> str:
        """
        同步方式提取网页内容
        
        Args:
            url: 目标网页 URL
            
        Returns:
            Markdown 格式的网页内容
        """
        return asyncio.run(self.extract(url))
    
    def extract_with_metadata_sync(self, url: str) -> Dict[str, Any]:
        """
        同步方式提取网页内容并返回元数据
        
        Args:
            url: 目标网页 URL
            
        Returns:
            包含内容和元数据的字典
        """
        return asyncio.run(self.extract_with_metadata(url))
