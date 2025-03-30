import logging
import os
import uuid
import zipfile

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

import ebooklib
from ebooklib import epub

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

def get_image_from_ebook(book_metadata: dict):
    book_images = []
    
    book = epub.read_epub(book_metadata.get('book_dir'))
    folder_name = str(uuid.uuid4())
    output_dir = f"/tmp/epub_image_extractor/extracted_images/{folder_name}/"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # TODO: Add a check to see if the book is empty or not
    for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        image_name: str = image.get_name().split('/').pop()
        image_path: str = os.path.join(output_dir, image_name)

        with open(image_path, "wb") as img_file:
            img_file.write(image.get_content())

        book_images.append(image_path)
        logging.debug(f"Image saved: {image_path}")

    # Create a ZIP file containing all extracted images
    zip_file_name = book_metadata.get('book_name')
    zip_file_path = f"/tmp/epub_image_extractor/extracted_images/{folder_name}/{zip_file_name}.zip"
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for image_path in book_images:
            zipf.write(image_path, os.path.basename(image_path))
            logging.debug(f"Image added to ZIP: {image_path}")

    logging.info(f"ZIP file created: {zip_file_path}")

    return

@app.get('/', response_class=HTMLResponse)
async def render_upload_page(request: Request):
    return templates.TemplateResponse(request=request, name='upload.jinja', status_code=200)

@app.post('/upload')
async def extract_image_from_book(epub_file: UploadFile = Form(...)):
    book_images_dir = "/tmp/epub_image_extractor/extracted_images/"
    book_dir = "/tmp/epub_image_extractor/books/"

    if not os.path.exists(book_images_dir) and not os.path.exists(book_dir):
        os.makedirs(book_images_dir, exist_ok=True)
    
    if not os.path.exists(book_dir):  
        os.makedirs(book_dir, exist_ok=True)
    
    book_metadata = {
        "book_dir": f"/tmp/epub_image_extractor/books/{epub_file.filename[:20] + str(uuid.uuid4())}",
        "book_name": epub_file.filename
    }
    
    with open(book_metadata.get("book_dir"), "wb") as file:
        file.write(await epub_file.read())
    
    get_image_from_ebook(book_metadata)
    
    return {'filename': epub_file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)