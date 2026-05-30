
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class FakeTerminalGenerator:
    def generate(self, text, output, width=1200, height=650):
        img = Image.new("RGB", (int(width), int(height)), "#050507")
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((20, 20, int(width)-20, int(height)-20), radius=24, fill="#0d0e12", outline="#333640", width=2)
        draw.ellipse((50, 50, 66, 66), fill="#ff5f57")
        draw.ellipse((76, 50, 92, 66), fill="#ffbd2e")
        draw.ellipse((102, 50, 118, 66), fill="#28c840")
        y = 105
        for line in text.splitlines():
            draw.text((55, y), line, fill="#e8e8e8")
            y += 28
            if y > int(height)-55:
                break
        img.save(output)
        return str(output)
