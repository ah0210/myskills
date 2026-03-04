# Jina Reader + Crawl4AI 双引擎网页解析器

一个强大、灵活的网页内容提取工具，结合 Jina Reader 和 Crawl4AI 的优势，提供智能双引擎解析能力。

## 功能特性

### 双引擎支持

- **Jina Reader**：快速、轻量级的网页内容提取
  - 自动去除广告、导航等无关内容
  - 适合快速获取文章正文
  - 无需安装额外浏览器驱动

- **Crawl4AI**：强大的网页爬取和内容提取
  - 支持动态渲染（JavaScript 执行）
  - 可提取结构化数据（markdown、HTML、链接、图片等）
  - 支持自定义提取规则和 CSS 选择器
  - 适合复杂网页和需要详细结构化数据的场景

### 智能选择

- 自动根据网页特点选择最佳引擎
- 提供降级机制，确保解析成功率
- 统一的 API 接口，简化使用

## 安装和设置

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器

### 步骤 1：创建虚拟环境

**Windows PowerShell:**

```powershell
# 进入技能包目录
cd skills/web-parser

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
# 进入技能包目录
cd skills/web-parser

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate
```

### 步骤 2：安装依赖

```powershell
# 安装所有依赖
pip install -r requirements.txt
```

### 步骤 3：验证安装

```python
from skills.web_parser import WebParser

# 测试解析器
parser = WebParser()
print("WebParser 初始化成功！")
```

## 快速开始

### 基础使用

```python
from skills.web_parser import WebParser

# 创建解析器实例（自动选择引擎）
parser = WebParser()

# 解析网页
url = "https://example.com/article"
content = parser.parse(url)
print(content)
```

### 指定引擎

```python
from skills.web_parser import WebParser

# 创建解析器实例
parser = WebParser()

# 使用 Jina Reader
content = parser.parse(url, engine="jina")

# 使用 Crawl4AI
content = parser.parse(url, engine="crawl4ai")
```

### 获取元数据

```python
from skills.web_parser import WebParser

parser = WebParser()

# 解析并获取元数据
metadata = parser.parse_with_metadata(url)
print(f"内容: {metadata['content']}")
print(f"引擎: {metadata['engine']}")
print(f"链接数: {len(metadata.get('links', []))}")
```

## 详细使用指南

### 1. Jina Reader 单独使用

```python
from skills.web_parser import JinaReader

# 创建 Jina Reader 实例
reader = JinaReader(timeout=30, retry_times=3)

# 提取网页内容
content = reader.extract("https://example.com/article")

# 提取并获取元数据
metadata = reader.extract_with_metadata("https://example.com/article")
print(f"状态码: {metadata['status_code']}")
print(f"内容长度: {len(metadata['content'])}")

# 检查服务是否可用
if reader.is_available():
    print("Jina Reader 服务可用")
```

### 2. Crawl4AI 单独使用

```python
from skills.web_parser import Crawl4AIParser
import asyncio

# 创建 Crawl4AI 解析器实例
parser = Crawl4AIParser(headless=True, timeout=30)

# 异步方式提取内容
async def extract_content():
    content = await parser.extract("https://example.com/article")
    print(content)

asyncio.run(extract_content())

# 同步方式提取内容
content = parser.extract_sync("https://example.com/article")

# 提取并获取元数据
metadata = parser.extract_with_metadata_sync("https://example.com/article")
print(f"HTML: {metadata['html'][:100]}...")
print(f"链接: {metadata['links']}")

# 提取所有链接
links = asyncio.run(parser.extract_links("https://example.com/article"))
for link in links:
    print(f"{link['text']}: {link['href']}")

# 提取所有图片
images = asyncio.run(parser.extract_images("https://example.com/article"))
for img in images:
    print(f"{img['alt']}: {img['src']}")

# 使用自定义 CSS 选择器
async def extract_custom():
    result = await parser.extract_custom(
        "https://example.com/article",
        css_selector="article.content"
    )
    print(result)

asyncio.run(extract_custom())
```

### 3. 双引擎智能解析

```python
from skills.web_parser import WebParser

# 创建解析器，设置首选引擎
parser = WebParser(prefer_engine="auto")

# 自动选择引擎解析
content = parser.parse("https://example.com/article")

# 检查 Jina Reader 是否可用
if parser.is_jina_available():
    print("Jina Reader 可用，将优先使用")
else:
    print("Jina Reader 不可用，将使用 Crawl4AI")
```

## 使用场景

### 场景 1：快速提取文章正文

