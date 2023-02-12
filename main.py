import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse 
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Body, Request, Form
from fastapi import FastAPI, File, UploadFile
from newpaddle import OCR, parsing
from paddleocr import PaddleOCR
from newpaddle import pdfconverter
from newpaddle import empty_directory

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='en')


templates = Jinja2Templates(directory="htmldirectory")
@app.get("/")
async def root():
    return FileResponse('./htmldirectory/index.html')

@app.post("/scan")
async def scan_image(request:Request, file:UploadFile):
    folder = "image-upload"
    if not os.path.isdir(f"./{folder}"):
        os.mkdir(f"./{folder}")
        
    file_name=str(file.filename)
    with open(f"./{folder}/{file_name}", "wb+") as file_object:
        file_object.write(file.file.read())
    file_path=f"./{folder}/{file_name}"
    if file_name.split(".")[1] == "pdf":
        pdfconverter(file_path, folder)
        os.remove(file_path)
        for image in os.listdir(f"./{folder}"):
            file_path = f'{folder}/{image}'

    try:
        list_of_words = OCR(file_path, ocr)
        final_results = parsing(list_of_words)

        html_content = f"""
                        <html>
                            <head>
                                <title>Results</title>
                            </head>
                            <body>
                                <h1>"{"Scanning Image"}"</h1>
                            </body>
                        </html>
                        """
        
        
            # return FileResponse('./htmldirectory/df_representation.html')
        empty_directory("image_upload")
        return final_results
    except:
        empty_directory("image_upload")
        return "INVALID IMAGE! TRY AGAIN PLEASE."

