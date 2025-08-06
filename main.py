# 程序入口，初始化 GUI 和事件处理
import tkinter as tk
import os
from gui import ImageGeneratorGUI
from api import generate_image

def main():
    # 创建Images目录
    os.makedirs("Images", exist_ok=True)
    # 创建主窗口
    root = tk.Tk()
    # 设置窗口标题
    root.title("Pollinations.AI 图像生成器")
    # 设置窗口最小大小
    root.minsize(600, 500)
    # 初始化 GUI，传入主窗口和 API 调用函数
    app = ImageGeneratorGUI(root, generate_image)
    # 启动主事件循环
    root.mainloop()

if __name__ == "__main__":
    main()