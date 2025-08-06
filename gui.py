# 用户界面实现，包含输入框、按钮和图像显示
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import io
import logging
import os
from utils import load_config, save_image
import sys

# 设置中文字体支持
if sys.platform.startswith('win'):
    default_font = ('Microsoft YaHei UI', 10)
else:
    default_font = ('SimHei', 10)

class ImageGeneratorGUI:
    def __init__(self, root, generate_image_func):
        """初始化图形界面"""
        self.root = root
        self.generate_image_func = generate_image_func
        self.config = load_config()
        self.current_filename = None
        
        # 设置窗口标题和大小
        self.root.title("AI 图像生成器")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # 初始窗口大小设置
        self.root.geometry("900x700")
        
        # 设置主题样式
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # 配置自定义样式
        self.style.configure("TLabel", font=default_font)
        self.style.configure("TButton", font=default_font, padding=5)
        self.style.configure("TCheckbutton", font=default_font)
        self.style.configure("TCombobox", font=default_font)
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # 创建标题标签
        title_label = ttk.Label(self.main_frame, text="AI 图像生成器", font=(default_font[0], 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 创建参数框架
        param_frame = ttk.LabelFrame(self.main_frame, text="生成参数", padding=15)
        param_frame.pack(fill="x", pady=(0, 15))
        
        # 提示词
        ttk.Label(param_frame, text="提示词:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.prompt_entry = ttk.Entry(param_frame, width=60)
        self.prompt_entry.insert(0, "A beautiful sunset over the ocean")
        self.prompt_entry.grid(row=0, column=1, pady=5, columnspan=3)
        
        # 模型选择
        ttk.Label(param_frame, text="模型选择:", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.model_var = tk.StringVar(value=self.config["default_model"])
        models = self.config.get("available_models", ["flux", "gptimage", "kontext"])
        self.model_menu = ttk.Combobox(param_frame, textvariable=self.model_var, values=models, state="readonly", width=15)
        self.model_menu.grid(row=2, column=1, sticky="w", pady=5)
        
        # 图像尺寸
        size_frame = ttk.Frame(param_frame)
        size_frame.grid(row=3, column=0, columnspan=4, sticky="w", pady=5)
        
        ttk.Label(size_frame, text="宽度: ").pack(side="left", padx=(0, 10))
        self.width_entry = ttk.Entry(size_frame, width=10)
        self.width_entry.insert(0, str(self.config["default_width"]))
        self.width_entry.pack(side="left", padx=(0, 20))
        
        ttk.Label(size_frame, text="高度: ").pack(side="left", padx=(0, 10))
        self.height_entry = ttk.Entry(size_frame, width=10)
        self.height_entry.insert(0, str(self.config["default_height"]))
        self.height_entry.pack(side="left")
        
        # 种子值和引用
        seed_referrer_frame = ttk.Frame(param_frame)
        seed_referrer_frame.grid(row=4, column=0, columnspan=4, sticky="w", pady=5)

        ttk.Label(seed_referrer_frame, text="种子值:").pack(side="left", padx=(0, 10))
        self.seed_entry = ttk.Entry(seed_referrer_frame, width=10)
        self.seed_entry.insert(0, "42")
        self.seed_entry.pack(side="left", padx=(0, 20))

        ttk.Label(seed_referrer_frame, text="引用:").pack(side="left", padx=(0, 10))
        self.referrer_entry = ttk.Entry(seed_referrer_frame, width=30)
        self.referrer_entry.insert(0, "")
        self.referrer_entry.pack(side="left")
        
        # 高级选项
        ttk.Label(param_frame, text="高级选项:", anchor="w").grid(row=5, column=0, sticky="w", pady=10)
        
        option_frame = ttk.Frame(param_frame)
        option_frame.grid(row=5, column=1, columnspan=3, sticky="w")
        
        self.nologo_var = tk.BooleanVar(value=self.config["default_nologo"])
        ttk.Checkbutton(option_frame, text="无水印", variable=self.nologo_var).pack(side="left", padx=10)
        
        self.enhance_var = tk.BooleanVar(value=self.config["default_enhance"])
        ttk.Checkbutton(option_frame, text="增强", variable=self.enhance_var).pack(side="left", padx=10)
        
        self.private_var = tk.BooleanVar(value=self.config["default_private"])
        ttk.Checkbutton(option_frame, text="私有模式", variable=self.private_var).pack(side="left", padx=10)
        
        self.safe_var = tk.BooleanVar(value=self.config["default_safe"])
        ttk.Checkbutton(option_frame, text="安全模式", variable=self.safe_var).pack(side="left", padx=10)
        
        # 按钮区域
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=15)
        
        self.generate_button = ttk.Button(button_frame, text="生成图像", command=self.generate, style="Accent.TButton")
        self.generate_button.pack(side="left", padx=10)
        
        self.save_button = ttk.Button(button_frame, text="保存图像", command=self.save_image, state="disabled", style="Accent.TButton")
        self.save_button.pack(side="left", padx=10)
        
        # 状态栏框架
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(side="bottom", fill="x", pady=(10, 15), padx=10)

        # 左侧状态栏标签
        self.status_label_left = ttk.Label(self.status_frame, text="请输入提示词并点击生成", anchor="w")
        self.status_label_left.pack(side="left")

        # 右侧状态栏标签
        self.status_label_right = ttk.Label(self.status_frame, text="", anchor="e")
        self.status_label_right.pack(side="right")
        
        # 图像显示区域（设置最小高度）
        image_frame = ttk.LabelFrame(self.main_frame, text="预览", padding=5)
        image_frame.pack(fill="both", expand=True)
        image_frame.configure(height=400)  # 设置预览区域的最小高度
        
        # 创建画布（无滚动条）
        self.canvas = tk.Canvas(image_frame)
        self.canvas.pack(fill="both", expand=True)
        
        # 创建预览框架
        self.preview_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.preview_frame, anchor="nw")
        
        # 图像标签
        self.image_label = ttk.Label(self.preview_frame, text="图像将在这里显示")
        self.image_label.pack(fill="both", expand=True, pady=2)
        
        # 文件名标签
        self.filename_label = ttk.Label(self.preview_frame, text="", font=('Arial', 10, 'bold'), foreground='black', anchor="center")
        self.filename_label.pack(fill="x", pady=(5, 10))  # 增加底部填充，确保文件名完整显示
        logging.info("文件名标签已创建")
        
        # 配置按钮样式
        self.style.configure("Accent.TButton", foreground="white", background="#4CAF50")
        
        # 绑定窗口大小调整事件
        self.root.bind("<Configure>", self.on_resize)
        
        self.current_image_data = None
        self.current_photo = None
        
        # 在所有组件加载完成后居中窗口
        self.root.after(100, self.center_window)
    
    def on_resize(self, event):
        """处理窗口大小调整，更新预览图像"""
        if self.current_image_data:
            self.update_preview_image()

    def update_preview_image(self):
        """动态更新预览图像大小"""
        if not self.current_image_data:
            return
        
        try:
            img = Image.open(io.BytesIO(self.current_image_data))
            original_width, original_height = img.size
            
            # 获取画布可用空间（减去内边距）
            canvas_width = self.canvas.winfo_width() - 20
            canvas_height = self.canvas.winfo_height() - 40  # 额外减去文件名标签的高度
            
            # 计算缩放比例，保持宽高比
            ratio = min(canvas_width / original_width, canvas_height / original_height, 1.0)
            preview_width = int(original_width * ratio)
            preview_height = int(original_height * ratio)
            
            # 确保最小尺寸
            if preview_width < 1:
                preview_width = 1
            if preview_height < 1:
                preview_height = 1
                
            img = img.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
            self.current_photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_photo, text="")
            self.image_label.image = self.current_photo
            
        except Exception as e:
            logging.error(f"更新预览图像失败: {str(e)}")
            self.status_label_left.config(text=f"显示图像失败: {str(e)}")

    def generate(self):
        """处理图像生成逻辑"""
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            seed = int(self.seed_entry.get())
            if not (256 <= width <= 4096 and 256 <= height <= 4096):
                raise ValueError("宽度和高度必须在 256-4096 之间")
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
            logging.error(f"输入验证失败: {str(e)}")
            return
        
        prompt = self.prompt_entry.get()
        model = self.model_var.get()
        
        # 更新状态和按钮
        self.status_label_left.config(text="正在生成图像，请稍候...")
        self.generate_button.config(state="disabled")
        self.save_button.config(state="disabled")
        
        self.root.update()
        
        try:
            success, result = self.generate_image_func(
                prompt, width, height, seed,
                referrer=self.referrer_entry.get(),
                model=model,
                nologo=self.nologo_var.get(),
                enhance=self.enhance_var.get(),
                private=self.private_var.get(),
                safe=self.safe_var.get()
            )
            if success:
                self.current_image_data = result
                try:
                    # 自动保存图像
                    success_save, path = save_image(result)
                    if success_save:
                        self.current_filename = os.path.basename(path)
                        self.filename_label.config(text=f"{self.current_filename}")
                        logging.info(f"更新文件名标签: {self.current_filename}")
                    else:
                        self.current_filename = None
                        self.filename_label.config(text="保存失败")
                        logging.info("保存失败，更新文件名标签")
                        logging.error(f"自动保存失败: {path}")
                    
                    # 更新预览图像
                    self.update_preview_image()
                    
                    # 获取图像文件大小
                    file_size = len(result) / 1024  # 转换为KB
                    if success_save:
                        self.status_label_left.config(text=f"图像生成成功并已保存 ({width}x{height}, {file_size:.2f}KB)")
                    else:
                        self.status_label_left.config(text=f"图像生成成功 ({width}x{height}, {file_size:.2f}KB)，点击保存图像")
                    self.status_label_right.config(text="")
                    self.save_button.config(state="normal")
                except Exception as e:
                    self.status_label_left.config(text=f"显示图像失败: {str(e)}")
                    self.status_label_right.config(text="")
                    logging.error(f"图像显示失败: {str(e)}")
            else:
                error_msg = result if isinstance(result, str) else "未知错误，请稍后重试"
                self.status_label_left.config(text=error_msg)
                messagebox.showerror("生成失败", error_msg)
        except Exception as e:
            self.status_label_left.config(text=f"生成失败: {str(e)}")
            logging.error(f"生成图像失败: {str(e)}")
        
        self.generate_button.config(state="normal")
    
    def save_image(self):
        """保存图像到用户指定路径"""
        if not self.current_image_data:
            messagebox.showerror("错误", "没有可保存的图像")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        if file_path:
            success, result = save_image(self.current_image_data, file_path)
            if success:
                self.current_filename = os.path.basename(file_path)
                self.filename_label.config(text=f"{self.current_filename}")
                self.status_label_right.config(text=f"图像已保存为 {file_path}")
            else:
                self.status_label_right.config(text=f"图像保存失败: {result}")
    
    def center_window(self):
        """将窗口居中显示在屏幕上"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")