import io
import os
from PIL import Image, ImageDraw, ImageFont

# 预加载字体以优化性能
FONT_PATH = "font.ttf"
DEFAULT_FONT_SIZE_RATIO = 0.1  # 字体大小默认为图片高度的 10%

def create_meme(image_bytes: bytes, top_text: str, bottom_text: str) -> bytes:
    """
    接收原始图像字节和文本，返回合成后的 PNG/JPEG 图像字节流。
    """
    # 纯内存操作，避免磁盘 I/O
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size

    # 动态计算字体大小
    font_size = max(int(img_h * DEFAULT_FONT_SIZE_RATIO), 20)
    
    try:
        if os.path.exists(FONT_PATH):
            font = ImageFont.truetype(FONT_PATH, font_size)
        else:
            # 如果没找到 font.ttf，回退到默认字体（可能不支持中文）
            font = ImageFont.load_default()
    except IOError:
        font = ImageFont.load_default()

    def draw_text_with_outline(text: str, y_pos: int):
        if not text:
            return
            
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        
        # 计算居中 X 坐标
        x = (img_w - text_w) / 2
        y = y_pos

        # Meme 风格: 黑色描边 
        outline_color = "black"
        stroke_width = max(int(font_size * 0.05), 2)
        
        for adj in range(-stroke_width, stroke_width + 1):
            for opp in range(-stroke_width, stroke_width + 1):
                if adj != 0 or opp != 0:
                    draw.text((x + adj, y + opp), text, font=font, fill=outline_color)
                    
        # 绘制核心白色文本
        draw.text((x, y), text, font=font, fill="white")

    # 渲染顶部文本 (留出 5% 的上边距)
    if top_text:
        draw_text_with_outline(top_text, int(img_h * 0.05))
        
    # 渲染底部文本 (留出 5% 的下边距 + 字体自身高度)
    if bottom_text:
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_h = bbox[3] - bbox[1]
        draw_text_with_outline(bottom_text, int(img_h * 0.95) - text_h)

    # 导出到内存缓冲区
    output_buffer = io.BytesIO()
    img.convert("RGB").save(output_buffer, format="JPEG", quality=90)
    return output_buffer.getvalue()