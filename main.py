import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse 
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Body, Request, Form
from fastapi import FastAPI, File, UploadFile
from newpaddle import OCR, parsing
from paddleocr import PaddleOCR
import io
import numpy as np
from PIL import Image

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='en',show_log = False)

@app.get("/")
async def root():
    return {"message": "Server is up and running!"}

@app.post("/scan")
async def scan_image(request:Request, file:UploadFile):
    
    # try:
        image_bytes = file.file.read()
        image = np.array(Image.open(io.BytesIO(image_bytes))) 
        list_of_words = OCR(image, ocr)
        final_results = parsing(list_of_words)
        # return FileResponse('./htmldirectory/df_representation.html')
        # empty_directory("image_upload")
        return final_results
    # except Exception as e:
    #     print(e)
    #     # empty_directory("image_upload")
    #     return {"error": str(e)}

