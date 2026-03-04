"""
Jina Reader 网页内容提取器
提供快速、轻量级的网页内容提取功能
"""

import requests
from typing import Optional, Dict, Any
import time


class JinaReader:
    """
    Jina Reader 网页内容提取器
    
    使用 Jina Reader API 快速提取网页正文内容
    自动去除广告、导航等无关内容
    """
    
    def __init__(self, timeout: int = 30, retry_times: int = 3):
        """
        初始化 Jina Reader
        
        Args:
            timeout: 请求超时时间（秒）
            retry_times: 失败重试次数
        """
        self.timeout = timeout
        self.retry_times = retry_times
        self.base_url = "https://r.jina.ai/"
    
    def extract(self, url: str) -> str:
        """
        提取网页内容
        
        Args:
            url: 目标网页 URL
            
        Returns:
            提取的文本内容
            
        Raises:
            requests.RequestException: 请求失败时抛出
        """
        jina_url = f"{self.base_url}{url}"
        
        for attempt in range(self.retry_times):
            try:
                response = requests.get(jina_url, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt == self.retry_times - 1:
                    raise
                time.sleep(1)
    
    def extract_with_metadata(self, url: str) -> Dict[str, Any]:
        """
        提取网页内容并返回元数据
        
        Args:
            url: 目标网页 URL
            
        Returns:
            包含内容和元数据的字典
        """
        jina_url = f"{self.base_url}{url}"
        
        for attempt in range(self.retry_times):
            try:
                response = requests.get(jina_url, timeout=self.timeout)
                response.raise_for_status()
                
                return {
                    "content": response.text,
                    "url": url,
                    "status_code": response.status_code,
                    "engine": "jina-reader"
                }
            except requests.RequestException as e:
                if attempt == self.retry_times - 1:
                    raise
                time.sleep(1)
    
    def is_available(self) -> bool:
        """
        检查 Jina Reader 服务是否可用
        
        Returns:
            服务是否可用
        """
        try:
            response = requests.get(f"{self.base_url}https://example.com", timeout=5)
            return response.status_code == 200
        except:
            return False
