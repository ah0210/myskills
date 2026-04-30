import { Editor, MarkdownView, Notice } from "obsidian";
import { AIService, ChatMessage } from "./ai-service";
import { PluginSettings, PromptItem } from "./settings";

export class Optimizer {
  private isOptimizing = false;
  private aiService: AIService;

  constructor(
    private settings: PluginSettings,
    aiService: AIService
  ) {
    this.aiService = aiService;
  }

  updateSettings(settings: PluginSettings): void {
    this.settings = settings;
    this.aiService.updateSettings(settings);
  }

  get optimizing(): boolean {
    return this.isOptimizing;
  }

  /**
   * 获取默认提示词
   */
  private getDefaultPrompt(): PromptItem | undefined {
    return this.settings.prompts.find(
      (p) => p.id === this.settings.defaultPromptId
    );
  }

  /**
   * 根据 ID 获取提示词
   */
  getPromptById(id: string): PromptItem | undefined {
    return this.settings.prompts.find((p) => p.id === id);
  }

  /**
   * 执行优化（核心入口）
   */
  async optimize(
    editor: Editor,
    view: MarkdownView,
    promptId?: string
  ): Promise<void> {
    if (this.isOptimizing) {
      new Notice("正在优化中，请稍候...");
      return;
    }

    // 1. 确定提示词
    const prompt = promptId
      ? this.getPromptById(promptId)
      : this.getDefaultPrompt();
    if (!prompt) {
      new Notice("未找到提示词，请先在设置中配置");
      return;
    }

    // 2. 确定优化范围（选中 or 全文）
    const selectedText = editor.getSelection();
    const isSelection = selectedText.length > 0;
    const content = isSelection ? selectedText : editor.getValue();

    if (!content.trim()) {
      new Notice("文章内容为空，无需优化");
      return;
    }

    // 3. 备份原文到剪贴板
    if (this.settings.autoBackup) {
      try {
        await navigator.clipboard.writeText(content);
      } catch {
        // 剪贴板写入失败不阻塞流程
      }
    }

    // 4. 加锁
    this.isOptimizing = true;
    const statusBar = (view.app.workspace as any).plugin?.statusBarItem;
    const statusText = "🔄 AI 优化中...";
    new Notice(statusText);

    // 5. 构建消息
    const messages: ChatMessage[] = [
      { role: "system", content: prompt.content },
      { role: "user", content },
    ];

    // 6. 调用 AI（流式）
    try {
      if (isSelection) {
        await this.optimizeSelection(editor, messages);
      } else {
        await this.optimizeFullDoc(editor, messages);
      }
    } catch (err) {
      // 错误已在 AIService 中 Notice
    } finally {
      this.isOptimizing = false;
    }
  }

  /**
   * 优化选中文本（流式替换）
   */
  private async optimizeSelection(
    editor: Editor,
    messages: ChatMessage[]
  ): Promise<void> {
    const from = editor.getCursor("from");
    const to = editor.getCursor("to");
    const originalText = editor.getSelection();
    let lastText = "";

    // 先清空选区
    editor.replaceSelection("");

    await this.aiService.chatStream(messages, {
      onChunk: (fullText) => {
        // 增量更新：只追加新增部分
        const delta = fullText.slice(lastText.length);
        lastText = fullText;
        editor.replaceRange(delta, editor.getCursor("from"));
      },
      onDone: (fullText) => {
        // 最终确认
        if (this.settings.showDiffSummary) {
          this.showDiffSummary(originalText, fullText);
        }
        new Notice("✅ 优化完成");
      },
      onError: (err) => {
        // 恢复原文
        const currentFrom = editor.getCursor("from");
        const currentTo = {
          line: currentFrom.line,
          ch: currentFrom.ch + lastText.length,
        };
        editor.replaceRange(originalText, currentFrom, currentTo);
        new Notice("❌ 优化失败，已恢复原文");
      },
    });
  }

  /**
   * 优化全文（流式替换）
   */
  private async optimizeFullDoc(
    editor: Editor,
    messages: ChatMessage[]
  ): Promise<void> {
    const originalText = editor.getValue();
    let lastText = "";

    // 清空编辑器
    editor.setValue("");

    await this.aiService.chatStream(messages, {
      onChunk: (fullText) => {
        const delta = fullText.slice(lastText.length);
        lastText = fullText;
        // 追加到编辑器末尾
        const lastLine = editor.lastLine();
        const lastCh = editor.getLine(lastLine).length;
        editor.replaceRange(delta, { line: lastLine, ch: lastCh });
      },
      onDone: (fullText) => {
        if (this.settings.showDiffSummary) {
          this.showDiffSummary(originalText, fullText);
        }
        new Notice("✅ 优化完成");
      },
      onError: (err) => {
        editor.setValue(originalText);
        new Notice("❌ 优化失败，已恢复原文");
      },
    });
  }

  /**
   * 显示差异摘要
   */
  private showDiffSummary(original: string, optimized: string): void {
    const origLines = original.split("\n").length;
    const optLines = optimized.split("\n").length;
    const origChars = original.length;
    const optChars = optimized.length;
    const charDiff = optChars - origChars;
    const lineDiff = optLines - origLines;

    const summary = [
      `📊 优化摘要`,
      `原文: ${origChars} 字 / ${origLines} 行`,
      `优化后: ${optChars} 字 / ${optLines} 行`,
      `变化: ${charDiff >= 0 ? "+" : ""}${charDiff} 字 / ${lineDiff >= 0 ? "+" : ""}${lineDiff} 行`,
    ].join("\n");

    new Notice(summary, 5000);
  }
}
