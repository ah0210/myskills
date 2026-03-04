"""
Playwright 网页抓取 GUI 工具
提供图形界面进行网页抓取操作
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import os
import time
from crawler import WebCrawler


class CrawlerGUI:
    """
    网页抓取 GUI 界面
    """
    
    def __init__(self, root):
        """
        初始化 GUI 界面
        
        Args:
            root: 根窗口
        """
        self.root = root
        self.root.title("Playwright 网页抓取工具")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 抓取线程
        self.crawl_thread = None
        self.is_crawling = False
        
        # 创建主框架
        self.create_main_frame()
        
        # 创建 URL 输入区域
        self.create_url_section()
        
        # 创建分页设置区域
        self.create_pagination_section()
        
        # 创建内容选择区域
        self.create_content_section()
        
        # 创建控制按钮区域
        self.create_control_section()
        
        # 创建日志和结果区域
        self.create_output_section()
    
    def create_main_frame(self):
        """
        创建主框架
        """
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_url_section(self):
        """
        创建 URL 输入区域
        """
        section_frame = ttk.LabelFrame(self.main_frame, text="目标网站", padding="10")
        section_frame.pack(fill=tk.X, pady=5)
        
        # URL 输入
        ttk.Label(section_frame, text="URL:", width=10).grid(row=0, column=0, sticky=tk.W)
        self.url_var = tk.StringVar(value="https://example.com")
        url_entry = ttk.Entry(section_frame, textvariable=self.url_var, width=80)
        url_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 浏览器模式
        ttk.Label(section_frame, text="浏览器模式:", width=10).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.headless_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(section_frame, text="无头模式", variable=self.headless_var).grid(row=1, column=1, sticky=tk.W, padx=5)
    
    def create_pagination_section(self):
        """
        创建分页设置区域
        """
        section_frame = ttk.LabelFrame(self.main_frame, text="分页设置", padding="10")
        section_frame.pack(fill=tk.X, pady=5)
        
        # 启用分页
        self.pagination_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(section_frame, text="启用分页抓取", variable=self.pagination_var, 
                       command=self.toggle_pagination).grid(row=0, column=0, sticky=tk.W, columnspan=3)
        
        # 下一页按钮选择器
        ttk.Label(section_frame, text="下一页选择器:", width=15).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.next_button_var = tk.StringVar(value=".next, .pagination-next, #next")
        next_button_entry = ttk.Entry(section_frame, textvariable=self.next_button_var, width=60)
        next_button_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # 最大页数
        ttk.Label(section_frame, text="最大页数:", width=15).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_pages_var = tk.IntVar(value=5)
        max_pages_spinbox = ttk.Spinbox(section_frame, from_=1, to=100, textvariable=self.max_pages_var, width=10)
        max_pages_spinbox.grid(row=2, column=1, sticky=tk.W, padx=5)
    
    def toggle_pagination(self):
        """
        切换分页设置的启用状态
        """
        pass  # 这里可以添加UI状态更新逻辑
    
    def create_content_section(self):
        """
        创建内容选择区域
        """
        section_frame = ttk.LabelFrame(self.main_frame, text="内容选择", padding="10")
        section_frame.pack(fill=tk.X, pady=5)
        
        # 内容类型选择
        ttk.Label(section_frame, text="内容类型:", width=15).grid(row=0, column=0, sticky=tk.W)
        
        # 内容类型列表
        content_types = ["链接", "标题", "段落", "图片", "自定义"]
        self.content_type_var = tk.StringVar(value="链接")
        content_type_combo = ttk.Combobox(section_frame, textvariable=self.content_type_var, values=content_types, width=15)
        content_type_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # CSS 选择器
        ttk.Label(section_frame, text="CSS 选择器:", width=15).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.selector_var = tk.StringVar(value="a")
        selector_entry = ttk.Entry(section_frame, textvariable=self.selector_var, width=60)
        selector_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # 预设选择器
        preset_frame = ttk.Frame(section_frame)
        preset_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        ttk.Button(preset_frame, text="链接 (a)", command=lambda: self.set_selector("a")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="标题 (h1-h6)", command=lambda: self.set_selector("h1, h2, h3, h4, h5, h6")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="段落 (p)", command=lambda: self.set_selector("p")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="图片 (img)", command=lambda: self.set_selector("img")).pack(side=tk.LEFT, padx=5)
    
    def set_selector(self, selector):
        """
        设置 CSS 选择器
        
        Args:
            selector: CSS 选择器
        """
        self.selector_var.set(selector)
    
    def create_control_section(self):
        """
        创建控制按钮区域
        """
        section_frame = ttk.Frame(self.main_frame)
        section_frame.pack(fill=tk.X, pady=5)
        
        # 开始按钮
        self.start_button = ttk.Button(section_frame, text="开始抓取", command=self.start_crawl)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # 停止按钮
        self.stop_button = ttk.Button(section_frame, text="停止抓取", command=self.stop_crawl, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 保存结果按钮
        self.save_button = ttk.Button(section_frame, text="保存结果", command=self.save_results, state=tk.DISABLED)
        self.save_button.pack(side=tk.RIGHT, padx=5)
    
    def create_output_section(self):
        """
        创建日志和结果区域
        """
        # 日志区域
        log_frame = ttk.LabelFrame(self.main_frame, text="日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=90, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # 结果区域
        result_frame = ttk.LabelFrame(self.main_frame, text="结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=90, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
    
    def log(self, message):
        """
        记录日志
        
        Args:
            message: 日志消息
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_result(self, result):
        """
        更新结果显示
        
        Args:
            result: 抓取结果
        """
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if isinstance(result, list):
            for item in result[:50]:  # 只显示前50个结果
                if isinstance(item, dict):
                    if "text" in item:
                        self.result_text.insert(tk.END, f"{item['text']}\n")
                    if "href" in item and item['href']:
                        self.result_text.insert(tk.END, f"  → {item['href']}\n")
                    self.result_text.insert(tk.END, "\n")
        elif isinstance(result, str):
            self.result_text.insert(tk.END, result)
        
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def start_crawl(self):
        """
        开始抓取
        """
        if self.is_crawling:
            return
        
        # 禁用按钮
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        
        # 清空日志和结果
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        # 启动抓取线程
        self.is_crawling = True
        self.crawl_thread = threading.Thread(target=self.crawl_thread_func)
        self.crawl_thread.daemon = True
        self.crawl_thread.start()
    
    def stop_crawl(self):
        """
        停止抓取
        """
        if not self.is_crawling:
            return
        
        self.is_crawling = False
        self.log("正在停止抓取...")
    
    def crawl_thread_func(self):
        """
        抓取线程函数
        """
        try:
            url = self.url_var.get().strip()
            if not url:
                self.log("错误: 请输入 URL")
                return
            
            headless = self.headless_var.get()
            use_pagination = self.pagination_var.get()
            next_button_selector = self.next_button_var.get().strip()
            max_pages = self.max_pages_var.get()
            content_selector = self.selector_var.get().strip()
            
            self.log(f"开始抓取: {url}")
            self.log(f"浏览器模式: {'无头' if headless else '有头'}")
            
            results = []
            
            with WebCrawler(headless=headless) as crawler:
                if use_pagination and next_button_selector:
                    self.log(f"启用分页抓取，最大页数: {max_pages}")
                    self.log(f"下一页选择器: {next_button_selector}")
                    results = crawler.crawl_pagination(
                        url=url,
                        next_button_selector=next_button_selector,
                        content_selector=content_selector,
                        max_pages=max_pages
                    )
                else:
                    self.log("单页抓取")
                    if crawler.open_url(url, wait_time=5):
                        # 滚动页面以加载更多内容
                        self.log("滚动页面加载更多内容...")
                        for i in range(3):
                            crawler.page.evaluate("window.scrollBy(0, 1000)")
                            time.sleep(2)
                        
                        # 等待内容加载
                        time.sleep(3)
                        
                        # 提取内容
                        results = crawler.extract_elements(content_selector)
                        
                        # 如果是段落，过滤掉太短的
                        if content_selector == "p" and results:
                            results = [r for r in results if len(r['text'].strip()) > 20]
                        
                        # 如果没有找到内容，尝试获取整个页面的文本
                        if not results:
                            self.log("使用选择器未找到内容，尝试获取整个页面文本...")
                            full_text = crawler.get_text_content()
                            if full_text and len(full_text.strip()) > 100:
                                results = [{"text": full_text, "href": "", "src": "", "tag": "body"}]
                                self.log(f"成功获取页面文本，共 {len(full_text)} 字符")
                    else:
                        self.log("无法打开 URL")
            
            if results:
                self.log(f"成功抓取 {len(results)} 个元素")
                self.update_result(results)
                self.save_button.config(state=tk.NORMAL)
            else:
                self.log("未抓取到任何内容")
                self.update_result("未抓取到任何内容")
                
        except Exception as e:
            self.log(f"抓取失败: {str(e)}")
            self.update_result(f"抓取失败: {str(e)}")
        finally:
            self.is_crawling = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def save_results(self):
        """
        保存结果
        """
        try:
            # 获取结果文本
            result_content = self.result_text.get(1.0, tk.END).strip()
            if not result_content:
                messagebox.showinfo("提示", "没有结果可保存")
                return
            
            # 创建输出目录
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            # 生成文件名
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crawl_result_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # 保存结果
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(result_content)
            
            messagebox.showinfo("成功", f"结果已保存到: {filepath}")
            self.log(f"结果已保存到: {filepath}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
            self.log(f"保存失败: {str(e)}")


def main():
    """
    主函数
    """
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
