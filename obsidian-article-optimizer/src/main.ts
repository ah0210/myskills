import { Plugin, MarkdownView, Notice, Editor } from "obsidian";
import {
  DEFAULT_SETTINGS,
  PluginSettings,
  OptimizerSettingTab,
  PromptItem,
} from "./settings";
import { AIService } from "./ai-service";
import { Optimizer } from "./optimizer";

export default class ArticleOptimizerPlugin extends Plugin {
  settings!: PluginSettings;
  aiService!: AIService;
  optimizer!: Optimizer;
  statusBarItem!: HTMLElement;

  async onload(): Promise<void> {
    await this.loadSettings();

    // 初始化服务
    this.aiService = new AIService(this.settings);
    this.optimizer = new Optimizer(this.settings, this.aiService);

    // 状态栏
    this.statusBarItem = this.addStatusBarItem();
    this.statusBarItem.setText("🦐 AI优化");

    // 命令：优化文章（使用默认提示词）
    this.addCommand({
      id: "optimize-article",
      name: "优化文章（默认提示词）",
      editorCallback: (editor: Editor, view: MarkdownView) => {
        this.optimizer.optimize(editor, view);
      },
    });

    // 命令：选择提示词优化
    this.addCommand({
      id: "optimize-with-prompt",
      name: "优化文章（选择提示词）",
      editorCallback: (editor: Editor, view: MarkdownView) => {
        this.showPromptSelector(editor, view);
      },
    });

    // 为每个提示词注册独立命令
    this.registerPromptCommands();

    // 快捷键
    this.addCommand({
      id: "optimize-shortcut",
      name: "优化文章（快捷键）",
      editorCallback: (editor: Editor, view: MarkdownView) => {
        this.optimizer.optimize(editor, view);
      },
    });

    // 设置面板
    this.addSettingTab(new OptimizerSettingTab(this.app, this));
  }

  onunload(): void {
    // 清理
  }

  async loadSettings(): Promise<void> {
    const loaded = await this.loadData();
    this.settings = Object.assign({}, DEFAULT_SETTINGS, loaded);

    // 确保 prompts 数组存在且有内容
    if (!this.settings.prompts || this.settings.prompts.length === 0) {
      this.settings.prompts = DEFAULT_SETTINGS.prompts;
    }
  }

  async saveSettings(): Promise<void> {
    await this.saveData(this.settings);
    this.optimizer.updateSettings(this.settings);
    this.registerPromptCommands();
  }

  /**
   * 为每个提示词注册独立命令（命令面板可选）
   */
  private registeredPromptCommandIds: string[] = [];

  private registerPromptCommands(): void {
    // 移除旧命令
    for (const id of this.registeredPromptCommandIds) {
      (this.app as any).commands?.removeCommand?.(
        `${this.manifest.id}:${id}`
      );
    }
    this.registeredPromptCommandIds = [];

    // 注册新命令
    for (const prompt of this.settings.prompts) {
      const commandId = `optimize-prompt-${prompt.id}`;
      this.addCommand({
        id: commandId,
        name: `优化: ${prompt.name}`,
        editorCallback: (editor: Editor, view: MarkdownView) => {
          this.optimizer.optimize(editor, view, prompt.id);
        },
      });
      this.registeredPromptCommandIds.push(commandId);
    }
  }

  /**
   * 显示提示词选择器（命令面板风格）
   */
  private showPromptSelector(
    editor: Editor,
    view: MarkdownView
  ): void {
    const prompts = this.settings.prompts;
    if (prompts.length === 0) {
      new Notice("没有可用的提示词");
      return;
    }

    // 使用 Obsidian 的 FuzzySuggestModal
    const modal = new PromptSuggestModal(this, prompts, (prompt) => {
      this.optimizer.optimize(editor, view, prompt.id);
    });
    modal.open();
  }
}

import { FuzzySuggestModal } from "obsidian";

class PromptSuggestModal extends FuzzySuggestModal<PromptItem> {
  private prompts: PromptItem[];
  private onSelect: (prompt: PromptItem) => void;

  constructor(
    plugin: ArticleOptimizerPlugin,
    prompts: PromptItem[],
    onSelect: (prompt: PromptItem) => void
  ) {
    super(plugin.app);
    this.prompts = prompts;
    this.onSelect = onSelect;
    this.setPlaceholder("选择提示词...");
  }

  getItems(): PromptItem[] {
    return this.prompts;
  }

  getItemText(item: PromptItem): string {
    return item.name;
  }

  onChooseItem(item: PromptItem): void {
    this.onSelect(item);
  }
}
