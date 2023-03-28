import io
import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, Request
from newpaddle import OCR, parsing
from paddleocr import PaddleOCR
import cv2
import base64
import skimage.io
from uuid import uuid4
import os
import numpy as np
import tensorflow as tf
from crop import cropp
from PIL import Image
from typing import List

def sharp(image):
    sharpen_filter = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-0]])
    sharped_img = cv2.filter2D(image, -1, sharpen_filter)
    return sharped_img

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
async def scan_image(in_files: List[UploadFile] = File(...)):
    out_res=[]
    for in_file in in_files:
        try:
            content = await in_file.read()  
            numpy_image = np.frombuffer(content, np.uint8)
            image = cv2.imdecode(numpy_image, cv2.IMREAD_COLOR)
            image = remove_alpha_channel(image)
            image=cropp(image)
            # image=sharp(image)
            cv2.imwrite(f"image_upload/{uuid4().hex}.jpg", image)
            list_of_words = OCR(image, ocr)
            print(list_of_words)
            final_results = parsing(list_of_words)
            print(final_results)
            out_res.append(final_results)
            
                    
        except Exception as e:
            print(e)
            # empty_directory("image_upload")
            # return {"error": str(e)}
    return {"res":out_res}
