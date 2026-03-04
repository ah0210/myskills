"""
双引擎智能网页解析器
根据网页特点自动选择最佳解析引擎
"""

from typing import Optional, Dict, Any, Literal
from .jina_reader import JinaReader
from .crawl4ai_parser import Crawl4AIParser


class WebParser:
    """
    双引擎智能网页解析器
    
    自动选择 Jina Reader 或 Crawl4AI 进行网页内容提取
    提供统一的接口和智能降级机制
    """
    
    def __init__(self, prefer_engine: Literal["auto", "jina", "crawl4ai"] = "auto"):
        """
        初始化双引擎解析器
        
        Args:
            prefer_engine: 首选引擎 ("auto", "jina", "crawl4ai")
        """
        self.prefer_engine = prefer_engine
        self.jina_reader = JinaReader()
        self.crawl4ai_parser = Crawl4AIParser()
    
    def parse(self, url: str, engine: Optional[str] = None) -> str:
        """
        解析网页内容
        
        Args:
            url: 目标网页 URL
            engine: 指定使用的引擎 ("jina", "crawl4ai", None 表示自动选择)
            
        Returns:
            解析后的文本内容
        """
        if engine == "jina":
            return self._parse_with_jina(url)
        elif engine == "crawl4ai":
            return self._parse_with_crawl4ai(url)
        else:
            return self._parse_auto(url)
    
    def parse_with_metadata(self, url: str, engine: Optional[str] = None) -> Dict[str, Any]:
        """
        解析网页内容并返回元数据
        
        Args:
            url: 目标网页 URL
            engine: 指定使用的引擎 ("jina", "crawl4ai", None 表示自动选择)
            
        Returns:
            包含内容和元数据的字典
        """
        if engine == "jina":
            return self.jina_reader.extract_with_metadata(url)
        elif engine == "crawl4ai":
            return self.crawl4ai_parser.extract_with_metadata_sync(url)
        else:
            return self._parse_auto_with_metadata(url)
    
    def _parse_auto(self, url: str) -> str:
        """
        自动选择引擎解析网页
        
        Args:
            url: 目标网页 URL
            
        Returns:
            解析后的文本内容
        """
        if self.prefer_engine == "jina":
            try:
                content = self.jina_reader.extract(url)
                if len(content) > 100:
                    return content
            except Exception:
                pass
            return self._parse_with_crawl4ai(url)
        elif self.prefer_engine == "crawl4ai":
            return self._parse_with_crawl4ai(url)
        else:
            try:
                content = self.jina_reader.extract(url)
                if len(content) > 100:
                    return content
            except Exception:
                pass
            return self._parse_with_crawl4ai(url)
    
    def _parse_auto_with_metadata(self, url: str) -> Dict[str, Any]:
        """
        自动选择引擎解析网页并返回元数据
        
        Args:
            url: 目标网页 URL
            
        Returns:
            包含内容和元数据的字典
        """
        if self.prefer_engine == "jina":
            try:
                metadata = self.jina_reader.extract_with_metadata(url)
                if len(metadata["content"]) > 100:
                    return metadata
            except Exception:
                pass
            return self.crawl4ai_parser.extract_with_metadata_sync(url)
        elif self.prefer_engine == "crawl4ai":
            return self.crawl4ai_parser.extract_with_metadata_sync(url)
        else:
            try:
                metadata = self.jina_reader.extract_with_metadata(url)
                if len(metadata["content"]) > 100:
                    return metadata
            except Exception:
                pass
            return self.crawl4ai_parser.extract_with_metadata_sync(url)
    
    def _parse_with_jina(self, url: str) -> str:
        """
        使用 Jina Reader 解析网页
        
        Args:
            url: 目标网页 URL
            
        Returns:
            解析后的文本内容
        """
        return self.jina_reader.extract(url)
    
    def _parse_with_crawl4ai(self, url: str) -> str:
        """
        使用 Crawl4AI 解析网页
        
        Args:
            url: 目标网页 URL
            
        Returns:
            解析后的文本内容
        """
        return self.crawl4ai_parser.extract_sync(url)
    
    def is_jina_available(self) -> bool:
        """
        检查 Jina Reader 是否可用
        
        Returns:
            是否可用
        """
        return self.jina_reader.is_available()
