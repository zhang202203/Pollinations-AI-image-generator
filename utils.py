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

def save_image(image_data, path):
    """保存图像并记录日志"""
    try:
        with open(path, "wb") as f:
            f.write(image_data)
        logging.info(f"图像保存成功: {path}")
        return True
    except Exception as e:
        logging.error(f"图像保存失败: {str(e)}")
        return False