import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse 
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Body, Request, Form
from fastapi import FastAPI, File, UploadFile
from newpaddle import OCR, parsing
from paddleocr import PaddleOCR

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='en')


templates = Jinja2Templates(directory="htmldirectory")
@app.get("/")
async def root():
    return FileResponse('./htmldirectory/index.html')

@app.post("/scan")
async def scan_image(request:Request, file:UploadFile):
    if not os.path.isdir("./image_upload"):
        os.mkdir("./image_upload")
        
    file_name=str(file.filename)
    with open(f"./image_upload/{file_name}", "wb+") as file_object:
        file_object.write(file.file.read())
    file_path=f"./image_upload/{file_name}"
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
    os.remove(file_path)
    return final_results

