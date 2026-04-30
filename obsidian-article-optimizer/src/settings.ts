import { App, PluginSettingTab, Setting } from "obsidian";
import ArticleOptimizerPlugin from "./main";

export interface PromptItem {
  id: string;
  name: string;
  content: string;
  isDefault: boolean;
  createdAt: number;
}

export interface PluginSettings {
  // AI 配置
  apiEndpoint: string;
  apiKey: string;
  modelName: string;

  // 提示词库
  prompts: PromptItem[];
  defaultPromptId: string;

  // 编辑器行为
  autoBackup: boolean;
  showDiffSummary: boolean;

  // 快捷键
  optimizeShortcut: string;
}

export const DEFAULT_PROMPTS: PromptItem[] = [
  {
    id: "preset-format",
    name: "格式优化",
    content:
      "你是一位专业的文章编辑。请优化以下文章的排版与格式，遵守以下规则：\n1. 禁止使用 H1（# 一级标题），最大标题层级为 H2（## 二级标题），层级分明；\n2. 文章最前面保留或补充一段引言/说明文字，然后再进入标题结构；\n3. 标题使用平行并列的形式（如：## 背景、## 方案、## 总结），不要使用「一、二、三」或「第一步、第二步」等步骤式编号；\n4. 优化完成后直接输出优化后的文章内容，不要在结尾添加任何说明性文字（如「以上为格式优化结果」等）；\n5. 只优化格式和结构，不改变原文的核心内容和意思，不大幅改写。",
    isDefault: true,
    createdAt: Date.now(),
  },
  {
    id: "preset-seo",
    name: "SEO 优化",
    content:
      "你是一位SEO专家。请优化以下文章的搜索引擎可见性，包括：优化标题使其更吸引点击、调整关键词密度和分布、添加适当的H标签结构、优化首段和末段。要求：只做SEO相关的优化，保持原文核心内容不变，不大幅改写。",
    isDefault: false,
    createdAt: Date.now(),
  },
  {
    id: "preset-geo",
    name: "GEO 优化",
    content:
      "你是一位GEO（Generative Engine Optimization）专家。请优化以下文章，使其更容易被AI搜索引擎引用和推荐，包括：增加结构化数据描述、优化内容使其更易被AI理解和引用、确保关键信息清晰明确。要求：只做GEO相关的优化，保持原文核心内容不变，不大幅改写。",
    isDefault: false,
    createdAt: Date.now(),
  },
  {
    id: "preset-polish",
    name: "润色精简",
    content:
      "你是一位资深的文字编辑。请对以下文章进行润色和精简：去除冗余表述、修正语法错误、优化句子结构、使表达更加精炼准确。要求：保持原文核心意思和风格不变，只做润色精简，不改变内容方向。",
    isDefault: false,
    createdAt: Date.now(),
  },
  {
    id: "preset-structure",
    name: "结构优化",
    content:
      "你是一位文章结构优化专家。请优化以下文章的结构，遵守以下规则：\n1. 禁止使用 H1（# 一级标题），最大标题层级为 H2（## 二级标题）；\n2. 文章最前面保留或补充一段引言/说明文字，然后再进入标题结构；\n3. 标题使用平行并列的形式，不要使用「一、二、三」或步骤式编号；\n4. 优化完成后直接输出优化后的文章内容，不要在结尾添加任何说明性文字；\n5. 只调整文章结构和段落逻辑，不改变各部分的核心内容，保持原文意思不变。",
    isDefault: false,
    createdAt: Date.now(),
  },
];

export const DEFAULT_SETTINGS: PluginSettings = {
  apiEndpoint: "http://localhost:11434/v1/chat/completions",
  apiKey: "",
  modelName: "llama3",

  prompts: DEFAULT_PROMPTS,
  defaultPromptId: "preset-format",

  autoBackup: true,
  showDiffSummary: true,

  optimizeShortcut: "ctrl+shift+o",
};

export class OptimizerSettingTab extends PluginSettingTab {
  plugin: ArticleOptimizerPlugin;

