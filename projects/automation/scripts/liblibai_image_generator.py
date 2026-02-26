#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LiblibAI 生图 API 集成脚本
用于 Medium 文章自动生成配图

文档：https://liblibai.feishu.cn/wiki/UAMVw67NcifQHukf8fpccgS5n6d
"""

import requests
import base64
import json
from pathlib import Path
from datetime import datetime

# ==================== 配置区域 ====================

# LiblibAI API 配置（需要填写）
LIBLIB_CONFIG = {
    "api_key": "YOUR_API_KEY_HERE",  # ← 填入你的 API Key
    "base_url": "https://api.liblib.ai",  # ← 确认 API 基础 URL
    "generate_endpoint": "/api/generate",  # ← 确认生图端点
    "timeout": 60,  # 超时时间（秒）
}

# 输出配置
OUTPUT_CONFIG = {
    "output_dir": "/home/jerry/.openclaw/workspace/medium_images",
    "format": "png",  # png 或 jpg
    "quality": 95,
}

# ==================== 生图函数 ====================

def generate_image(prompt, negative_prompt="", width=1024, height=576, **kwargs):
    """
    调用 LiblibAI API 生成图片
    
    参数:
        prompt: 正向提示词
        negative_prompt: 负向提示词
        width: 图片宽度（Medium 封面推荐 1400）
        height: 图片高度（Medium 封面推荐 560）
        **kwargs: 其他 API 参数
    
    返回:
        dict: {
            "success": bool,
            "image_path": str,  # 本地保存路径
            "image_url": str,   # 如果 API 返回 URL
            "error": str        # 错误信息（如果失败）
        }
    """
    
    print(f"🎨 开始生成图片...")
    print(f"   提示词：{prompt[:50]}...")
    print(f"   尺寸：{width}x{height}")
    
    # 准备请求数据
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        **kwargs  # 其他参数
    }
    
    # 准备请求头
    headers = {
        "Authorization": f"Bearer {LIBLIB_CONFIG['api_key']}",
        "Content-Type": "application/json",
    }
    
    try:
        # 发送请求
        response = requests.post(
            f"{LIBLIB_CONFIG['base_url']}{LIBLIB_CONFIG['generate_endpoint']}",
            headers=headers,
            json=payload,
            timeout=LIBLIB_CONFIG['timeout']
        )
        
        # 检查响应
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ API 调用成功")
        
        # 解析响应（根据实际情况调整）
        if "image_url" in result:
            # API 返回图片 URL
            image_url = result["image_url"]
            image_data = download_image(image_url)
        elif "image_base64" in result:
            # API 返回 Base64 编码
            image_data = base64.b64decode(result["image_base64"])
        elif "images" in result and len(result["images"]) > 0:
            # API 返回图片数组
            image_data = base64.b64decode(result["images"][0])
        else:
            return {
                "success": False,
                "error": f"未知的响应格式：{result.keys()}"
            }
        
        # 保存图片
        image_path = save_image(image_data)
        
        return {
            "success": True,
            "image_path": str(image_path),
            "image_url": result.get("image_url", ""),
        }
        
    except requests.exceptions.Timeout:
        return {"success": False, "error": "API 请求超时"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络错误：{e}"}
    except Exception as e:
        return {"success": False, "error": f"未知错误：{e}"}


def download_image(url):
    """下载图片"""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def save_image(image_data):
    """保存图片到本地"""
    output_dir = Path(OUTPUT_CONFIG["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"liblib_{timestamp}.{OUTPUT_CONFIG['format']}"
    filepath = output_dir / filename
    
    # 保存
    with open(filepath, "wb") as f:
        f.write(image_data)
    
    print(f"💾 图片已保存：{filepath}")
    return filepath


# ==================== 预设提示词模板 ====================

PROMPT_TEMPLATES = {
    "cover_trading": {
        "prompt": "Professional AI trading bot dashboard, holographic charts showing upward trend, crypto symbols Bitcoin Ethereum, dark theme with neon blue and green accents, futuristic financial technology, ultra detailed, 8k, cinematic lighting --ar 2.5:1",
        "negative_prompt": "blurry, low quality, distorted, ugly, text, watermark",
        "width": 1400,
        "height": 560,
    },
    
    "performance_chart": {
        "prompt": "Clean financial chart showing 30-day performance, green upward trend line from 0 to 24.7 percent, minimalist design, white background, professional business infographic, high contrast --ar 4:3",
        "negative_prompt": "cluttered, messy, dark, confusing, text, numbers",
        "width": 800,
        "height": 600,
    },
    
    "system_architecture": {
        "prompt": "Modern system architecture diagram, clean flowchart with boxes and arrows, technology stack visualization, blue and white color scheme, minimalist professional style, isometric view --ar 5:4",
        "negative_prompt": "cluttered, messy, colorful, cartoon, 3d render",
        "width": 1000,
        "height": 800,
    },
    
    "arbitrage_concept": {
        "prompt": "Concept art of arbitrage trading, balance scale with YES and NO shares, cryptocurrency symbols, green profit arrow, clean vector illustration, flat design, professional finance style --ar 4:3",
        "negative_prompt": "photorealistic, dark, complex, 3d, cartoon",
        "width": 800,
        "height": 600,
    },
    
    "ai_brain": {
        "prompt": "AI neural network brain analyzing financial data, glowing connections and nodes, blue and purple gradient, futuristic artificial intelligence concept, digital art, high detail --ar 16:9",
        "negative_prompt": "realistic, photograph, dark, scary, robot",
        "width": 1024,
        "height": 576,
    },
}


# ==================== 批量生成函数 ====================

def generate_article_images(image_types=None):
    """
    为文章批量生成配图
    
    参数:
        image_types: 要生成的图片类型列表，默认生成全部
                    可选：["cover", "performance", "architecture", "arbitrage", "ai"]
    
    返回:
        list: 生成的图片路径列表
    """
    
    if image_types is None:
        image_types = ["cover_trading", "performance_chart", "system_architecture"]
    
    generated_images = []
    
    for image_type in image_types:
        if image_type not in PROMPT_TEMPLATES:
            print(f"⚠️  未知的图片类型：{image_type}")
            continue
        
        print(f"\n{'='*60}")
        print(f"🎨 生成图片：{image_type}")
        print(f"{'='*60}")
        
        config = PROMPT_TEMPLATES[image_type]
        
        result = generate_image(
            prompt=config["prompt"],
            negative_prompt=config.get("negative_prompt", ""),
            width=config["width"],
            height=config["height"],
        )
        
        if result["success"]:
            generated_images.append(result["image_path"])
            print(f"✅ 成功：{result['image_path']}")
        else:
            print(f"❌ 失败：{result['error']}")
    
    print(f"\n{'='*60}")
    print(f"📊 生成完成：{len(generated_images)}/{len(image_types)} 张")
    print(f"{'='*60}")
    
    return generated_images


# ==================== 主函数 ====================

def main():
    """主函数"""
    print("="*60)
    print("🎨 LiblibAI 生图工具")
    print("="*60)
    print()
    
    # 检查 API Key
    if LIBLIB_CONFIG["api_key"] == "YOUR_API_KEY_HERE":
        print("❌ 错误：请先配置 API Key")
        print()
        print("编辑此文件，修改 LIBLIB_CONFIG 中的 api_key:")
        print(f"   api_key: \"YOUR_API_KEY_HERE\"  →  \"你的实际 API Key\"")
        print()
        print("API Key 获取方式:")
        print("1. 访问：https://liblibai.feishu.cn/wiki/UAMVw67NcifQHukf8fpccgS5n6d")
        print("2. 查看 API 文档")
        print("3. 获取 API Key")
        return
    
    # 生成文章配图（默认 3 张：封面 + 收益图 + 架构图）
    images = generate_article_images()
    
    if images:
        print()
        print("📁 生成的图片:")
        for img in images:
            print(f"   - {img}")
        print()
        print("✅ 完成！现在可以在 Medium 文章中使用这些图片了")
    else:
        print()
        print("❌ 没有成功生成任何图片")


if __name__ == "__main__":
    main()
