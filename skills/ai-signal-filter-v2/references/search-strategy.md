# 搜索策略

## 内容提取方式

### 主方案：web_fetch
使用 OpenClaw 原生 `web_fetch` 工具获取页面内容，参数：
- `extractMode`: markdown（默认，自动过滤广告和无用内容）
- `maxChars`: 10000（单次获取上限）

### 备选方案：markdown.new
web_fetch 失败时使用 markdown.new 服务：
- URL 格式：`https://markdown.new/{原始URL}`
- 适用场景：境外网站、web_fetch 超时或返回空内容
- 示例：`web_fetch(url: "https://markdown.new/https://openai.com/blog")`

通常 web_fetch 可满足需求，境外网站无法访问时启用备选。

---

## 语言策略

- **英文搜索**：模型发布、开源项目、国际行业动态、GitHub
- **中文搜索**：中国AI平台、国内政策、中文社区讨论
- **同一话题中英文各搜一次**：避免单一语言的信息茧房

---

## 信息源分级

### Tier 1（一手，可单独作为来源）

- 官方博客和公告
- GitHub release 页面、GitHub trending
- 论文页面（arXiv 等）
- 官方文档和 changelog

### Tier 2（聚合，需交叉验证）

- Hacker News 热帖
- Reddit（r/LocalLLaMA, r/MachineLearning, r/artificial 等）
- 技术社区首发文章（机器之心、量子位、InfoQ、36氪AI等）
- 中文社区：知乎AI话题热榜、掘金AI板块、少数派AI专栏
- 独立内容源：AI领域深度博主
- 国内大模型官方公告
- API status 页面
- 产品更新日志
- CSDN、博客园等技术博客中的工具推荐

### Tier 2+（垂直专业源，单源可进入"值得留意"区）

- AI 变现/副业垂直源（如自游人等专注于 AI 商业化的平台）
- 垂直领域专业媒体（单一领域信息密度高于通用媒体）

### Tier 3（分析，只能作为线索）

- 科技媒体深度文章（36kr 等）
- 行业分析师长文
- 播客摘要和访谈记录
- Newsletter（Ben's Bites, a16z AI 等）

---

## 搜索维度

每次执行从以下 12 个维度中选择至少 4 个轮换覆盖，避免与 history.md 最近 7 天重复。

1. **模型能力变化**：新发布、重大更新、能力变化、定价变化
   - 关键词：`AI model release update`, `AI模型发布更新`, `LLM benchmark update`, `大模型价格调整`

2. **工具生态变化**：新产品、重要更新、开源项目里程碑
   - 关键词：`AI tool launch`, `AI工具新品`, `AI open source release`, `开源AI项目更新`

3. **行业结构变化**：融资（战略级）、政策法规、大厂战略调整
   - 关键词：`AI funding`, `AI融资`, `AI policy regulation`, `AI政策法规`, `tech company AI strategy`

4. **办公生态**：新功能、集成变化、合作伙伴动态
   - 关键词：`productivity AI feature update`, `办公AI功能更新`, `workspace AI integration`

5. **开源社区动态**：重大 release、新框架、性能突破
   - 关键词：`open source AI release`, `开源AI框架`, `AI performance breakthrough`, `AI推理优化`

6. **AI 应用层**：新应用模式、用户行为变化、商业模式创新
   - 关键词：`AI application trend`, `AI应用趋势`, `AI business model`, `AI商业化`

7. **AI安全与对齐**：越狱方法、数据泄露、对齐突破、安全漏洞
   - 关键词：`AI security alignment`, `AI安全漏洞`, `大模型越狱`, `AI对齐突破`

8. **监管与合规**：国内生成式AI备案、欧盟AI法案落地、数据合规要求
   - 关键词：`AI regulation compliance`, `生成式AI备案`, `AI监管政策`, `数据合规要求`

9. **AI 赚钱**：变现方法、商业化路径、收入模式
   - 关键词：`AI make money`, `AI变现`, `AI赚钱方法`, `AI商业模式`, `AI revenue`, `AI副业`

10. **GitHub/开源工具**：新兴开源项目、GitHub trending、免费工具
    - 关键词：`GitHub trending AI`, `open source AI assistant free`, `awesome AI agents`
    - 搜索方法：除 web_search 外，可直接 web_fetch GitHub trending 页面

11. **中国AI生态**：运营商AI平台、央企AI战略、国产AI基础设施
    - 关键词：从用户画像关注清单动态生成（如用户关注的公司+`AI`）
    - 注意：用中文搜索为主

12. **AI编程工具/Agent工具**：编程助手、Agent框架、开发工具
    - 关键词：`AI coding assistant free`, `open source AI agent tool`, `AI编程工具`, `AI agent framework`
    - 补充：从用户画像自定义关键词中提取相关工具搜索词

---

## 关注清单驱动搜索

维度 11 和 12 的搜索词**不硬编码**，完全由用户画像的"关注清单"和"自定义关键词"驱动：

1. 读取 `memory/signal/profile.md` 中的"关注清单"和"自定义关键词"
2. 将关注清单中的公司/工具与维度主题组合生成搜索词
3. 将自定义关键词直接作为搜索词补充

---

## 搜索轮次规划

| 轮次 | 目的 | 维度范围 | 语言 |
|------|------|---------|------|
| 第1轮 | 宏观动态 | 从 1/3/7/8 中选 | 英文为主 |
| 第2轮 | 工具生态 | 从 2/5/10/12 中选 | 英文为主 |
| 第3轮 | 应用变现 | 从 4/6/9 中选 | 中文为主 |
| 第4轮 | 关注清单+补充 | 从 11 + 关注清单 + 自定义关键词中选 | 中英混合 |

每轮 1-2 个 web_search 查询，总计 4-8 个查询。维度选择避免与最近 7 天历史重复。

---

## 降权规则

以下信息自动降权，需要额外强的理由才能保留：

- 含"最强""颠覆""首个""史上"等营销词的 → 自动降权
- 纯跑分数据（未经实测验证的）→ 必须标注"未经实测验证"
- 小额融资新闻（除非改变了行业格局）→ 不报
- "XX 即将发布"（只有发布了才报）→ 不报预告

**例外（不降权）**：
- 匹配用户画像"关注清单"的信息 → 不因"小工具"降权
- 免费/开源工具且有明确 benchmark 对比 → 不因"小版本更新"降权
- 用户角色可直接使用的工具/平台 → 不因"非重大新闻"降权

> **降权 ≠ 通过门控**：降权后的信息仍需通过质量门控，不因降权而自动保留。如无法通过门控，删除。

---

## 交叉验证规则

- **今日信号区**：至少 2 个独立来源确认
- **值得留意区**：至少 1 个来源 + 1 个佐证
- **单一来源**：标注"待验证"，不能进"今日信号"
- **关注清单匹配项**：单一来源可进入"值得留意"区
- **垂直专业源**（Tier 2+）：单一来源可进入"值得留意"区

---

## 动态信息源

读取 `memory/signal/profile.md` 中的信息源评分部分获取动态评分。优先搜索高评分信息源，降低低评分源搜索频率。

搜索完成后，根据本次搜索结果更新 `memory/signal/profile.md` 的信息源评分：
- 某信息源产出的信号通过了质量门控 → 产出次数 +1，通过次数 +1
- 某信息源产出的信号被门控删除 → 产出次数 +1
