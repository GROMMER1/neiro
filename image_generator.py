import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def generate_image_from_text(text: str) -> str:
    # Простой генератор картинки на основе текста (заглушка)
    img = Image.new('RGB', (512, 256), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 120), text[:100], fill=(255, 255, 0))

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
