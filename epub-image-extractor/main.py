import uvicorn
import ebooklib
from ebooklib import epub
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging

import ebooklib
import os

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

def get_image_from_ebook(book_path: str):
    book_images = []
    
    book = epub.read_epub(book_path)

    # TODO
    # Create UUID path for output_dir
    output_dir = "/tmp/epub-image-extractor/{}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        image_path = os.path.join(output_dir, image.get_name())
        with open(image_path, "wb") as img_file:
            img_file.write(image.get_content())
        book_images.append(image_path)
        logging.debug(f"Image saved: {image_path}")

    return

@app.get('/', response_class=HTMLResponse)
async def render_upload_page(request: Request):
    return templates.TemplateResponse(request=request, name='upload.jinja', status_code=200)

@app.post('/upload')
async def extract_image_from_book(epub_file: UploadFile = Form(...)):
    book_file_location = f"/tmp/{epub_file.filename}"
    with open(book_file_location, "wb") as file:
        file.write(await epub_file.read())
    
    get_image_from_ebook(book_file_location)
    return {'filename': epub_file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)