```python
from skills.web_parser import JinaReader

reader = JinaReader()
url = "https://news.example.com/article/12345"

content = reader.extract(url)
print(content)
```

### 场景 2：提取动态渲染的网页

```python
from skills.web_parser import Crawl4AIParser

parser = Crawl4AIParser()
url = "https://spa.example.com/data"

content = parser.extract_sync(url)
print(content)
```

### 场景 3：批量处理多个网页

```python
from skills.web_parser import WebParser
import concurrent.futures

parser = WebParser()
urls = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3"
]

# 并发处理
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(parser.parse, urls))

for i, content in enumerate(results):
    print(f"文章 {i+1}: {len(content)} 字符")
```

### 场景 4：提取结构化数据

```python
from skills.web_parser import Crawl4AIParser
import asyncio

async def extract_structured_data(url):
    parser = Crawl4AIParser()
    metadata = await parser.extract_with_metadata(url)
    
    return {
        "title": metadata["content"].split("\n")[0],
        "content": metadata["content"],
        "links": metadata["links"],
        "images": metadata["images"]
    }

data = asyncio.run(extract_structured_data("https://example.com/article"))
print(data)
```

## 配置选项

### JinaReader 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| timeout | int | 30 | 请求超时时间（秒） |
| retry_times | int | 3 | 失败重试次数 |

### Crawl4AIParser 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| headless | bool | True | 是否使用无头浏览器 |
| timeout | int | 30 | 超时时间（秒） |

### WebParser 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prefer_engine | str | "auto" | 首选引擎 ("auto", "jina", "crawl4ai") |

## 最佳实践

1. **快速提取**：优先使用 Jina Reader，速度快且简单
2. **复杂网页**：使用 Crawl4AI 处理需要 JavaScript 渲染的网页
3. **结构化数据**：Crawl4AI 提供更丰富的结构化数据提取能力
4. **错误处理**：实现双引擎切换机制，提高成功率
5. **性能优化**：对于批量任务，考虑使用并发处理

## 注意事项

1. **Jina Reader 限制**
   - 有速率限制，大量请求时请注意控制频率
   - 某些网站可能无法访问

2. **Crawl4AI 要求**
   - 需要安装浏览器驱动（如 Playwright），首次使用会自动下载
   - 占用资源较多，不适合大规模并发

3. **反爬机制**
   - 某些网站可能有反爬机制，请遵守网站的 robots.txt 规则
   - 敏感信息（如登录后的页面）可能需要额外的认证处理

4. **虚拟环境**
   - 始终在虚拟环境中使用此技能包
   - 不同项目应使用独立的虚拟环境

## 故障排除

### Jina Reader 无法访问

**问题**：Jina Reader 返回错误或超时

**解决方案**：
- 检查网络连接
- 确认目标网站是否可访问
- 尝试使用 Crawl4AI 作为替代方案
- 增加 timeout 参数

### Crawl4AI 渲染失败

**问题**：Crawl4AI 无法正确渲染网页

**解决方案**：
- 确认已安装浏览器驱动
- 检查网络连接
- 增加超时时间设置
- 尝试关闭 headless 模式查看浏览器行为

### 提取内容不完整

**问题**：提取的内容不完整或格式错误

**解决方案**：
- 尝试使用不同的提取策略
- 检查网页是否需要 JavaScript 渲染
- 考虑使用 CSS 选择器精确提取
- 检查目标网站是否有反爬机制

### 虚拟环境问题

**问题**：无法激活虚拟环境或导入模块失败

**解决方案**：
- 确认 Python 版本 >= 3.8
- 重新创建虚拟环境
- 重新安装依赖：`pip install -r requirements.txt`
- 检查虚拟环境路径是否正确

## 文件结构

```
skills/web-parser/
├── __init__.py              # 模块初始化文件
├── jina_reader.py           # Jina Reader 实现
├── crawl4ai_parser.py       # Crawl4AI 实现
├── web_parser.py             # 双引擎智能解析器
├── requirements.txt         # 依赖列表
├── .venv-config            # 虚拟环境配置
├── README.md               # 使用文档
└── examples/               # 示例代码
    ├── basic_usage.py      # 基础使用示例
    ├── advanced_usage.py  # 高级用法示例
    └── batch_processing.py # 批量处理示例
```

## 更新日志

### v1.0.0 (2026-03-04)

- 初始版本发布
- 支持 Jina Reader 和 Crawl4AI 双引擎
- 提供智能引擎选择机制
- 完整的文档和示例代码

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 Issue 联系。
