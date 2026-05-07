import { Plugin, MarkdownView, Notice, Editor } from "obsidian";
import { DEFAULT_SETTINGS, PluginSettings, OptimizerSettingTab } from "./settings";
import { AIService } from "./ai-service";
import { Optimizer } from "./optimizer";

export default class ArticleOptimizerPlugin extends Plugin {
  settings!: PluginSettings;
  aiService!: AIService;
  optimizer!: Optimizer;
  statusBarItem!: HTMLElement;

  async onload(): Promise<void> {
    await this.loadSettings();

    this.aiService = new AIService(this.settings);
    this.optimizer = new Optimizer(this.settings, this.aiService);

    this.statusBarItem = this.addStatusBarItem();
    this.statusBarItem.setText("🦐 AI优化");

    this.addCommand({
      id: "optimize-article",
      name: "优化文章",
      editorCallback: (editor: Editor, view: MarkdownView) => {
        this.optimizer.optimize(editor, view);
      },
    });

    this.addSettingTab(new OptimizerSettingTab(this.app, this));
  }

  onunload(): void {}

  async loadSettings(): Promise<void> {
    const loaded = await this.loadData();
    this.settings = Object.assign({}, DEFAULT_SETTINGS, loaded);
  }

  async saveSettings(): Promise<void> {
    await this.saveData(this.settings);
    this.optimizer.updateSettings(this.settings);
  }
}
