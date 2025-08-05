import urllib.parse
import logging
import requests
from utils import setup_logging

# 初始化日志
setup_logging()

def generate_image(prompt, width, height, seed, referrer="", model="flux", nologo=True, enhance=False, private=False, safe=True):
    """
    调用 Pollinations AI API 生成图像，并返回图像数据或错误信息。
    
    参数:
        prompt (str): 图像描述文本
        width (int): 图像宽度
        height (int): 图像高度
        seed (int): 随机种子
        model (str): 使用的模型，默认为 "flux"
        nologo (bool): 是否移除水印
        enhance (bool): 是否增强图像
        private (bool): 是否私有生成
        safe (bool): 是否启用安全模式
    
    返回:
        tuple: (成功标志, 图像数据或错误消息)
    """
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    params = {
        "width": width,
        "height": height,
        "seed": seed,
        "model": model,
        "nologo": str(nologo).lower(),
        "enhance": str(enhance).lower(),
        "private": str(private).lower(),
        "safe": str(safe).lower()
    }

    # 如果referrer不为空，则添加到参数中
    if referrer:
        params["referrer"] = referrer
    
    try:
        logging.info(f"发送 API 请求: {url}, 参数: {params}")
        response = requests.get(url, params=params, timeout=300)
        response.raise_for_status()
        logging.info("图像生成成功")
        return True, response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"API 请求失败: {str(e)}")
        return False, f"错误: {str(e)}"