  constructor(app: App, plugin: ArticleOptimizerPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    // === AI 配置 ===
    containerEl.createEl("h2", { text: "AI 配置" });

    new Setting(containerEl)
      .setName("API 地址")
      .setDesc("OpenAI 兼容的 Chat Completions 接口地址")
      .addText((text) =>
        text
          .setPlaceholder("http://localhost:11434/v1/chat/completions")
          .setValue(this.plugin.settings.apiEndpoint)
          .onChange(async (value) => {
            this.plugin.settings.apiEndpoint = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("API Key")
      .setDesc("留空则不发送（Ollama 本地无需填写）")
      .addText((text) =>
        text
          .setPlaceholder("sk-...")
          .setValue(this.plugin.settings.apiKey)
          .onChange(async (value) => {
            this.plugin.settings.apiKey = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("模型名称")
      .setDesc("如 llama3、qwen2、gpt-4 等")
      .addText((text) =>
        text
          .setPlaceholder("llama3")
          .setValue(this.plugin.settings.modelName)
          .onChange(async (value) => {
            this.plugin.settings.modelName = value;
            await this.plugin.saveSettings();
          })
      );

    // === 编辑器行为 ===
    containerEl.createEl("h2", { text: "编辑器行为" });

    new Setting(containerEl)
      .setName("自动备份原文")
      .setDesc("优化前自动将原文复制到剪贴板")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.autoBackup)
          .onChange(async (value) => {
            this.plugin.settings.autoBackup = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("显示差异摘要")
      .setDesc("优化后显示变化统计")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.showDiffSummary)
          .onChange(async (value) => {
            this.plugin.settings.showDiffSummary = value;
            await this.plugin.saveSettings();
          })
      );

    // === 提示词库 ===
    containerEl.createEl("h2", { text: "提示词库" });

    this.renderPromptList(containerEl);
  }

  private renderPromptList(containerEl: HTMLElement): void {
    const listEl = containerEl.createDiv({ cls: "optimizer-prompt-list" });
    listEl.empty();

    for (const prompt of this.plugin.settings.prompts) {
      const itemEl = listEl.createDiv({ cls: "optimizer-prompt-item" });

      const headerEl = itemEl.createDiv({
        cls: "optimizer-prompt-header",
      });

      headerEl.createSpan({
        cls: "optimizer-prompt-name",
        text: prompt.name + (prompt.isDefault ? " ⭐默认" : ""),
      });

      const btnGroup = headerEl.createDiv({ cls: "optimizer-prompt-btns" });

      // 设为默认
      if (!prompt.isDefault) {
        btnGroup.createEl("button", {
          text: "设为默认",
          cls: "mod-cta optimizer-btn-sm",
        }).onclick = async () => {
          this.plugin.settings.prompts.forEach((p) => (p.isDefault = false));
          prompt.isDefault = true;
          this.plugin.settings.defaultPromptId = prompt.id;
          await this.plugin.saveSettings();
          this.renderPromptList(containerEl);
        };
      }

      // 删除
      if (!prompt.id.startsWith("preset-")) {
        btnGroup.createEl("button", {
          text: "删除",
          cls: "mod-warning optimizer-btn-sm",
        }).onclick = async () => {
          this.plugin.settings.prompts = this.plugin.settings.prompts.filter(
            (p) => p.id !== prompt.id
          );
          if (this.plugin.settings.defaultPromptId === prompt.id) {
            this.plugin.settings.defaultPromptId =
              this.plugin.settings.prompts[0]?.id || "";
            if (this.plugin.settings.prompts[0]) {
              this.plugin.settings.prompts[0].isDefault = true;
            }
          }
          await this.plugin.saveSettings();
          this.renderPromptList(containerEl);
        };
      }

      // 提示词内容
      const contentEl = itemEl.createDiv({ cls: "optimizer-prompt-content" });
      const textarea = contentEl.createEl("textarea", {
        cls: "optimizer-prompt-textarea",
      });
      textarea.value = prompt.content;
      textarea.rows = 3;
      textarea.onchange = async () => {
        prompt.content = textarea.value;
        await this.plugin.saveSettings();
      };
    }

    // 添加新提示词
    new Setting(listEl)
      .setName("添加新提示词")
      .setDesc("输入提示词名称后点击添加")
      .addText((text) => {
        text.setPlaceholder("提示词名称");
        text.inputEl.className = "optimizer-new-prompt-name";
      })
      .addButton((btn) =>
        btn
          .setButtonText("添加")
          .setClass("mod-cta")
          .onClick(async () => {
            const nameInput = listEl.querySelector(
              ".optimizer-new-prompt-name"
            ) as HTMLInputElement;
            const name = nameInput?.value?.trim();
            if (!name) return;

            const newPrompt: PromptItem = {
              id: "custom-" + Date.now(),
              name,
              content: "",
              isDefault: false,
              createdAt: Date.now(),
            };
            this.plugin.settings.prompts.push(newPrompt);
            await this.plugin.saveSettings();
            this.renderPromptList(containerEl);
          })
      );
  }
}
