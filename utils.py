# 工具函数（日志记录、图像处理等）
import os
import logging
from datetime import datetime
from PIL import Image
import json

# 配置日志
def setup_logging():
    """初始化日志记录，保存到 logs/ 目录"""
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        #handlers=[]  # 清空 handlers，禁用所有日志输出
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def load_config():
    """加载 config.json 中的默认参数"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("config.json 未找到，使用默认参数")
        return {
            "default_model": "flux",
            "default_width": 1024,
            "default_height": 1024,
            "default_nologo": True,
            "default_enhance": False,
            "default_private": False,
            "default_safe": True
        }

def generate_unique_filename():
    """生成唯一的文件名，格式为：YYYY-MM-DD_AI0001.jpg，序号从0001开始，同名文件存在时序号+1"""
    # 获取当前日期
    date_str = datetime.now().strftime("%Y-%m-%d")
    # 确保Images目录存在
    os.makedirs("Images", exist_ok=True)
    
    # 基础文件名格式
    base_filename = f"{date_str}_AI"
    counter = 1
    
    # 检查文件是否存在，如果存在则序号+1
    while True:
        # 格式化序号为4位数，例如0001, 0002等
        formatted_counter = f"{counter:04d}"
        filename = f"{base_filename}{formatted_counter}.jpg"
        full_path = os.path.join("Images", filename)
        
        # 如果文件不存在，则返回该路径
        if not os.path.exists(full_path):
            return full_path
        
        # 文件存在，序号+1继续尝试
        counter += 1

def save_image(image_data, path=None):
    """保存图像并记录日志

    参数:
        image_data (bytes): 图像数据
        path (str, optional): 保存路径，如果为None则自动生成

    返回:
        tuple: (成功标志, 保存路径或错误消息)
    """
    try:
        # 如果没有提供路径，则生成唯一文件名
        if path is None:
            path = generate_unique_filename()
        
        with open(path, "wb") as f:
            f.write(image_data)
        logging.info(f"图像保存成功: {path}")
        return True, path
    except Exception as e:
        logging.error(f"图像保存失败: {str(e)}")
        return False, str(e)