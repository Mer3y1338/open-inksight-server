# Open-InkSight-Server

一个轻量级的 InkSight 墨水屏私有化推送服务端。支持自定义图片流、天气、文案以及系统监控数据推送。

## ✨ 特性

- 🖼️ **本地图库随机推送**：自动将图片处理为黑白纸感风格。
- 🌤️ **自定义天气**：对接标准天气 API。
- 📝 **自定义文案**：底部落款、问候语完全自定义。
- 💻 **本地探针替代**：可选开启本机资源监控推送到墨水屏，无需依赖外部 Server Dashboard。

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/YourName/open-inksight-server.git
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
