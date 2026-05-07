import { Editor, MarkdownView, Notice } from "obsidian";
import { PluginSettings } from "./settings";
import { AIService, ChatMessage } from "./ai-service";

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

  /**
   * 执行优化（核心入口）
   */
  async optimize(editor: Editor, view: MarkdownView): Promise<void> {
    if (this.isOptimizing) {
      new Notice("正在优化中，请稍候...");
      return;
    }

    const prompt = this.settings.optimizePrompt?.trim();
    if (!prompt) {
      new Notice("请先在设置中填写优化提示词");
      return;
    }

    const selectedText = editor.getSelection();
    const isSelection = selectedText.length > 0;
    const content = isSelection ? selectedText : editor.getValue();

    if (!content.trim()) {
      new Notice("没有可优化的内容");
      return;
    }

    if (this.settings.autoBackup) {
      await navigator.clipboard.writeText(content);
      new Notice("原文已备份到剪贴板");
    }

    this.isOptimizing = true;
    const statusBar = (view.app as any).statusBar;
    const originalStatus = statusBar?.containerEl?.querySelector(".status-bar-item")?.textContent;

    try {
      await this.runOptimization(editor, content, isSelection, prompt);
    } catch (err: any) {
      new Notice("优化失败: " + (err?.message || String(err)), 5000);
    } finally {
      this.isOptimizing = false;
    }
  }

  private async runOptimization(
    editor: Editor,
    originalContent: string,
    isSelection: boolean,
    prompt: string
  ): Promise<void> {
    const messages: ChatMessage[] = [
      {
        role: "system",
        content: prompt,
      },
      {
        role: "user",
        content: originalContent,
      },
    ];

    let lastText = "";

    await this.aiService.chatStream(messages, {
      onChunk: (text: string) => {
        lastText = text;
        if (isSelection) {
          const from = editor.getCursor("from");
          editor.replaceSelection(text);
        } else {
          editor.setValue(text);
        }
      },
      onDone: (fullText: string) => {
        if (this.settings.showDiffSummary) {
          this.showDiffSummary(originalContent, fullText);
        }
      },
      onError: (err: Error) => {
        if (isSelection) {
          const from = editor.getCursor("from");
          if (lastText) {
            const to = {
              line: from.line,
              ch: from.ch + lastText.length,
            };
            editor.replaceRange(originalContent, from, to);
          } else {
            editor.replaceSelection(originalContent);
          }
        } else {
          editor.setValue(originalContent);
        }
        new Notice("优化失败: " + err.message, 5000);
      },
    });
  }

  private showDiffSummary(original: string, optimized: string): void {
    const origChars = original.length;
    const optChars = optimized.length;
    const origLines = original.split("\n").length;
    const optLines = optimized.split("\n").length;
    const charDiff = optChars - origChars;
    const lineDiff = optLines - origLines;
    const charSign = charDiff >= 0 ? "+" : "";
    const lineSign = lineDiff >= 0 ? "+" : "";

    const summary = `📊 优化完成 | 字数: ${origChars}→${optChars} (${charSign}${charDiff}) | 行数: ${origLines}→${optLines} (${lineSign}${lineDiff})`;
    new Notice(summary, 5000);
  }
}
