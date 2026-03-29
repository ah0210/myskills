# 安装指南

## 标准安装方式（通过ClawHub）

### 1. 安装ClawHub CLI（如果未安装）
```bash
npm install -g clawhub
```

### 2. 登录ClawHub
```bash
clawhub login
```

### 3. 安装技能
```bash
clawhub install tech-discussion-manager
```

安装过程会自动完成：
- ✅ 创建标准目录结构
- ✅ 安装模板文件
- ✅ 更新智能体规则系统
- ✅ 集成到记忆系统

## 手动安装方式

### 1. 下载技能
```bash
# 克隆或下载技能到OpenClaw技能目录
git clone <仓库地址> ~/.openclaw/skills/tech-discussion-manager
```

### 2. 执行安装步骤
```bash
# 设置工作空间环境变量
export OPENCLAW_WORKSPACE="/path/to/your/workspace"

# 1. 创建目录结构
mkdir -p $OPENCLAW_WORKSPACE/memory/tech-discussions/archive \
         $OPENCLAW_WORKSPACE/code-output \
         $OPENCLAW_WORKSPACE/docs/decisions \
         $OPENCLAW_WORKSPACE/docs/architecture

# 2. 安装模板文件
cp ~/.openclaw/skills/tech-discussion-manager/templates/*.md $OPENCLAW_WORKSPACE/memory/tech-discussions/

# 3. 更新智能体配置（自动添加规则到AGENTS.md）
grep -q "技术讨论沉淀规则" $OPENCLAW_WORKSPACE/AGENTS.md || echo -e "
### 💬 技术讨论沉淀规则
1. 所有技术讨论必须使用 tech-discussion-manager 技能管理
2. 讨论记录使用标准模板保存到 memory/tech-discussions/ 目录
3. 代码产出必须保存到 code-output/ 对应主题目录
4. 重要决策必须同步到 MEMORY.md 和 docs/decisions/ 目录
5. 讨论结束后必须更新 memory/tech-discussions/index.md 索引" >> $OPENCLAW_WORKSPACE/AGENTS.md
```

## 验证安装

安装完成后，可以通过以下方式验证：

1. 检查目录结构是否创建成功：
```bash
ls $OPENCLAW_WORKSPACE/memory/tech-discussions/
# 应该包含 archive/ 目录、TEMPLATE.md 文件
```

2. 检查AGENTS.md是否已添加规则：
```bash
grep "技术讨论沉淀规则" $OPENCLAW_WORKSPACE/AGENTS.md
# 应该能看到规则内容
```

3. 测试智能体触发：
```
用户：我们讨论一下GEO工具的开发
智能体应该回复：✅ 已为你创建技术讨论记录...
```

## 卸载方式

### 通过ClawHub卸载
```bash
clawhub uninstall tech-discussion-manager
```

### 手动卸载
1. 删除技能目录：
```bash
rm -rf ~/.openclaw/skills/tech-discussion-manager
```

2. （可选）删除AGENTS.md中的规则：
编辑`$OPENCLAW_WORKSPACE/AGENTS.md`，删除"技术讨论沉淀规则"章节。

3. （可选）删除讨论数据：
```bash
# 注意：这会删除所有历史讨论记录，请谨慎操作
# rm -rf $OPENCLAW_WORKSPACE/memory/tech-discussions/
```

## 升级方式

### 通过ClawHub升级
```bash
clawhub update tech-discussion-manager
```

### 手动升级
1. 下载最新版本的技能文件，覆盖`~/.openclaw/skills/tech-discussion-manager/`目录
2. 重新执行安装步骤中的模板安装和配置更新步骤

## 多工作空间支持
如果有多个工作空间，需要在每个工作空间执行安装步骤：
```bash
# 切换到工作空间1
export OPENCLAW_WORKSPACE="/workspace1"
# 执行安装步骤...

# 切换到工作空间2
export OPENCLAW_WORKSPACE="/workspace2"
# 执行安装步骤...
```

每个工作空间的讨论数据相互独立，互不影响。
