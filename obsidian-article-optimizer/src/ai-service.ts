import { Notice, requestUrl, Platform } from "obsidian";
import { PluginSettings } from "./settings";

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface StreamCallbacks {
  onChunk: (text: string) => void;
  onDone: (fullText: string) => void;
  onError: (error: Error) => void;
}

export class AIService {
  constructor(private settings: PluginSettings) {}

  updateSettings(settings: PluginSettings): void {
    this.settings = settings;
  }

  private buildHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.settings.apiKey) {
      headers["Authorization"] = `Bearer ${this.settings.apiKey}`;
    }
    return headers;
  }

  private buildBody(messages: ChatMessage[], stream: boolean): string {
    return JSON.stringify({
      model: this.settings.modelName,
      messages,
      stream,
    });
  }

  /**
   * 测试 AI 服务连接
   */
  async testConnection(): Promise<void> {
    const headers = this.buildHeaders();
    const body = this.buildBody(
      [{ role: "user", content: "ping" }],
      false
    );

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    try {
      const response = await fetch(this.settings.apiEndpoint, {
        method: "POST",
        headers,
        body,
        signal: controller.signal,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      if (!data?.choices?.[0]?.message?.content) {
        throw new Error("API 返回格式异常");
      }
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * 流式请求（SSE），支持超时和重试
   */
  async chatStream(
    messages: ChatMessage[],
    callbacks: StreamCallbacks
  ): Promise<void> {
    let lastError: Error | null = null;
    const maxRetries = this.settings.maxRetries;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      if (attempt > 0) {
        await this.delay(1000 * attempt);
      }

      try {
        await this.doChatStream(messages, callbacks);
        return;
      } catch (err: any) {
        lastError = err;
        if (attempt < maxRetries) {
          new Notice(`AI 请求失败，正在重试 (${attempt + 1}/${maxRetries})...`);
        }
      }
    }

    callbacks.onError(lastError || new Error("未知错误"));
    new Notice("AI 流式请求失败: " + (lastError?.message || "未知错误"), 5000);
  }

  private async doChatStream(
    messages: ChatMessage[],
    callbacks: StreamCallbacks
  ): Promise<void> {
    const headers: Record<string, string> = {
      ...this.buildHeaders(),
      Accept: "text/event-stream",
    };
    const body = this.buildBody(messages, true);

    const controller = new AbortController();
    const timeoutId = setTimeout(
      () => controller.abort(),
      this.settings.requestTimeout
    );

    let fullText = "";

    try {
      const response = await fetch(this.settings.apiEndpoint, {
        method: "POST",
        headers,
        body,
        signal: controller.signal,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("无法获取响应流");
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith("data: ")) continue;

          const data = trimmed.slice(6);
          if (data === "[DONE]") {
            callbacks.onDone(fullText);
            return;
          }

          try {
            const parsed = JSON.parse(data);
            const delta = parsed?.choices?.[0]?.delta?.content;
            if (delta) {
              fullText += delta;
              callbacks.onChunk(fullText);
            }
          } catch {
            // 跳过解析失败的行
          }
        }
      }

      callbacks.onDone(fullText);
    } catch (err: any) {
      if (err?.name === "AbortError") {
        throw new Error(`请求超时（${this.settings.requestTimeout / 1000}秒）`);
      }
      throw err;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
