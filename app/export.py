
from PIL import Image, ImageDraw, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
from collections import defaultdict

def render_strokes(history, canvasH, canvasW):
    pdf_buffer = io.BytesIO()
    sizeH = 2160
    sizeW = 3840
    c = canvas.Canvas(pdf_buffer, pagesize=(sizeW, sizeH))

    scaleX = sizeW / canvasW
    scaleY = sizeH / canvasH
    scaleAvg = (scaleX + scaleY) / 2

    # Group strokes by page
    pages = defaultdict(list)
    for stroke in history:
        pages[stroke.get("page")].append(stroke)

    for pageNum in sorted(pages.keys()):
        img = Image.new("RGB", (sizeW, sizeH), "white")
        draw = ImageDraw.Draw(img)

        for stroke in pages[pageNum]:
            size = stroke.get("size")
            colour = stroke.get("colour")
            width = int(size * scaleAvg)
            flag = 0

            for x0, y0 in stroke.get("points"):
                x = x0 * scaleX
                y = y0 * scaleY

                if flag:
                    draw.line([hx, hy, x, y], fill=colour, width=width)
                else:
                    r = width // 2
                    draw.ellipse([x - r, y - r, x + r, y + r], fill=colour)
                    flag = 1

                hx, hy = x, y

        # CPU-intensive filter
        img = img.filter(ImageFilter.UnsharpMask(radius=5, percent=150, threshold=3))
        c.drawImage(ImageReader(img), 0, 0, width=sizeW, height=sizeH)
        c.showPage()

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

