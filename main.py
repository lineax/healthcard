from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse 
from fastapi.responses import HTMLResponse



app = FastAPI()


templates = Jinja2Templates(directory="htmldirectory")
@app.get("/")
async def root():
    return FileResponse('./htmldirectory/index.html')

@app.post("/scan")
async def scan_image():
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
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/capture")
async def scan_image():
    html_content = f"""
                    <html>
                        <head>
                            <title>Results</title>
                        </head>
                        <body>
                            <h1>"{"Capturing Image"}"</h1>
                        </body>
                    </html>
                    """
       
        
            # return FileResponse('./htmldirectory/df_representation.html')
    return HTMLResponse(content=html_content, status_code=200)



@app.post("/upload")
async def scan_image():
    html_content = f"""
                    <html>
                        <head>
                            <title>Results</title>
                        </head>
                        <body>
                            <h1>"{"Uploading Image"}"</h1>
                        </body>
                    </html>
                    """
       
        
            # return FileResponse('./htmldirectory/df_representation.html')
    return HTMLResponse(content=html_content, status_code=200)