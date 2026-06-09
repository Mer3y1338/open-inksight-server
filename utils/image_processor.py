import os
import random
from PIL import Image, ImageEnhance, ImageOps

def process_image(image_path, output_path, enable_paper_filter=True):
    """
    处理图片：裁剪为 16:9 (以右上角为基准)，并应用黑白纸感滤镜。
    适合 InkSight 墨水屏的观感。
    """
    try:
        with Image.open(image_path) as img:
            # 1. 计算 16:9 裁剪框
            img_w, img_h = img.size
            target_ratio = 16 / 9
            current_ratio = img_w / img_h
            
            if current_ratio > target_ratio:
                # 图片太宽，截取右侧 (右上裁切偏好)
                new_w = int(img_h * target_ratio)
                left = img_w - new_w
                box = (left, 0, img_w, img_h)
            else:
                # 图片太高，截取顶部 (右上裁切偏好)
                new_h = int(img_w / target_ratio)
                box = (0, 0, img_w, new_h)
                
            img_cropped = img.crop(box)
            
            # 2. 纸感滤镜处理
            if enable_paper_filter:
                # 转换为灰度图
                img_cropped = img_cropped.convert("L")
                
                # 增加对比度，让黑白分明，更有"墨水"感
                enhancer = ImageEnhance.Contrast(img_cropped)
                img_cropped = enhancer.enhance(1.2)
                
                # 稍微增加亮度，模拟纸张底色
                bright_enhancer = ImageEnhance.Brightness(img_cropped)
                img_cropped = bright_enhancer.enhance(1.1)

                # 添加黑白边框效果 (内缩加黑边)
                img_cropped = ImageOps.expand(img_cropped, border=10, fill='white')
                img_cropped = ImageOps.expand(img_cropped, border=4, fill='black')
                
            # 3. 统一缩放到适合墨水屏的尺寸 (例如 800x450)
            img_resized = img_cropped.resize((800, 450), Image.Resampling.LANCZOS)
            
            img_resized.save(output_path, "JPEG", quality=85)
            return True
    except Exception as e:
        print(f"图片处理失败: {e}")
        return False

def get_random_local_image(images_dir, cache_dir, enable_paper_filter=True):
    """从本地目录随机抽取一张图片并处理返回缓存路径"""
    if not os.path.exists(images_dir):
        os.makedirs(images_dir, exist_ok=True)
        
    valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    images = [f for f in os.listdir(images_dir) if f.lower().endswith(valid_exts)]
    
    if not images:
        return None
        
    selected_image = random.choice(images)
    source_path = os.path.join(images_dir, selected_image)
    
    # 缓存处理后的图片
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        
    cached_filename = f"ink_processed_{selected_image}"
    cached_path = os.path.join(cache_dir, cached_filename)
    
    # 如果已经处理过，直接返回
    if os.path.exists(cached_path):
        return cached_path
        
    if process_image(source_path, cached_path, enable_paper_filter):
        return cached_path
        
    return None