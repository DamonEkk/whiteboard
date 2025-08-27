from PIL import Image, ImageDraw


def render_strokes(history, canvasH, canvasW):
    pageList = []

    pageNum = -1
    heightScale = 2160 / canvasH
    widthScale = 3840 / canvasW
    strokeID = -1
        

    for stroke in history:
        flag = 0
        
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

            if flag == 1:
                drawImage.line([historyX+strokeSize//2, historyY+strokeSize//2, x+strokeSize//2, y+strokeSize//2], fill=colour, width=strokeSize)

            else:
                flag = 1
                drawImage.ellipse([x-strokeSize//2, y-strokeSize//2, x+strokeSize//2, y+strokeSize//2], fill=colour, width=strokeSize)  


            historyX = x
            historyY = y

    pageList.append(newImage)

    return pageList
