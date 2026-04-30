import { Notice, requestUrl, RequestUrlParam } from "obsidian";
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

  /**
   * 非流式请求
   */
  async chat(messages: ChatMessage[]): Promise<string> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.settings.apiKey) {
      headers["Authorization"] = `Bearer ${this.settings.apiKey}`;
    }

    const body = {
      model: this.settings.modelName,
      messages,
      stream: false,
    };

    try {
      const response = await requestUrl({
        url: this.settings.apiEndpoint,
        method: "POST",
        headers,
        body: JSON.stringify(body),
      });

      const data = response.json;
      if (data?.choices?.[0]?.message?.content) {
        return data.choices[0].message.content;
      }
      throw new Error("API 返回格式异常: " + JSON.stringify(data));
    } catch (err: any) {
      const msg = err?.message || String(err);
      new Notice("AI 请求失败: " + msg, 5000);
      throw err;
    }
  }

  /**
   * 流式请求（SSE）
   */
  async chatStream(
    messages: ChatMessage[],
    callbacks: StreamCallbacks
  ): Promise<void> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };
    if (this.settings.apiKey) {
      headers["Authorization"] = `Bearer ${this.settings.apiKey}`;
    }

    const body = {
      model: this.settings.modelName,
      messages,
      stream: true,
    };

    let fullText = "";

    try {
      const response = await fetch(this.settings.apiEndpoint, {
        method: "POST",
        headers,
        body: JSON.stringify(body),
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

      // 流结束但没收到 [DONE]
      callbacks.onDone(fullText);
    } catch (err: any) {
      const msg = err?.message || String(err);
      callbacks.onError(err);
      new Notice("AI 流式请求失败: " + msg, 5000);
    }
  }
}
