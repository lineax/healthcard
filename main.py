from fastapi import FastAPI
from fastapi import FastAPI, Request
from newpaddle import OCR, parsing
from paddleocr import PaddleOCR
import cv2
import base64
import skimage.io
from uuid import uuid4
import os
def decode(base64_string):
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")

    imgdata = base64.b64decode(base64_string)
    img = skimage.io.imread(imgdata, plugin='imageio')
    return img


def remove_alpha_channel(img):
    if img.shape[2] == 4:
        img = img[:, :, :3]
    return img

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='en',show_log = False)

if not os.path.exists("image_upload"):
    os.mkdir("image_upload")


@app.get("/")
async def root():
    return {"message": "Server is up and running!"}

@app.post("/scan")
async def scan_image(request:Request):
    
    try:

        json_input = await request.json()
        image_value = json_input['image']
        image_base64 = image_value.split(',')[1]
        image=decode(image_base64)
        
        image = remove_alpha_channel(image)
        cv2.imwrite(f"image_upload/{uuid4().hex}.jpg", image)
        list_of_words = OCR(image, ocr)
        final_results = parsing(list_of_words)
        return final_results
        
    except Exception as e:
        print(e)
        # empty_directory("image_upload")
        return {"error": str(e)}

