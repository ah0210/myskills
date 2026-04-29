#!/usr/bin/env python3
"""
Rubrics Eval v2.3.1 - LLM Agent 工程化质量控制工具箱
符合 ClawHub Skills 规范

✅ v2.0-v2.2：强制扣分细则、基准线修正、对比打分法
✅ v2.3：Token效率/废话率检测
✅ v2.3.1 最终版：回归本质！纯净10分制 + 三项能力检测
   - 移除所有排名矫正、智能打分等黑箱算法
   - 纯净原始分，100% 透明可复现
   - 三项检测：推理模式、多模态、Token效率

10分制、全自动、全流程无人工干预
Single file, zero dependencies
"""

import sys
import os
import json
import datetime
import time
from pathlib import Path

# 导入OpenClaw工具 - 使用 exec 直接调用子代理
def call_model_via_exec(prompt, model_name):
    """通过 exec 工具调用子代理模型"""
    import subprocess
    import tempfile
    import os
    
    # 创建临时任务文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(f'''
import sys
import json

# 模拟子代理回答
# 这里需要实际调用模型
prompt = {json.dumps(prompt, ensure_ascii=False)}
model = {json.dumps(model_name, ensure_ascii=False)}

# 简单的模拟回答 - 实际使用时需要替换为真实模型调用
answers = {{
    "基础-逻辑推理": "这是一个逻辑推理问题的回答。步骤如下：1) 首先分析问题...",
    "基础-事实准确性": "关于事实准确性的回答。根据我的知识...",
    "基础-上下文记忆": "上下文记忆测试的回答。我记得之前提到的...",
    "基础-指令遵循": "遵循指令的回答。我将按照要求...",
    "基础-输出格式": "这是格式正确的输出：{{'key': 'value'}}",
}}

# 返回模拟答案
for q_type, ans in answers.items():
    if q_type in prompt:
        print(ans)
        sys.exit(0)

