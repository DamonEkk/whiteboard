from PIL import Image, ImageDraw, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
from collections import defaultdict
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
bucket = "pictures-bucket-cab432-assignment"

def render_strokes(roomID, canvasH, canvasW):
    qutName = "n12197718@qut.edu.au"
    pdf_buffer = io.BytesIO()
    sizeH = 2160
    sizeW = 3840
    c = canvas.Canvas(pdf_buffer, pagesize=(sizeW, sizeH))
    scaleX = sizeW / canvasW
    scaleY = sizeH / canvasH
    scaleAvg = (scaleX + scaleY) / 2
    roomID = str(1)
    history = []
    
    try: # Pull all items from dynamodb table. 
        response = dynamodb.query(
            TableName="n12197718-whiteboard-strokes",
            KeyConditionExpression="#pk = :username",
            ExpressionAttributeNames={
                "#pk": "qut-username"
            },
            ExpressionAttributeValues={
                ":username": {"S": qutName}
            }
        )

        items = response.get("Items", [])
        if items:
            history = [{k: list(v.values())[0] for k, v in item.items()} for item in items]
        else:
            print("No strokes found for this user")

    except Exception as e:
        print(e) 

    pages = defaultdict(list)
    for stroke in history:
        pages[stroke.get("page")].append(stroke)

    pictures_prefix = f"pictures/{roomID}/"
    pdf_prefix = f"pdf/{roomID}/"

    # Clear folders for new items
    clear_folder(pictures_prefix)
    clear_folder(pdf_prefix)

    for pageNum in sorted(pages.keys()):
        img = Image.new("RGB", (sizeW, sizeH), "white")
        draw = ImageDraw.Draw(img)

        for stroke in pages[pageNum]:
            size = float(stroke.get("size"))
            colour = stroke.get("colour")
            width = int(size * scaleAvg)
            flag = 0

            # Normalize points from DynamoDB format
            points_raw = stroke.get("points", [])
            normalized_points = []
            for pt in points_raw:
                coords = pt.get("L", [])
                if len(coords) == 2:
                    x = float(coords[0]["N"])
                    y = float(coords[1]["N"])
                    normalized_points.append((x, y))

            for x0, y0 in normalized_points:
                x = x0 * scaleX
                y = y0 * scaleY

                if flag:
                    draw.line([hx, hy, x, y], fill=colour, width=width)
                else:
                    r = width // 2
                    draw.ellipse([x - r, y - r, x + r, y + r], fill=colour)
                    flag = 1
                hx, hy = x, y

        img = img.filter(ImageFilter.UnsharpMask(radius=5, percent=150, threshold=3))

        # Save each image.
        img_buf = io.BytesIO()
        img.save(img_buf, format="PNG")
        img_buf.seek(0)
        s3_key = f"{pictures_prefix}{pageNum}.png"
        s3.upload_fileobj(img_buf, bucket, s3_key)

    # Pull images from s3 and create the pdf
    for pageNum in sorted(pages.keys()):
        s3key = f"{pictures_prefix}{pageNum}.png"
        imgObj = s3.get_object(Bucket=bucket, Key=s3key)
        imgData = io.BytesIO(imgObj["Body"].read())
        img = Image.open(imgData)
        c.drawImage(ImageReader(img), 0, 0, width=sizeW, height=sizeH)
        c.showPage()

    # Save pdf and upload to s3
    c.save()
    pdf_buffer.seek(0)
    pdf_data = pdf_buffer.getvalue()
    pdf_s3_key = f"{pdf_prefix}untitled.pdf"
    s3.upload_fileobj(io.BytesIO(pdf_data), bucket, pdf_s3_key)

    return pdf_buffer



# Only want one copy of the items in s3 depending on the room. So we clear before adding them.
def clear_folder(foldername): # Takes in param like s3/pictures/-5748573
    respjson = s3.list_objects_v2(Bucket=bucket, Prefix=foldername)
    if "Contents" in respjson: # Checks if the folder is empty.
        for item in respjson["Contents"]:
            s3.delete_object(Bucket=bucket, Key=item["Key"]) # Delte items

