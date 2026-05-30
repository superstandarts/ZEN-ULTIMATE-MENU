
from pathlib import Path
from PIL import Image

class ImageTools:
    def resize(self, src, dst, width, height):
        img = Image.open(src)
        img = img.resize((int(width), int(height)))
        img.save(dst)
        return str(dst)

    def compress(self, src, dst, quality=75):
        img = Image.open(src)
        if dst.lower().endswith((".jpg",".jpeg")):
            img = img.convert("RGB")
            img.save(dst, quality=int(quality), optimize=True)
        else:
            img.save(dst, optimize=True)
        return str(dst)

    def remove_metadata(self, src, dst):
        img = Image.open(src)
        data = list(img.getdata())
        clean = Image.new(img.mode, img.size)
        clean.putdata(data)
        clean.save(dst)
        return str(dst)
