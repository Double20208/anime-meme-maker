from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import Response
from generator import create_meme

app = FastAPI(
    title="Anime Meme API",
    description="Production-grade Meme Generation Microservice",
    version="1.0.0"
)

@app.post("/generate/", summary="生成表情包", response_class=Response)
async def generate_meme_endpoint(
    image: UploadFile = File(..., description="原始动漫截图/图片"),
    top_text: str = Form("", description="顶部文本"),
    bottom_text: str = Form("", description="底部文本")
):
    """
    接收图像上传和自定义文本，返回渲染后的表情包流。
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传有效的图片文件。")
        
    try:
        # 读取上传文件
        img_bytes = await image.read()
        
        # 调用图像处理逻辑
        meme_bytes = create_meme(img_bytes, top_text, bottom_text)
        
        # 返回图片流
        return Response(content=meme_bytes, media_type="image/jpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图像处理失败: {str(e)}")