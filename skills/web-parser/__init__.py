"""
Jina Reader + Crawl4AI 双引擎网页解析器
提供灵活、强大的网页内容提取方案
"""

from .jina_reader import JinaReader
from .crawl4ai_parser import Crawl4AIParser
from .web_parser import WebParser

__version__ = "1.0.0"
__all__ = ["JinaReader", "Crawl4AIParser", "WebParser"]
