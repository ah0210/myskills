# 七猫小说抓取示例

这个示例演示如何使用 Playwright 抓取七猫小说网站的内容。

## 使用方法

### 1. 确保已安装依赖

```powershell
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 确认依赖已安装
pip list | Select-String playwright
```

### 2. 运行示例脚本

```powershell
# 进入 examples 目录
cd examples

# 运行七猫小说抓取示例
python crawl_qimao.py
```

### 3. 查看结果

- 抓取的内容会保存在 `output` 目录
- 如果抓取失败，会生成 `page_source.html` 文件，用于分析页面结构

## 功能说明

### 主要改进

1. **等待动态内容加载**
   - 使用 `wait_until="networkidle"` 等待网络空闲
   - 增加额外的等待时间（5秒）
   - 确保动态内容完全加载

2. **多选择器尝试**
   - 自动尝试多个常见的内容选择器
   - 找到第一个有效的内容就使用

3. **有头模式调试**
   - 默认使用有头模式，可以看到浏览器行为
   - 便于调试和找到正确的选择器

4. **错误处理**
   - 如果抓取失败，会保存页面 HTML 用于分析
   - 提供详细的日志信息

## 自定义抓取

### 修改目标 URL

编辑 `crawl_qimao.py` 文件，修改 `url` 变量：

```python
url = "https://www.qimao.com/shuku/YOUR_NOVEL_ID/"
```

### 添加新的选择器

如果默认选择器无法找到内容，可以添加新的选择器：

```python
content_selectors = [
    ".chapter-content",
    ".content-text",
    ".read-content",
    "article",
    ".text-content",
    "p",
    # 添加你的选择器
    ".your-custom-selector",
]
```

### 如何找到正确的选择器

1. **使用浏览器开发者工具**
   - 在浏览器中打开目标网页
   - 按 F12 打开开发者工具
   - 使用元素选择器（左上角箭头图标）
   - 点击小说内容区域
   - 查看元素的 class 或 id

2. **查看保存的 HTML**
   - 如果抓取失败，会生成 `page_source.html`
   - 用文本编辑器打开，搜索小说内容
   - 找到包含内容的 HTML 标签和 class

## 常见问题

### 1. 抓取不到内容

**原因**：
- 网站使用了复杂的 JavaScript 渲染
- 内容选择器不正确
- 需要登录才能查看

**解决方法**：
- 增加等待时间
- 使用有头模式查看页面加载过程
- 查看保存的 HTML 找到正确的选择器

### 2. 内容不完整

**原因**：
- 页面加载时间不够
- 内容需要滚动才能加载

**解决方法**：
- 增加等待时间
- 添加滚动逻辑

### 3. 需要登录

**原因**：
- 某些小说需要登录才能查看

**解决方法**：
- 使用有头模式，手动登录后再抓取
- 或者使用 cookies 自动登录

## 扩展功能

### 批量抓取多章节

```python
# 示例：抓取多个章节
chapters = [
    "https://www.qimao.com/shuku/1834789-17167752040008/",
    "https://www.qimao.com/shuku/1834789-17167752040009/",
    # 更多章节...
]

for chapter_url in chapters:
    crawl_qimao_novel(chapter_url)
    time.sleep(2)  # 避免请求过快
```

### 保存为其他格式

```python
# 保存为 JSON
import json

data = {
    "url": url,
    "content": content,
    "timestamp": datetime.datetime.now().isoformat()
}

with open("novel.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 注意事项

1. **遵守网站规则**
   - 不要过度抓取，避免对服务器造成压力
   - 遵守网站的 robots.txt 规则
   - 尊重版权

2. **合法使用**
   - 仅用于学习和研究目的
   - 不要用于商业用途
   - 不要传播抓取的内容

3. **技术限制**
   - 某些网站有反爬机制
   - 可能需要处理验证码
   - IP 可能被封禁

## 许可证

MIT License
