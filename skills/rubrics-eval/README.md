# Rubrics Eval - LLM Agent 评测工具

## 版本信息
- 当前版本：v2.3.1 (OpenClaw定制版)
- 适配环境：OpenClaw 2026.4.15+

## 功能说明
专业的LLM Agent质量评测工具，基于五层10分制架构，支持多模型对比评测：

| 层级 | 权重 | 满分 | 说明 |
|------|------|------|------|
| 第一层：基础能力 | 20% | 2.0 分 | 逻辑推理、事实准确性、上下文记忆等 |
| 第二层：工具专项能力 | 35% | 3.5 分 | 文件读写、代码执行、网络搜索等Agent核心能力 |
| 第三层：场景化适配能力 | 20% | 2.0 分 | 写代码、写文档、Debug、数据分析等实际场景 |
| 第四层：性能&安全能力 | 15% | 1.5 分 | 幻觉抗性、长对话稳定性等 |
| 第五层：惩罚/奖励项 | 10% | 1.0 分 | 幻觉/错误扣分，零错误奖励 |

## 核心特性
✅ 三层纠偏机制：难度系数修正 + 基准线归一化 + 高分压缩，彻底解决分数虚高
✅ 第三方独立打分：固定使用yama模型作为裁判，杜绝自答自评
✅ 全自动评测：通过OpenClaw子会话能力自动调用不同模型答题
✅ 批量对比：支持多模型横向对比，自动生成排名和推荐建议

## 运行环境要求
1. OpenClaw版本 ≥ 2026.4.15
2. 已配置待评测模型和打分模型（请在 `config.json` 中配置）
3. 子代理功能正常启用（全自动模式）

## ⚙️ 首次使用 - 配置模型

**重要：所有模型名称已从硬编码改为配置文件管理！**

1. 打开 `config.json` 配置文件
2. 修改 `被测模型映射`，将键值对改为您环境中的实际模型名称
3. 修改 `打分模型` 为您用作第三方评测裁判的模型名称
4. 调整 `评测设置` 中的参数（随机抽题数量、超时时间等）

配置示例：
```json
{
  "被测模型映射": {
    "model1": "your-org/model-a",
    "model2": "your-org/model-b"
  },
  "打分模型": "your-org/judge-model",
  "默认被测模型": "model1",
  "评测设置": {
    "随机抽题数量": 5,
    "题目超时秒数": 120
  }
}
```

## 使用方法

### 1. 单个模型评测
```bash
# ✅ 推荐：增量评测（随机抽取5道题，数量可配置）
python3 scripts/rubrics.py eval model model1 --random5 --manual

# 完整评测（19道题）
python3 scripts/rubrics.py eval model model1

# 快速评测（5道基础题）
python3 scripts/rubrics.py eval model model1 --quick

# 盲测模式
python3 scripts/rubrics.py eval model model1 --blind
```

**增量评测特性：**
- 每次从全部题库随机抽取 N 道题（默认5道，可在 config.json 修改）
- 自动按层级均衡抽样，确保各维度都有覆盖
- 多次评测结果可逐步积累，形成完整画像
- 适合 CI/CD 持续集成场景，每次提交跑少量题目

### 2. 批量多模型对比
```bash
# 批量评测多个模型（模型名称在 config.json 中配置）
python3 scripts/rubrics.py eval batch model1,model2,model3 --quick

# 增量批量对比（每个模型随机抽5题）
python3 scripts/rubrics.py eval batch model1,model2 --random5 --manual
```

### 3. 查看历史评测
```bash
python3 scripts/rubrics.py eval history
```

### 4. 生成评测报告
```bash
python3 scripts/rubrics.py eval report
```

## 问题排查与解决方案

### 常见问题汇总
详细的问题描述与解决方案请参考：[评测问题与解决方案.md](./评测问题与解决方案.md)

### 快速问题导航
1. **API插件未启用**：参考「评测问题与解决方案.md」中问题1，可选择启用插件或使用手动模式
2. **sessions-spawn插件未启用**：参考「评测问题与解决方案.md」中问题2
3. **非交互式环境input()报错**：参考「评测问题与解决方案.md」中问题3
4. **批量评测空跑得分为0**：参考「评测问题与解决方案.md」中问题4
5. **yama模型不可用**：修改脚本`grade_answer`函数，使用其他可用模型作为临时打分模型

## 历史修改记录
### 2026-04-20 OpenClaw定制版
1. 重构`call_model`函数，使用sessions_spawn子会话实现模型调用，不需要API插件
2. 适配OpenClaw多Agent配置，支持调用rose/tulip/bamboo/oak/yama等模型
3. 优化错误处理，增加详细的失败日志
4. 完善README文档，沉淀部署和使用经验

## 适配方案讨论沉淀
### 为什么不使用API插件？
- OpenClaw默认不启用API插件，需要修改配置
- 子会话能力是OpenClaw原生功能，更安全更稳定
- 不需要额外配置，开箱即用

### 多模型调用原理
- 利用OpenClaw的多Agent配置，每个模型对应一个Agent ID
- 通过sessions_spawn创建对应Agent的子会话，实现不同模型调用
- 子会话独立运行，不会影响主会话状态

### 打分机制说明
- 固定使用yama作为第三方打分模型，保证评测公平性
- 所有模型使用同一套评测标准，结果横向可比
- 强制扣分规则，杜绝感情分和放水
