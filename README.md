# Pollinations.AI 图像生成器

## 版本信息
Version 1.5

一个基于 Python 的桌面应用程序，通过 Pollinations.AI API 生成 AI 图像，支持自定义多种参数和直观的中文用户界面。项目设计模块化，适合开发者和初创公司快速集成 AI 图像生成功能，灵感来源于Pollinations.AI 提供的免费 API 生成 AI 图像，为开发者提供经济高效的解决方案。

## 功能特点

- 直观的图形用户界面，支持中文显示
- 程序启动时窗口自动居中显示在屏幕中央
- 完整的 Pollinations.AI API 参数自定义（包括提示词、模型选择等）
- 图像预览和缩放功能，自动适应窗口大小
- 自动保存生成的图像到 `Images/` 目录，文件名格式为 `YYYY-MM-DD_AI0001.jpg`，序号自动递增
- 图像下方居中显示文件名，便于用户识别
- 支持手动保存图像为 JPEG 或 PNG 格式
- 详细的日志记录，保存至 `logs/` 目录
- 可配置的默认参数，通过 `config.json` 设置
- 支持多种 AI 模型选择（例如 `flux`、`gptimage`、`kontext`）
- 添加引用(Referrer)参数支持，用于基于引用的身份验证
- 种子值设置，支持复现相同图像
- 高级选项支持：无水印、增强、私有模式和安全模式
- 图像生成成功后显示分辨率（原始尺寸）和文件大小信息
- 状态栏位置优化，分为左右两部分显示：
  - 左侧：显示图像生成状态和信息
  - 右侧：显示图像保存状态和路径
- 提供测试脚本（Test.py）用于查询可用的图像模型

## 安装指南

### 前提条件
- Python 3.10 或更高版本
- pip (Python 包管理器)
- 网络连接（用于调用 Pollinations.AI API）

### 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/your-username/pollinations-ai-image-generator.git
   cd pollinations-ai-image-generator
   ```

2. **安装依赖**
   打开终端，导航到项目目录，运行以下命令：
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用程序**
   ```bash
   python main.py
   ```

## 使用方法

1. **启动应用程序**
   运行 `main.py` 后，将显示应用程序主界面，界面支持中文显示。

2. **设置生成参数**
   - **提示词(Prompt)**: 输入描述您想要生成的图像的文本（如"A beautiful sunset over the ocean"）。
   - **模型选择**: 从下拉菜单中选择 AI 模型（如 `flux`、`gptimage` 或 `kontext`）。
   - **图像尺寸**: 设置宽度和高度（默认 1024x1024，范围必须在 256-4096 之间）。
   - **种子值**: 设置随机种子，相同的种子值可以生成相同的图像（默认 42）。
   - **引用(Referrer)**: 可选，用于基于引用的身份验证（默认空）。
   - **高级选项**: 勾选相应选项设置 `无水印`、`增强`、`私有模式` 和 `安全模式`。

3. **生成图像**
   点击"生成图像"按钮，状态栏将显示生成进度（如"正在生成图像，请稍候..."）。

4. **查看和保存图像**
   - 生成完成后，图像会自动保存到 `Images/` 目录，文件名格式为 `YYYY-MM-DD_AI0001.jpg`，同一天生成的图像序号会自动递增（如0001, 0002等）。
   - 图像会在预览区域显示，并自动适应窗口大小。
   - 如需保存到其他位置，点击"保存图像"按钮，选择保存路径和格式（JPEG 或 PNG）。
   - 状态栏会显示图像的分辨率和文件大小信息。

## 项目结构

```
Pollinations-AI-Image-Generator/
├── main.py           # 程序入口，初始化 GUI 和事件处理
├── api.py            # Pollinations.AI API 调用处理
├── gui.py            # 用户界面实现，包含输入框、按钮和图像显示
├── utils.py          # 工具函数（日志记录、图像处理等）
├── config.json       # 默认参数配置文件
├── Test.py           # 测试脚本，用于列出可用的图像模型
├── Images/           # 生成的图像保存目录
├── logs/             # 日志文件目录，存储运行日志
└── README.markdown   # 项目文档
```

## 配置文件

应用程序使用 `config.json` 文件存储默认参数，您可以编辑此文件自定义默认设置：

```json
{
    "default_model": "flux",
    "default_width": 1024,
    "default_height": 1024,
    "default_nologo": true,
    "default_enhance": false,
    "default_private": false,
    "default_safe": false,
    "default_preview_width": 146,
    "default_preview_height": 146
}
```

## 故障排除

- **无法生成图像**: 检查网络连接，确保 `https://image.pollinations.ai/prompt/` 可访问。
- **参数错误**: 确保宽度和高度在 256-4096 范围内，种子值为整数。
- **中文显示问题**: 程序已配置中文字体支持（如“微软雅黑”），如仍有问题，请确保系统已安装中文字体。
- **保存失败**: 检查目标路径权限和可用空间，确保 `logs/` 目录可写。

## 依赖项

- Python 3.10+
- tkinter (GUI 框架，Python 内置)
- requests (API 调用)
- Pillow (图像处理)
- json (配置文件处理，Python 内置)
- logging (日志记录，Python 内置)
- datetime (时间处理，Python 内置)
- os (文件系统操作，Python 内置)

安装第三方依赖：
```bash
pip install requests Pillow
```

## 许可证

本项目采用 MIT 许可证 - 详情参见 [LICENSE](LICENSE) 文件。

## 致谢

- [Pollinations.AI](https://pollinations.ai/) 提供的 API 服务。
- Python 社区提供的优秀库支持（如 `tkinter`、`requests`、`Pillow`）。
- 灵感来源于Pollinations.AI 提供的免费 API 生成 AI 图像，为开发者提供经济高效的解决方案。