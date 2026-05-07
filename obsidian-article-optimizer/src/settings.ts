import { App, PluginSettingTab, Setting, Notice } from "obsidian";
import ArticleOptimizerPlugin from "./main";
import { AIService } from "./ai-service";

export interface PluginSettings {
  apiEndpoint: string;
  apiKey: string;
  modelName: string;
  optimizePrompt: string;
  autoBackup: boolean;
  showDiffSummary: boolean;
  requestTimeout: number;
  maxRetries: number;
}

export const DEFAULT_SETTINGS: PluginSettings = {
  apiEndpoint: "http://localhost:11434/v1/chat/completions",
  apiKey: "",
  modelName: "llama3",
  optimizePrompt:
    "你是一位专业的文章编辑。请优化以下文章的排版与格式，遵守以下规则：\n1. 禁止使用 H1（# 一级标题），最大标题层级为 H2（## 二级标题），层级分明；\n2. 文章最前面保留或补充一段引言/说明文字，然后再进入标题结构；\n3. 标题使用平行并列的形式（如：## 背景、## 方案、## 总结），不要使用「一、二、三」或「第一步、第二步」等步骤式编号；\n4. 优化完成后直接输出优化后的文章内容，不要在结尾添加任何说明性文字（如「以上为格式优化结果」等）；\n5. 只优化格式和结构，不改变原文的核心内容和意思，不大幅改写。",
  autoBackup: true,
  showDiffSummary: true,
  requestTimeout: 60000,
  maxRetries: 2,
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

    new Setting(containerEl)
      .setName("测试连接")
      .setDesc("发送一条简单请求验证 AI 服务是否可用")
      .addButton((btn) =>
        btn
          .setButtonText("测试连接")
          .setClass("mod-cta")
          .onClick(async () => {
            btn.setButtonText("测试中...");
            btn.setDisabled(true);
            try {
              const testService = new AIService(this.plugin.settings);
              await testService.testConnection();
              new Notice("✅ 连接成功！AI 服务可用");
            } catch (err: any) {
              new Notice("❌ 连接失败: " + (err?.message || String(err)), 8000);
            } finally {
              btn.setButtonText("测试连接");
              btn.setDisabled(false);
            }
          })
      );

    containerEl.createEl("h2", { text: "优化提示词" });

    const promptDesc = containerEl.createDiv({
      cls: "optimizer-prompt-desc",
    });
    promptDesc.createEl("p", {
      text: "AI 将严格按照以下提示词要求优化你的文章。你可以自定义提示词来控制优化行为。",
    });

    const promptContainer = containerEl.createDiv({
      cls: "optimizer-prompt-container",
    });

    const textarea = promptContainer.createEl("textarea", {
      cls: "optimizer-prompt-textarea",
    });
    textarea.value = this.plugin.settings.optimizePrompt;
    textarea.rows = 8;
    textarea.onchange = async () => {
      this.plugin.settings.optimizePrompt = textarea.value;
      await this.plugin.saveSettings();
    };

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
      .setDesc("优化后显示字数/行数变化统计")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.showDiffSummary)
          .onChange(async (value) => {
            this.plugin.settings.showDiffSummary = value;
            await this.plugin.saveSettings();
          })
      );

    containerEl.createEl("h2", { text: "高级设置" });

    new Setting(containerEl)
      .setName("请求超时（毫秒）")
      .setDesc("AI 请求的最大等待时间，默认 60000ms（60秒）")
      .addText((text) =>
        text
          .setPlaceholder("60000")
          .setValue(String(this.plugin.settings.requestTimeout))
          .onChange(async (value) => {
            const num = parseInt(value, 10);
            if (!isNaN(num) && num >= 5000) {
              this.plugin.settings.requestTimeout = num;
              await this.plugin.saveSettings();
            }
          })
      );

    new Setting(containerEl)
      .setName("最大重试次数")
      .setDesc("请求失败后的重试次数，默认 2 次")
      .addText((text) =>
        text
          .setPlaceholder("2")
          .setValue(String(this.plugin.settings.maxRetries))
          .onChange(async (value) => {
            const num = parseInt(value, 10);
            if (!isNaN(num) && num >= 0 && num <= 5) {
              this.plugin.settings.maxRetries = num;
              await this.plugin.saveSettings();
            }
          })
      );
  }
}
