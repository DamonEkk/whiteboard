from PIL import Image, ImageDraw
pageNum = -1
pageList = []

def render_strokes(history, canvasH, canvasW):


    heightScale = 2160 / canvasH
    widthScale = 3840 / canvasW
    

    for stroke in history:
        if stroke.get("page") != pageNum:
            if pageNum != -1:
                pageList.append(newImage)

            pageNum = stroke.get("page")
            newImage = Image.new("RGB", (3840, 2160), "white")
            drawImage = ImageDraw.Draw(newImage)


            
        
        strokeSize = stroke.get("size")
        colour = stroke.get("colour")

        for coords in stroke.get("points"):
            x = coords[0] * widthScale
            y = coords[1] * heightScale

            drawImage.ellipse([x-strokeSize//2, y-strokeSize//2, x+strokeSize//2, y+strokeSize//2], fill=colour)

    return pageList
