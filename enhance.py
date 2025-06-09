import sys
import fitz  # PyMuPDF

from pathlib import Path
from PIL import Image, ImageFilter


# Low effort working script...
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: enhance.py <source> <destination>') 
        exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    if not src.exists():
        print(f'Source is invalid, "{src}" does not exist')
        exit(1)

    doc = fitz.open(src)
    images = []

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # ~144 dpi
        img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150,
                                                 threshold=3))
        images.append(img.convert('RGB'))

    images[0].save(dst, save_all=True, append_images=images[1:], resolution=300)
