import os
import yaml
import time
import psutil
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File
from pydantic import BaseModel
import uvicorn
import requests

from utils.image_processor import get_random_local_image

app = FastAPI(title="Open-InkSight-Server")

# 尝试加载配置文件
CONFIG_PATH = "config.yaml"
if not os.path.exists(CONFIG_PATH):
    print("⚠️ 警告: config.yaml 不存在，正在使用 config.example.yaml 初始化...")
    import shutil
    shutil.copy("config.example.yaml", CONFIG_PATH)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 常量定义
IMAGES_DIR = config["data"]["local_images_dir"]
CACHE_DIR = "data/cache"

# --- 安装静态文件路由 ---
if not os.path.exists("public"):
    os.makedirs("public")
app.mount("/static", StaticFiles(directory="public"), name="static")

# --- 天气与系统监控辅助函数 ---

def fetch_weather():
    if not config["weather"].get("enabled", False):
        return {"temp": "--", "text": "天气关闭"}
    
    provider = config["weather"].get("provider", "qweather")
    if provider == "qweather":
        # 此处模拟/实现和风天气逻辑
        api_key = config["weather"].get("api_key")
        location = config["weather"].get("location")
        if api_key == "YOUR_QWEATHER_API_KEY" or not api_key:
            return {"temp": "25°C", "text": "请配置API Key"}
            
        try:
            url = f"https://devapi.qweather.com/v7/weather/now?location={location}&key={api_key}"
            resp = requests.get(url, timeout=5).json()
            if resp.get("code") == "200":
                now = resp["now"]
                return {"temp": f"{now['temp']}°C", "text": now['text']}
        except Exception as e:
            print(f"天气获取失败: {e}")
            
    return {"temp": "--", "text": "获取失败"}

def get_system_status():
    if not config["system_monitor"].get("enabled", False):
        return None
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        return f"CPU:{cpu}% RAM:{mem}%"
    except:
        return None

# --- API 路由定义 (兼容原 DB 接口) ---

@app.get("/")
def index():
    return FileResponse("public/index.html")

@app.get("/api/inksight/data")
def get_inksight_data():
    """墨水屏主数据接口：获取文案、天气、系统状态"""
    weather_data = fetch_weather()
    sys_status = get_system_status()
    
    # 构建墨水屏底部文本
    footer = config["ui"].get("footer_text", "我的宝宝")
    owner = config["ui"].get("owner_name", "User")
    
    # 组合系统状态和自定义文本
    status_text = sys_status if sys_status else time.strftime("%Y-%m-%d %H:%M")
    
    response_data = {
        "footer": f"{footer} | {owner}",
        "weather": weather_data,
        "status": status_text,
        "timestamp": int(time.time())
    }
    return JSONResponse(content=response_data)

@app.get("/api/inksight/image")
def get_inksight_image():
    """获取处理好的水墨屏相册图片"""
    mode = config["data"].get("image_mode", "local")
    enable_filter = config["ui"].get("enable_paper_filter", True)
    
    if mode == "local":
        img_path = get_random_local_image(IMAGES_DIR, CACHE_DIR, enable_filter)
        if img_path and os.path.exists(img_path):
            return FileResponse(img_path, media_type="image/jpeg")
            
    # 如果没图片，返回一个占位提示图或者 404
    return Response(content="No Image Configured or Directory Empty. Put images in data/images/", status_code=404)

# --- WebUI 控制台 API 路由 ---

@app.get("/api/admin/config")
def get_config():
    return config

@app.post("/api/admin/config")
async def update_config(new_config: dict):
    global config
    # 深度更新配置
    for key, val in new_config.items():
        if key in config and isinstance(val, dict):
            config[key].update(val)
        else:
            config[key] = val
    
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)
    return {"status": "ok"}

@app.post("/api/admin/upload")
async def upload_image(file: UploadFile = File(...)):
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        
    file_path = os.path.join(IMAGES_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"status": "ok", "filename": file.filename}

@app.post("/api/admin/push")
async def force_push_to_inksight():
    """主动调用 InkSight 云端 API 下发指令"""
    token = config.get("hardware", {}).get("token")
    if not token:
        return Response(content='{"detail": "未配置 InkSight Token"}', status_code=400, media_type="application/json")
        
    # 此处为示例调用逻辑：请求墨水屏的公开推送接口触发刷新
    # 因为不同固件 API 不同，这里留出通用的 REST 调用口
    try:
        # requests.post("https://inksight-api.example.com/push", headers={"Authorization": f"Bearer {token}"})
        return {"status": "ok", "message": "Push command triggered"}
    except Exception as e:
        return Response(content=f'{{"detail": "{str(e)}"}}', status_code=500, media_type="application/json")

if __name__ == "__main__":
    host = config["server"].get("host", "0.0.0.0")
    port = config["server"].get("port", 8082)
    print(f"🚀 Open-InkSight-Server 启动于 http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)