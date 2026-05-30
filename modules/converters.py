
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, os

class Converters:
    image_exts = {".png",".jpg",".jpeg",".webp",".bmp",".ico"}

    def convert_image(self, src, dst):
        src = Path(src); dst = Path(dst)
        img = Image.open(src)
        if dst.suffix.lower() in [".jpg", ".jpeg"]:
            img = img.convert("RGB")
        img.save(dst)
        return str(dst)

    def image_to_ico(self, src, dst):
        img = Image.open(src)
        img.save(dst, format="ICO", sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)])
        return str(dst)

    def text_to_pdf(self, src, dst):
        src = Path(src); dst = Path(dst)
        text = src.read_text(encoding="utf-8", errors="replace")
        lines = []
        for line in text.splitlines():
            while len(line) > 90:
                lines.append(line[:90])
                line = line[90:]
            lines.append(line)

        w, h = 1240, 1754
        pages = [lines[i:i+58] for i in range(0, len(lines), 58)] or [[]]
        images = []
        for page in pages:
            img = Image.new("RGB", (w,h), "white")
            d = ImageDraw.Draw(img)
            y = 70
            for line in page:
                d.text((70,y), line, fill="black")
                y += 28
            images.append(img)
        images[0].save(dst, save_all=True, append_images=images[1:])
        return str(dst)

    def ffmpeg_available(self):
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True)
            return True
        except Exception:
            return False

    def video_to_gif(self, src, dst, fps=12, width=480):
        if not self.ffmpeg_available():
            return "FFmpeg not found. Install FFmpeg and add it to PATH."
        cmd = ["ffmpeg","-y","-i",str(src),"-vf",f"fps={fps},scale={width}:-1:flags=lanczos",str(dst)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.stdout + r.stderr or str(dst)
