from fastapi import (
    APIRouter, 
    BackgroundTasks,
    Form,
    UploadFile,
    Request
)
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from epub_image_extractor.services import EpubService

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
async def render_upload_page(request: Request):
    return templates.TemplateResponse(
        request=request, name='upload.jinja', status_code=200
    )


@router.post('/upload')
async def extract_image_from_book(
    background_tasks: BackgroundTasks, epub_file: UploadFile = Form(...)
):
    epub_service = EpubService()
    await epub_service.save_ebook_file(epub_file)

    book_images_data: dict = epub_service.get_image_from_ebook(
        compressed_file_extension='zip'
    )

    background_tasks.add_task(epub_service.clean_up)

    return FileResponse(
        book_images_data.get('compressed_file_path'),
        filename=book_images_data.get('file_name'),
        media_type=book_images_data.get('file_type_header'),
    )