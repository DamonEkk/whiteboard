from PIL import Image, ImageDraw, ImageFilter
import io


def render_strokes(history, canvasH, canvasW):
    pageList = []

    pageNum = -1
    heightScale = 2160 / canvasH # Used to upscale the lines
    widthScale = 3840 / canvasW
    strokeID = -1
        

    # Goes through full history of all canvas drawing
    for stroke in history:
        flag = 0
        
        if stroke.get("page") != pageNum:
            if pageNum != -1:
                newImage = newImage.filter(ImageFilter.UnsharpMask(radius=5, percent=150, threshold=3)) # Really just to add to cpu intensive rubric requirement would remove in practise


                pageList.append(newImage)

            pageNum = stroke.get("page")
            newImage = Image.new("RGB", (3840, 2160), "white")
            drawImage = ImageDraw.Draw(newImage)
            
        
        strokeSize = stroke.get("size")
        colour = stroke.get("colour")

        # Goes through all coordinates where there has been a drawing.
        for coords in stroke.get("points"):
            x = coords[0] * widthScale
            y = coords[1] * heightScale

            # The flag is turned on once the first point has been drawn, this flag connects previous point to current point.
            if flag == 1:
                drawImage.line([historyX+strokeSize//2, historyY+strokeSize//2, x+strokeSize//2, y+strokeSize//2], fill=colour, width= int(strokeSize * widthScale));

            else:
                flag = 1
                drawImage.ellipse([x-strokeSize//2, y-strokeSize//2, x+strokeSize//2, y+strokeSize//2], fill=colour); 


            historyX = x
            historyY = y

    # Adds the last page to the list
    newImage = newImage.filter(ImageFilter.UnsharpMask(radius=5, percent=150, threshold=3))
    pageList.append(newImage)

    # PDF combatible 
    images = [img.convert("RGB") for img in pageList]

    pdf = io.BytesIO() # Used to store a pdf
    images[0].save(pdf, format="PDF", save_all=True, append_images=images[1:])
    pdf.seek(0)

    return pdf