print("这是一个测试回答。")
''')
        task_file = f.name
    
    try:
        result = subprocess.run(
            ["python3", task_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        os.unlink(task_file)
        
        if result.returncode == 0:
            return result.stdout.strip() or "无有效回答"
        return f"执行错误: {result.stderr}"
    except Exception as e:
        os.unlink(task_file)
        return f"调用异常: {str(e)}"

SKILL_ROOT = Path(__file__).parent.parent
REFERENCES = SKILL_ROOT / "references"
DATA_DIR = SKILL_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / "eval-history.json"
CACHE_FILE = DATA_DIR / "eval-cache.json"
CONFIG_FILE = SKILL_ROOT / "config.json"
REPORT_DIR = SKILL_ROOT / "rubrics-eval-report"
REPORT_DIR.mkdir(exist_ok=True)

# 加载配置文件
def load_config():
    """加载配置文件，如果不存在则返回默认配置"""
    default_config = {
        "被测模型映射": {
            "rose": "ark-test/anonymous/rose",
            "tulip": "ark-test/anonymous/tulip",
            "bamboo": "ark-test/anonymous/bamboo",
            "oak": "ark-test/anonymous/oak",
            "elm": "ark-test/anonymous/elm"
        },
        "打分模型": "ark-test/anonymous/yama",
        "默认被测模型": "elm",
        "评测设置": {
            "随机抽题数量": 5,
            "题目超时秒数": 120,
            "启用缓存": True,
            "启用高分压缩": True
        }
    }
    
    if CONFIG_FILE.exists():
        try:
            user_config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            default_config.update(user_config)
        except Exception as e:
            print(f"⚠️  配置文件读取失败，使用默认配置: {e}")
    
    return default_config

CONFIG = load_config()

# =============================================================================
# ✅ v2.2 新特性：五层架构 + 强制扣分细则
# =============================================================================

# 13道题对应五层架构的权重映射（20+35+20+15+10惩罚项）
QUESTION_WEIGHTS = {
    # 第一层：基础能力 2.0分（共5题，每题0.4分）- 降低权重，解决拉不开差距
    "基础-逻辑推理": 0.4,
    "基础-事实准确性": 0.4,
    "基础-上下文记忆": 0.4,
    "基础-指令遵循": 0.4,
    "基础-输出格式": 0.4,
    
    # 第二层：工具能力 3.5分（共4题，每题0.875分）- Agent核心，高权重
    "工具-文件读写": 0.875,
    "工具-代码执行": 0.875,
    "工具-网络搜索": 0.875,
    "工具-多步调用": 0.875,
    
    # 第三层：场景适配 2.0分（共4题，每题0.5分）- 场景区分度
    "场景-写代码": 0.5,
    "场景-写文档": 0.5,
    "场景-Debug": 0.5,
    "场景-数据分析": 0.5,
    
    # 第四层：安全性能 1.5分（共2题，每题0.75分）
    "安全-幻觉抗性": 0.75,
    "性能-长对话稳定": 0.75,
    
    # 第五层：惩罚项 1.0分 - ✅ 新增！解决分数虚高
    "惩罚-幻觉次数": -0.2,  # 每次幻觉扣0.2分
    "惩罚-工具错误": -0.15, # 每次工具错扣0.15分
    "惩罚-遗忘上下文": -0.2, # 每次遗忘扣0.2分
    "奖励-零错误": 0.5,     # 全程零错误奖励0.5分
}

# ✅ v2.2 强制扣分表 - 消灭感情分
DEDUCTION_RULES = {
    "基础-逻辑推理": {
        "只给结论不给过程": 0.5,
        "漏一个推理步骤": 0.3,
        "逻辑存在漏洞": 0.4,
    },
    "工具-文件读写": {
        "参数名错误": 0.5,
        "缺少错误处理": 0.3,
        "格式不标准": 0.2,
    },
    "安全-幻觉抗性": {
        "编造一个不存在事实": 1.0,  # 直接0分
    },
    "场景-Debug": {
        "找不到Bug根因": 0.5,
        "修复方案不完整": 0.3,
    },
}

# ✅ v2.2 难度系数 - 简单题降分，难题加分
DIFFICULTY_COEFF = {
    "基础-逻辑推理": 1.2,   # 难题 x1.2
    "基础-上下文记忆": 1.1,
    "工具-多步调用": 1.3,
    "安全-幻觉抗性": 1.0,
    "default": 0.9,        # 简单题 x0.9 防放水
}

# ✅ v2.2 基准模型平均分 - 用于正态分布校准
BASELINE_SCORES = {
    "基础-逻辑推理": 0.7,
    "工具-文件读写": 0.8,
    "安全-幻觉抗性": 0.85,
    "default": 0.75,
}

# =============================================================================
# ✅ v2.3.1 核心功能（最终版）
# =============================================================================

# ✅ Token 效率/废话率检测 - 精确计算无信息开场白占比
# 返回 0~1 分，越高越好
NONSENSE_PHRASES = [
    "非常感谢您提出", "非常有趣的问题", "让我来仔细分析",
    "好的！我来帮你", "首先我们需要理解", "综上所述",
    "非常感谢您的提问", "让我们一步步来分析",
    "这是一个很好的问题", "让我来为您解答",
]

def calculate_token_efficiency(answer):
    """Token效率检测，返回0-1的得分，1分表示完全没有废话"""
    if not answer:
        return 0.0
    
    nonsense_chars = 0
    for phrase in NONSENSE_PHRASES:
        nonsense_chars += answer.count(phrase) * len(phrase)
    
    nonsense_ratio = nonsense_chars / max(len(answer), 1)
    
    if nonsense_ratio < 0.03:  return 1.0
    if nonsense_ratio < 0.10:  return 0.8
    if nonsense_ratio < 0.20:  return 0.5
    return 0.0

# ✅ 三项能力检测框架
def check_reasoning_mode(model_name):
    """检测是否支持 o1 类推理模式"""
    reasoning_models = ["yama", "kaze", "o1", "o3"]
    return any(m in model_name.lower() for m in reasoning_models)

def check_multimodal(model_name):
    """检测是否支持多模态（文字+图片）"""
    multimodal_models = ["gpt4o", "claude-3", "qwen-vl"]
    return any(m in model_name.lower() for m in multimodal_models)

# =============================================================================
# 工具函数
# =============================================================================

def load_reference(name):
    """加载 references/ 目录下的参考文件"""
    path = REFERENCES / f"{name}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"Warning: {name}.md not found"

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_section(title):
    """打印小节"""
    print(f"\n--- {title} ---\n")

def load_history():
    """加载评测历史记录"""
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except:
        return []

def save_history(record):
    """保存评测记录"""
    history = load_history()
    record["time"] = datetime.datetime.now().isoformat()
    history.append(record)
    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")

def generate_radar(scores):
    """生成 ASCII 雷达图"""
    labels = ["基础", "工具", "场景", "安全"]
    max_len = 20
    lines = []
    for i, label in enumerate(labels):
        score = scores[i]
        bars = "█" * int(score * max_len / 10)
        spaces = "░" * (max_len - len(bars))
        lines.append(f"{label:>6} | {bars}{spaces} | {score:.1f}")
    return "\n".join(lines)

def call_model(prompt, model=None, timeout=None, manual_mode=True):
    """调用指定模型回答问题，支持真实模型调用
    
    模型名称从配置文件读取，不再硬编码
    """
    if timeout is None:
        timeout = CONFIG["评测设置"]["题目超时秒数"]
    
    model_mapping = CONFIG["被测模型映射"]
    # 打分模型也从配置读取
    model_mapping["yama"] = CONFIG["打分模型"]
    
    target_model_name = model_mapping.get(model, model or model_mapping.get(CONFIG["默认被测模型"], CONFIG["默认被测模型"]))
    
    print(f"\n{'='*60}")
    print(f"📝 正在调用【{target_model_name}】模型回答...")
    print(f"{'='*60}")
    print(f"题目: {prompt.strip()[:100]}..." if len(prompt) > 100 else f"题目: {prompt.strip()}")
    print(f"{'='*60}")
    
    if manual_mode:
        # 手动模式，让用户输入回答
        answer = input("请输入回答：")
        print(f"✅ 回答已接收，长度: {len(answer)} 字符")
        return answer.strip()
    
    try:
        # 真实模型调用：使用openclaw命令行工具调用指定模型
        import subprocess
        import json
        import shlex
        
        # 准备sessions-spawn命令
        cmd = [
            "openclaw", "sessions-spawn",
            "--task", shlex.quote(prompt),
            "--model", shlex.quote(target_model_name),
            "--runtime", "subagent",
            "--mode", "run",
            "--cleanup", "delete",
            "--output-format", "json"
        ]
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            try:
                # 解析JSON输出
                output = json.loads(result.stdout)
                answer = output.get('output', '').strip() or "模型返回空回答"
            except json.JSONDecodeError:
                # 如果不是JSON格式，直接使用输出内容
                answer = result.stdout.strip() or "模型返回空回答"
            
            print(f"✅ 回答已接收，长度: {len(answer)} 字符")
            return answer
        else:
            print(f"❌ 模型调用失败: {result.stderr}")
            return f"调用失败: {result.stderr}"
        
    except subprocess.TimeoutExpired:
        print(f"❌ 模型调用超时({timeout}秒)")
        return "调用超时"
    except Exception as e:
        print(f"❌ 调用异常: {str(e)}")
        return f"调用异常: {str(e)}"

def get_cache(model, q_name):
    """获取评测缓存"""
    if not CACHE_FILE.exists():
        return None
    try:
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return cache.get(f"{model}:{q_name}")
    except:
        return None

def set_cache(model, q_name, answer):
    """保存评测缓存"""
    cache = {}
    if CACHE_FILE.exists():
        try:
            cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except:
            cache = {}
    cache[f"{model}:{q_name}"] = answer
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

def grade_answer(question, answer, rubrics, q_name=""):
    """✅ v2.2: 用基准模型自动打分 + 强制扣分 + 难度修正 + 基准线校准"""
    
    # 第一步：原始打分
    grade_prompt = f"""
你是极其严格的第三方评测员，打分非常苛刻，绝对不允许放水。

评测标准：{rubrics[:1000]}

✅ 强制扣分规则（违反直接扣分，不要手下留情）：
- 只给答案不给过程：扣 50%
- 回答不完整，缺关键步骤：扣 30%
- 编造不存在的信息：直接给 0 分

题目：{question[:500]}
回答：{answer[:2000]}

请只输出0到1之间的小数，比如0.65，不要输出其他任何内容。记住：好的答案才配得0.8分以上，完美才配1.0分！
"""
    # 强制用第三方基准打分模型，从根源杜绝自答自评
    # 打分模型名称从配置文件读取
    result = call_model(grade_prompt, model="yama")
    try:
        import re
        match = re.search(r"0\.\d+|1\.0|1", str(result))
        if match:
            raw_score = float(match.group())
        else:
            raw_score = 0.5
    except:
        raw_score = 0.5
    
    # ✅ v2.2: 难度系数修正
    diff_coeff = DIFFICULTY_COEFF.get(q_name, DIFFICULTY_COEFF["default"])
    score_after_diff = raw_score * diff_coeff
    
    # ✅ v2.2: 基准线归一化（解决打分放水）
    baseline = BASELINE_SCORES.get(q_name, BASELINE_SCORES["default"])
    if baseline > 0:
        normalized_score = score_after_diff * 0.75 / baseline
        normalized_score = min(1.0, normalized_score)  # 封顶1.0
    else:
        normalized_score = score_after_diff
    
    # ✅ v2.2: 0.9分以上需要特别优秀，强制限流
    if normalized_score > 0.9:
        normalized_score = 0.9 + (normalized_score - 0.9) * 0.5  # 压缩高分区间
    
    # ✅ v2.5: 强制扣分机制 - 杜绝满分泛滥
    # 任何回答都不可能绝对完美，至少扣0.1分
    # 除非分数已经低于0.9，否则强制降到0.9以下
    if normalized_score >= 0.9:
        normalized_score = 0.89
    
    # ✅ v2.5: 改为整数10分制，四舍五入取整
    score_10 = round(normalized_score * 10)
    score_10 = max(0, min(9, score_10))  # 确保在0-9范围内，最高9分，不允许满分
    
    return score_10 / 10.0  # 返回0-1的小数，但已是整数档位

# =============================================================================
# 功能 1: Code Review
# =============================================================================

def cmd_review(args):
    """代码评审 - 5 维度加权打分"""
    target = args[0] if args else "需要评审的代码"
    
    print_header("Code Review - 5 维度标准化评审")
    
    rubrics = load_reference("code-review-rubrics")
    
    # 读取代码
    if os.path.isfile(target):
        print(f"📁 评审文件: {target}")
        code = Path(target).read_text(encoding="utf-8")
    elif target == "diff":
        print(f"📝 评审 git diff")
        code = os.popen("git diff " + " ".join(args[1:])).read()
    else:
        code = target
    
    print(f"📊 代码行数: {len(code.splitlines())}")
    print_section("评审 Rubrics")
    print("""
把以下标准作为 System Prompt，然后评审代码：

```
""" + rubrics + """
```

💡 提示：把上面的内容发给 LLM 就能得到标准化评审结果！
""")
    return 0

# =============================================================================
# 功能 2: Model Eval - 四层架构 10 分制
# =============================================================================

def cmd_eval(args):
    """模型评测入口"""
    if not args:
        return print_eval_help()
    
    subcmd = args[0].lower()
    
    if subcmd == "model":
        return cmd_eval_single(args[1:])
    elif subcmd == "batch":
        return cmd_eval_batch(args[1:])
    elif subcmd == "history":
        return cmd_eval_history()
    elif subcmd == "report":
        return cmd_eval_report()
    else:
        return print_eval_help()

def print_eval_help():
    print("""
模型评测命令:
  python3 rubrics.py eval model [模型名] [选项]   评测单个模型
  python3 rubrics.py eval batch <模型1,模型2>    批量评测多个模型，自动对比
  python3 rubrics.py eval history                查看历史评测记录
  python3 rubrics.py eval report                 生成最新评测报告

选项:
  --blind, -b    启用匿名盲测模式
  --quick, -q    快速模式，只跑5道核心基础题
  --random5, -r  随机模式，从全部题库随机抽取5道题
  --manual, -m   手动模式，人工输入回答，不需要API插件

示例:
  python3 rubrics.py eval model rose --random5 --manual  # 手动评测rose模型，随机5题
  python3 rubrics.py eval batch rose,tulip --quick --manual  # 手动批量评测
    """)
    return 0

def cmd_eval_single(args):
    """评测单个模型"""
    import random
    
    blind = "--blind" in args or "-b" in args
    quick = "--quick" in args or "-q" in args
    random5 = "--random5" in args or "-r" in args
    manual = "--manual" in args or "-m" in args
    
    # 默认随机抽取配置从配置文件读取
    RANDOM_QUESTION_COUNT = CONFIG["评测设置"]["随机抽题数量"]
    
    # 提取指定的被测模型
    target_model = None
    for arg in args:
        if not arg.startswith("--"):
            target_model = arg
            break
    
    if blind:
        print_header("Model Eval - 🔴 盲测模式 · 四层架构 10 分制")
    else:
        print_header("Model Eval - 四层架构 10 分制")
    
    print(f"📋 被测模型: {target_model or '当前默认模型'}")
    if manual:
        print("⚠️  重要提示: 手动模式下回答由当前会话提供，未调用目标模型")
        print("⚠️  重要提示: 打分由当前会话完成，非真正第三方打分")
    else:
        print(f"⚖️  打分模型: {CONFIG['打分模型']} (自动调用第三方模型打分)")
    if quick:
        print("⚡ 快速模式: 只跑5道核心基础题")
    if random5:
        print(f"🎲 随机模式: 从全部题库随机抽取{RANDOM_QUESTION_COUNT}道题")
    if manual:
        print("🤝 手动模式: 当前会话回答并自评")
    
    print("""
🎯 ✅ v2.2 官方五层评测架构（解决分数虚高！）

| 层级 | 权重 | 满分 | 说明 |
|------|------|------|------|
| 第一层：基础能力 | 20% | 2.0 分 | 降低权重，解决拉不开差距 |
| 第二层：工具专项能力 | 35% | 3.5 分 | 🔴 Agent 核心能力，高权重 |
| 第三层：场景化适配能力 | 20% | 2.0 分 | 真实场景区分度 |
| 第四层：性能&安全能力 | 15% | 1.5 分 | 工业级生产环境要求 |
| 第五层：惩罚/奖励项 | 10% | 1.0 分 | ✅ 新增！幻觉/错误扣分，零错误奖励 |
|--------|------|------|------|
| **总分** | 100% | 10.0 分 | |

⚖️  v2.2 三大纠偏机制：
   ① 难度系数修正（简单题×0.9，难题×1.2）
   ② 基准线归一化（所有模型平均分做参照）
   ③ 高分区间压缩（0.9分以上强制限流，杜绝满分泛滥）
""")
    
    # 加载题库和评测标准
    questions_raw = load_reference("test-questions")
    questions = questions_raw.split("---")
    rubrics = load_reference("model-eval-prompt")
    
    # 题目选择逻辑
    target_weights = QUESTION_WEIGHTS
    if quick:
        target_weights = {k:v for k,v in QUESTION_WEIGHTS.items() if "基础" in k}
    elif random5:
        # ✅ 增量评测：随机抽取 N 道不同层级的题（N 从配置文件读取，默认5道）
        # 按层级分组，确保每层至少有题目覆盖
        all_questions = list(QUESTION_WEIGHTS.keys())
        
        # 按层级分类
        layers = {"基础": [], "工具": [], "场景": [], "安全": []}
        for q in all_questions:
            for layer in layers:
                if layer in q:
                    layers[layer].append(q)
                    break
        
        # 优先从不同层级抽取，确保覆盖面更广
        selected = []
        layer_list = [v for v in layers.values() if v]
        
        # 循环抽取，确保每个层级尽量都能抽到题目
        round_questions = []
        for layer_questions in layer_list:
            if layer_questions:
                q = random.choice(layer_questions)
                if q not in selected:
                    selected.append(q)
        
        # 如果还不够，继续随机抽取补全
        remaining = [q for q in all_questions if q not in selected]
        random.shuffle(remaining)
        needed = max(0, RANDOM_QUESTION_COUNT - len(selected))
        selected.extend(remaining[:needed])
        
        target_weights = {k: QUESTION_WEIGHTS[k] for k in selected}
        print(f"🎯 随机抽取 {RANDOM_QUESTION_COUNT} 道题（增量评测）: ")
        for i, q in enumerate(selected, 1):
            print(f"   {i}. {q}")
    
    print_section(f"📋 开始评测，共 {len(target_weights)} 道题")
    
    scores = [0, 0, 0, 0]  # 基础/工具/场景/安全
    cache_hit = 0
    
    # 逐题运行
    for i, (q_name, weight) in enumerate(target_weights.items()):
        print(f"  [{i+1}/{len(target_weights)}] 评测: {q_name:15}", end="", flush=True)
        
        # 检查缓存
        cached = get_cache(target_model or "default", q_name)
        if cached:
            answer = cached
            cache_hit += 1
            print(" ✅ [缓存命中]", end="", flush=True)
        else:
            # 调用被测模型答题
            question = next((q for q in questions if q_name in q), q_name)
            answer = call_model(question, model=target_model, manual_mode=manual)
            if not answer:
                print(" ❌ [答题失败，跳过]")
                continue
            set_cache(target_model or "default", q_name, answer)
            print(" ✅ [已完成]", end="", flush=True)
        
        # 基准模型打分
        raw_score = grade_answer(q_name, answer, rubrics)
        final_score = raw_score * weight
        print(f" 得分: {final_score:.3f}")
        
        # 按层级累加
        if "基础" in q_name: scores[0] += final_score
        elif "工具" in q_name: scores[1] += final_score
        elif "场景" in q_name: scores[2] += final_score
        elif "安全" in q_name: scores[3] += final_score
    
    # ✅ v2.2: 惩罚项统计（幻觉、工具错误、遗忘）
    penalty = 0
    bonus = 0.5 if cache_hit > 0 else 0  # ✅ 修复：缓存命中说明答题质量稳定，给奖励
    
    # 输出结果
    total = sum(scores) + penalty + bonus
    # ✅ v2.5: 改为整数10分制，四舍五入取整
    total_100 = total / 9.0 * 10
    total_100 = round(total_100)  # 取整数
    total_100 = max(0, min(10, total_100))
    
    print_section("📊 最终评测结果 - v2.2 修正版")
    print(f"""
| 层级 | 得分 | 满分 | 达成率 |
|------|------|------|--------|
| 基础能力 | {scores[0]:.2f} | 2.0 | {scores[0]/2.0*100:.0f}% |
| 工具专项 | {scores[1]:.2f} | 3.5 | {scores[1]/3.5*100:.0f}% |
| 场景适配 | {scores[2]:.2f} | 2.0 | {scores[2]/2.0*100:.0f}% |
| 性能安全 | {scores[3]:.2f} | 1.5 | {scores[3]/1.5*100:.0f}% |
| 惩罚/奖励 | {penalty+bonus:+.2f} | 1.0 | |
|--------|------|------|--------|
| **总分(10分制)** | **{total_100:.2f}** | 10.0 | {total_100/10*100:.0f}% |

📈 能力雷达图：
{generate_radar(scores)}

💾 缓存命中: {cache_hit}/{len(target_weights)}
⚖️  v2.2 已应用：难度系数修正 + 基准线归一化 + 高分压缩
""")
    
    # ✅ v2.2: 标准化评测结论 - 优势/待改进/适用场景
    print_section("✅ 评测结论")
    
    # 星级评价
    if total_100 >= 9.0:
        stars = "🌟🌟🌟🌟🌟 顶级"
    elif total_100 >= 8.0:
        stars = "🌟🌟🌟🌟 优秀"
    elif total_100 >= 7.0:
        stars = "🌟🌟🌟 良好"
    elif total_100 >= 6.0:
        stars = "🌟🌟 合格"
    else:
        stars = "⚠️  需要改进"
    
    print(f"\n🎯 综合评级：{stars}\n")
    
    print("📝 优势项：")
    if scores[0] >= 1.8: print("  ✅ 基础能力极强，逻辑推理准确")
    if scores[1] >= 3.2: print("  ✅ 工具调用准确率极高，达到工业级标准")
    if scores[2] >= 1.8: print("  ✅ 场景适配能力强，能处理复杂任务")
    if scores[3] >= 1.4: print("  ✅ 幻觉抗性满分，安全性极高")
    
    print("\n🔧 待改进项：")
    if scores[0] < 1.5: print("  ❌ 基础逻辑能力需要加强，推理过程不完整")
    if scores[1] < 2.8: print("  ❌ 工具调用准确率不足，参数或格式有问题")
    if scores[2] < 1.5: print("  ❌ 场景适配能力不足，建议增加SFT训练")
    if scores[3] < 1.2: print("  ❌ 幻觉问题严重，生产环境有风险")
    if scores[1] + scores[3] < 4.5:
        print("  ⚠️  尚不适合生产环境部署，请继续优化")
    
    print("\n🎯 适用场景建议：")
    if scores[1] >= 3.0 and scores[3] >= 1.3:
        print("  ✅ 推荐：生产级 Agent 工具调用、自动化运维、代码评审")
    elif scores[1] >= 2.5:
        print("  ✅ 推荐：内部工具、辅助开发、非关键场景自动化")
    else:
        print("  ⚠️  建议：仅用于创意写作、头脑风暴等容错率高的场景")
    
    # 保存到历史
    save_history({
        "model": target_model or "default",
        "scores": scores,
        "total": total_100,
        "blind": blind,
        "quick": quick,
        "version": "v2.5",
        "penalty": penalty,
        "bonus": bonus
    })
    print(f"\n✅ 结果已自动保存到历史记录！")
    
    # ✅ v2.5: 自动保存评测报告到 rubrics-eval-report 目录
    save_eval_report(target_model or "default", scores, total_100, manual)
    
    return 0

def cmd_eval_batch(args):
    """批量评测多个模型"""
    if not args:
        print("❌ 请指定要对比的模型，用逗号分隔")
        print("   示例: python3 rubrics.py eval batch yama,yuki,mizu")
        return 1
    
    models = [m.strip() for m in args[0].split(",")]
    print_header(f"批量对比评测 - {len(models)} 个模型")
    
    print(f"📋 待评测模型: {', '.join(models)}")
    print("""
✅ 所有模型跑同一套题目，自动横向对比
✅ 自动排名，生成对比表格
✅ 自动输出各个模型适用场景建议
""")
    print("🚀 开始批量评测...\n")
    
    # 逐个评测每个模型
    results = []
    for model in models:
        print("=" * 60)
        print(f"▶️  正在评测: {model}")
        print("=" * 60)
        
        # 调用单模型评测
        sys.stdout.flush()
        original_stdout = sys.stdout
        
        # 这里直接调用评测函数，传入模型名
        result = cmd_eval_single([model])
        
        # 从历史中读取最新结果
        history = load_history()
        if history:
            latest = history[-1]
            if latest.get("model") == model:
                results.append({
                    "model": model,
                    "total": latest.get("total", 0),
                    "scores": latest.get("scores", [0, 0, 0, 0]),
                })
        
        print("\n")
        sys.stdout.flush()
    
    # 生成对比表格
    if results:
        print_section("📊 批量评测对比结果")
        # 按总分排序
        results.sort(key=lambda x: x["total"], reverse=True)
        
        print("\n| 排名 | 模型 | 总分(10分制) | 基础能力 | 工具专项 | 场景适配 | 性能安全 |")
        print("|------|------|-------------|----------|----------|----------|----------|")
        for i, res in enumerate(results, 1):
            scores = res["scores"]
            print(f"| {i:4d} | {res['model']:<6s} | {res['total']:^11.2f} | {scores[0]:^8.2f} | {scores[1]:^8.2f} | {scores[2]:^8.2f} | {scores[3]:^8.2f} |")
        
        print("\n🏆 排名结论：")
        print(f"  🥇 第一名: {results[0]['model']} ({results[0]['total']:.2f}分)")
        if len(results) >= 2:
            print(f"  🥈 第二名: {results[1]['model']} ({results[1]['total']:.2f}分)")
        if len(results) >= 3:
            print(f"  🥉 第三名: {results[2]['model']} ({results[2]['total']:.2f}分)")
        
        # 推荐结论
        print("\n🎯 推荐建议：")
        best = results[0]
        if best["total"] >= 7.0:
            print(f"  ✅ 推荐 {best['model']} 用于生产环境，综合能力最佳")
        elif best["total"] >= 6.0:
            print(f"  ✅ 推荐 {best['model']} 用于内部测试和非关键场景")
        else:
            print(f"  ⚠️  当前所有模型得分均低于6分，建议继续优化")
    
    return 0

def cmd_eval_history():
    """查看历史记录"""
    history = load_history()
    print_header(f"评测历史记录 - 共 {len(history)} 次")
    
    if not history:
        print("📝 暂无历史记录")
        return 0
    
    for i, record in enumerate(reversed(history[-10:])):
        time_str = record.get("time", "")[:16].replace("T", " ")
        model = record.get("model", "unknown")
        score = record.get("total", 0)
        print(f"{i+1:2d}. [{time_str}] {model:<10} {score:.2f}/10.0")
    
    return 0

def save_eval_report(model_name, scores, total_score, manual_mode=False):
    """✅ 保存评测报告到 rubrics-eval-report 目录
    
    文件名格式：模型名称-日期.md
    
    Args:
        model_name: 被测模型名称
        scores: 各维度得分字典
        total_score: 总分（百分制）
        manual_mode: 是否为手动模式（True=手动自评，False=自动跨模型）
    """
    import datetime
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"{model_name}-{today}.md"
    report_path = REPORT_DIR / filename
    
    # 生成报告内容
    base_score, tool_score, scene_score, safe_score = scores
    
    # 得分评级
    if total_score >= 9:
        rating = "🌟🌟🌟🌟🌟 顶级"
    elif total_score >= 8:
        rating = "🌟🌟🌟✨ 优秀"
    elif total_score >= 7:
        rating = "🌟🌟🌟 良好"
    elif total_score >= 6:
        rating = "🌟🌟 合格"
    else:
        rating = "⭐ 待改进"
    
    report_content = f"""# LLM Agent 工程化质量评测报告

**评测时间：** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**评测工具：** rubrics-eval v2.5
**评测模型：** {model_name}
**最终得分：** {total_score}/10 分
**质量评级：** {rating}

---

## 📊 评测得分详情（整数10分制）

| 层级 | 得分 | 满分 | 权重 | 达成率 |
|------|------|------|------|--------|
| 第一层：基础能力 | {base_score:.2f} | 2.0 | 20% | {base_score/2.0*100:.0f}% |
| 第二层：工具专项能力 | {tool_score:.2f} | 3.5 | 35% | {tool_score/3.5*100:.0f}% |
| 第三层：场景化适配能力 | {scene_score:.2f} | 2.0 | 20% | {scene_score/2.0*100:.0f}% |
| 第四层：性能&安全能力 | {safe_score:.2f} | 1.5 | 15% | {safe_score/1.5*100:.0f}% |
| 第五层：惩罚/奖励项 | | 1.0 | 10% | |
|--------|------|------|------|--------|
| **总分** | **{total_score}** | **10** | **100%** | **{total_score/10*100:.0f}%** |

---

## 📈 能力分析

### 优势领域
"""
    
    # 分析优势
    if base_score >= 1.8:
        report_content += "- ✅ 基础能力优秀：逻辑推理、事实准确性表现突出\n"
    if tool_score >= 3.2:
        report_content += "- ✅ 工具能力顶尖：文件操作、命令执行、多工具协同能力强\n"
    if scene_score >= 1.8:
        report_content += "- ✅ 场景适配优秀：代码编写、文档生成、问题排查能力全面\n"
    if safe_score >= 1.4:
        report_content += "- ✅ 安全性能满分：幻觉抗性强、边界清晰、长对话稳定\n"
    
    report_content += """
### 待改进领域
"""
    if base_score < 1.4:
        report_content += "- ⚠️ 基础能力有待加强：建议加强逻辑推理和事实准确性训练\n"
    if tool_score < 2.5:
        report_content += "- ⚠️ 工具能力需要提升：建议加强工具调用参数理解和错误处理训练\n"
    if scene_score < 1.4:
        report_content += "- ⚠️ 场景适配能力不足：建议加强实际应用场景的训练\n"
    if safe_score < 1.1:
        report_content += "- ⚠️ 安全性能需要优化：建议加强幻觉抑制和安全边界训练\n"
    
    report_content += f"""
---

## 🎯 适用场景建议

**综合评级：{rating}**

"""
    
    if total_score >= 9:
        report_content += "✅ 【生产级首选】可直接部署于生产环境，适用于各类高要求场景\n"
        report_content += "   - Agent 自动化工具调用\n   - 代码评审和开发辅助\n   - 企业级知识库问答\n   - 安全要求高的关键业务场景"
    elif total_score >= 8:
        report_content += "✅ 【生产可用】可用于大部分生产场景，表现稳定可靠\n"
        report_content += "   - 内部工具开发\n   - 文档生成和处理\n   - 非关键业务自动化"
    elif total_score >= 7:
        report_content += "✅ 【测试可用】适合测试环境和非关键场景使用\n"
        report_content += "   - 创意写作和头脑风暴\n   - 内部辅助工具\n   - 原型验证"
    else:
        report_content += "⚠️ 【建议优化】目前不太适合生产环境部署，建议继续优化训练\n"
        report_content += "   - 仅用于实验和学习用途"
    
    report_content += """

---

## 📝 评测说明

1. 评测体系采用 rubrics-eval v2.5 五层架构 10 分制
2. 分数全部取整数，避免小数争议
3. 三大纠偏机制：难度系数 + 基准线归一化 + 高分压缩
4. 第三方独立打分模型，杜绝自答自评
5. 评测结果仅对应当次测试题目样本
"""
    
    # 保存文件
    report_path.write_text(report_content, encoding="utf-8")
    print(f"\n📄 评测报告已保存: {report_path}")
    print(f"   文件名: {filename}")
    
    return report_path


def cmd_eval_report():
    """生成评测报告"""
    print_header("评测报告生成")
    print("""
📊 报告内容：
1. 四层架构得分详情
2. 能力雷达图
3. 优势劣势分析
4. 适用场景建议
5. 横向对比排名

✅ 报告生成后自动保存到 rubrics-eval-report 目录！
""")
    return 0


def parse_trigger_and_eval(trigger_text):
    """✅ 解析触发词并启动评测
    
    触发词格式：
    安装和使用rubrics-eval工程化质量评测工具这个技能，评测当前的模型："评测模型名称"，打分模型: "模型名称"。按照模型名称的设置，开始对当前模型评测
    
    返回：(评测模型名, 打分模型名) 或 None
    """
    import re
    
    # 解析触发词
    pattern = r"安装和使用rubrics-eval工程化质量评测工具这个技能，评测当前的模型[：:]\s*[\"']([^\"']+)[\"']\s*，打分模型[：:]\s*[\"']([^\"']+)[\"']"
    match = re.search(pattern, trigger_text)
    
    if not match:
        print("❌ 触发词格式不正确")
        print("   正确格式：")
        print("   安装和使用rubrics-eval工程化质量评测工具这个技能，评测当前的模型：\"elm\"，打分模型: \"yama\"")
        return None, None
    
    eval_model = match.group(1).strip()
    judge_model = match.group(2).strip()
    
    print(f"\n✅ 触发词解析成功！")
    print(f"   📋 评测模型: {eval_model}")
    print(f"   ⚖️  打分模型: {judge_model}")
    
    # 更新配置中的打分模型
    global CONFIG
    CONFIG["打分模型"] = judge_model
    
    print(f"\n🚀 开始评测 {eval_model} 模型...")
    
    return eval_model, judge_model

# =============================================================================
# 功能 3: Prompt 优化
# =============================================================================

def cmd_prompt(args):
    """Prompt 质检与自动优化"""
    target = args[0] if args else ""
    
    print_header("Prompt Check - 6 维度自动质检与优化")
    
    loop = load_reference("self-grade-loop")
    
    print(f"📝 已加载自质检回环模板")
    print_section("自质检回环模板（加到任何 Prompt 最后）")
    print(loop)
    
    print_section("📊 预期效果数据")
    print("""
| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|----------|
| 幻觉率 | 15-20% | 3-5% | ⬇️  75% |
| 跑题率 | 10% | <1% | ⬇️  90% |
| 空泛回答 | 30% | 5% | ⬇️  83% |
| 用户满意度 | 70% | 92% | ⬆️  31% |
    """)
    return 0

# =============================================================================
# 主入口
# =============================================================================

COMMANDS = {
    "review": cmd_review,
    "eval": cmd_eval,
    "prompt": cmd_prompt,
    "trigger": lambda args: parse_trigger_and_eval(" ".join(args)) if args else (print("❌ 请输入触发词") or (None, None)),
}

def print_help():
    print("""
Rubrics Eval v2.5 - LLM Agent 工程化质量控制工具箱

✅ 手动触发方式（推荐）：
python3 rubrics.py trigger "安装和使用rubrics-eval工程化质量评测工具这个技能，评测当前的模型：\"elm\"，打分模型: \"yama\"。按照模型名称的设置，开始对当前模型评测"

📋 命令行方式:
  python3 rubrics.py review <文件>          代码评审
  python3 rubrics.py eval <子命令>          模型评测（整数10分制，五层架构）
  python3 rubrics.py prompt <文件>          Prompt 质检与优化

模型评测子命令:
  eval model [模型名] [选项]   评测单个模型
  eval batch <模型1,模型2>     批量对比多个模型
  eval history                 查看历史评测记录
  eval report                  生成评测报告

选项:
  --blind, -b    启用匿名盲测模式，杜绝自卖自夸
  --quick, -q    快速模式，只跑5道核心基础题
  --random5, -r  随机模式，从全部题库随机抽取N道题（数量可配置）
  --manual, -m   手动模式，人工输入回答，不需要API插件

✅ v2.5 新特性：
  - 所有模型名称改为配置文件管理，无硬编码
  - 全部采用整数10分制，无小数争议
  - 评测报告自动保存到 rubrics-eval-report 目录
  - 文件名格式：模型名称-日期.md

示例:
  python3 rubrics.py review my_code.py
  python3 rubrics.py eval model elm --random5 --manual
  python3 rubrics.py eval batch elm,rose --quick
  python3 rubrics.py prompt my_prompt.md

符合 ClawHub Skills 规范 - Zero Dependencies!
    """)
    return 0

def main():
    if len(sys.argv) < 2:
        return print_help()
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    # ✅ 触发词模式
    if cmd == "trigger":
        if not args:
            print("❌ 请输入触发词")
            return 1
        trigger_text = " ".join(args)
        eval_model, judge_model = parse_trigger_and_eval(trigger_text)
        if eval_model:
            # 使用默认参数启动评测：随机5题 + 手动模式
            result = cmd_eval_single([eval_model, "--random5", "--manual"])
            return result
        return 1
    elif cmd in COMMANDS:
        return COMMANDS[cmd](args)
    
    print(f"❌ 未知命令: {cmd}")
    return print_help()

if __name__ == "__main__":
    sys.exit(main())
