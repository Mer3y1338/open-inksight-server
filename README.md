# Open-InkSight-Server

一个轻量级的 InkSight 墨水屏私有化推送服务端。支持自定义图片流、天气、文案以及系统监控数据推送。

## ✨ 特性

- 🖼️ **本地图库随机推送**：自动将图片处理为黑白纸感风格。
- 🌤️ **自定义天气**：对接标准天气 API。
- 📝 **自定义文案**：底部落款、问候语完全自定义。
- 💻 **本地探针替代**：可选开启本机资源监控推送到墨水屏，无需依赖外部 Server Dashboard。

---

## 🤖 AI Agent 自动化部署教程 (推荐)

如果你的日常流重度依赖 AI Agent（如 Hermes、Claude Code 等），你**完全不需要手动敲代码**！只需复制以下 Prompt 发送给你的 Agent，让它全自动帮你完成部署：

**复制这段 Prompt 发送给你的 Agent：**
```text
请帮我在服务器上部署 Open-InkSight-Server。
1. 克隆仓库 https://github.com/Mer3y1338/open-inksight-server.git 到本地目录。
2. 配置 Python 虚拟环境并安装 requirements.txt 中的依赖。
3. 把 config.example.yaml 复制一份命名为 config.yaml。
4. 帮我修改 config.yaml，把 footer_text 改成 "摸鱼中"，owner_name 改成我的名字。
5. 使用 systemd 为其创建一个后台服务，确保开机自启，并立即启动。
6. 检查服务运行状态，并告诉我最终给墨水屏填写的 Server URL 是什么。
```
*注：你可以告诉 Agent 你想改的文案和天气配置，它会帮你搞定一切。*

---

## 🚀 传统手动部署

如果你喜欢亲自动手：

```bash
# 1. 克隆项目
git clone https://github.com/Mer3y1338/open-inksight-server.git
cd open-inksight-server

# 2. 安装依赖
pip install -r requirements.txt

# 3. 复制并修改配置
cp config.example.yaml config.yaml
# 编辑 config.yaml 填入你的天气API和文案

# 4. 放入你的图片
# 将图片放入 data/images/ 目录下

# 5. 启动服务
python main.py
```

## ⚙️ 墨水屏端配置

在你的 InkSight 硬件设置页面，将 `Server URL` 修改为你部署该服务机器的局域网 IP（例如：`http://192.168.1.100:8080`）。
