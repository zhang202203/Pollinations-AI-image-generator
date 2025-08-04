import tkinter as tk
from gui import ImageGeneratorGUI
from api import generate_image

def main():
    # 创建主窗口
    root = tk.Tk()
    # 初始化 GUI，传入主窗口和 API 调用函数
    app = ImageGeneratorGUI(root, generate_image)
    # 启动主事件循环
    root.mainloop()

if __name__ == "__main__":
    main()