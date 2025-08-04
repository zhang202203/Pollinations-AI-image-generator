import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import io
import logging
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
        
        # 设置窗口标题和大小
        self.root.title("Pollinations.AI 图像生成器")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 设置主题样式
        self.style = ttk.Style()
        self.style.theme_use("clam")  # 使用clam主题，更加现代
        
        # 配置自定义样式
        self.style.configure("TLabel", font=default_font)
        self.style.configure("TButton", font=default_font, padding=5)
        self.style.configure("TCheckbutton", font=default_font)
        self.style.configure("TCombobox", font=default_font)
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # 创建标题标签
        title_label = ttk.Label(self.main_frame, text="Pollinations.AI 图像生成器", font=(default_font[0], 16, "bold"))
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
        models = ["flux", "gptimage", "kontext"]
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
        
        # 种子值
        ttk.Label(param_frame, text="种子值:", anchor="w").grid(row=4, column=0, sticky="w", pady=5)
        self.seed_entry = ttk.Entry(param_frame, width=10)
        self.seed_entry.insert(0, "42")
        self.seed_entry.grid(row=4, column=1, sticky="w", pady=5)
        
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
        
        self.save_button = ttk.Button(button_frame, text="保存图像", command=self.save_image, state="disabled")
        self.save_button.pack(side="left", padx=10)
        
        # 状态栏
        self.status_label = ttk.Label(self.main_frame, text="请输入提示词并点击生成", anchor="w")
        self.status_label.pack(fill="x", pady=(10, 15))
        
        # 图像显示区域
        image_frame = ttk.LabelFrame(self.main_frame, text="预览", padding=15)
        image_frame.pack(fill="both", expand=True)
        
        self.image_label = ttk.Label(image_frame, text="图像将在这里显示")
        self.image_label.pack(expand=True)
        
        # 配置按钮样式
        self.style.configure("Accent.TButton", foreground="white", background="#4CAF50")
        
        self.current_image_data = None
    
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
        self.status_label.config(text="正在生成图像，请稍候...")
        self.generate_button.config(state="disabled")
        self.save_button.config(state="disabled")
        
        # 创建进度条
        progress_window = tk.Toplevel(self.root)
        progress_window.title("生成中")
        progress_window.geometry("300x100")
        progress_window.resizable(False, False)
        
        # 居中显示进度窗口
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        progress_label = ttk.Label(progress_window, text="图像生成中...")
        progress_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=250, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start()
        
        self.root.update()
        
        try:
            success, result = self.generate_image_func(
                prompt, width, height, seed, model,

                nologo=self.nologo_var.get(),
                enhance=self.enhance_var.get(),
                private=self.private_var.get(),
                safe=self.safe_var.get()
            )
        finally:
            # 无论成功失败，都关闭进度窗口
            progress_bar.stop()
            progress_window.destroy()
        
        if success:
            self.current_image_data = result
            try:
                img = Image.open(io.BytesIO(result))
                # 计算调整后的尺寸，保持宽高比，确保完整显示在预览框
                # 设置固定预览高度为160像素
                preview_height = 160
                
                img_width, img_height = img.size
                # 根据图像原始比例计算宽度
                ratio = preview_height / img_height
                preview_width = int(img_width * ratio)
                
                # 确保宽度至少为1像素
                if preview_width <= 1:
                    preview_width = 1
                
                # 计算调整后的尺寸，保持宽高比
                ratio = preview_height / img_height
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo
                self.status_label.config(text="图像生成成功，点击保存图像")
                self.save_button.config(state="normal")
            except Exception as e:
                self.status_label.config(text=f"显示图像失败: {str(e)}")
                logging.error(f"图像显示失败: {str(e)}")
        else:
            self.status_label.config(text=result)
            messagebox.showerror("生成失败", result)
        
        self.generate_button.config(state="normal")
    
    def save_image(self):
        """保存图像到用户指定路径"""
        if not self.current_image_data:
            messagebox.showerror("错误", "没有可保存的图像")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            if save_image(self.current_image_data, file_path):
                self.status_label.config(text=f"图像已保存为 {file_path}")
            else:
                self.status_label.config(text="图像保存失败")