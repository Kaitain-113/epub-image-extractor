import os
import zipfile

from ebooklib import ITEM_IMAGE, epub
from fastapi import UploadFile

from .helpers import generate_uuid_string


class EpubService:
    __BOOK_IMAGES_DIR = 'storage/extracted_images/'
    __BOOK_DIR = 'storage/books/'
    __COMPRESSED_FILE_TYPE_HEADER = {
        'zip': 'application/zip',
    }

    def __init__(self):
        EpubService.__create_storage_folders()
        self.book_storaged_file_path: str = ''
        self.book_original_file_name: str = ''
        self.output_images_dir_name: str = generate_uuid_string()

    @classmethod
    def __create_storage_folders(cls) -> None:
        """
        Create necessary directories for storing EPUB files and extracted images.
        """
        if not os.path.exists(cls.__BOOK_IMAGES_DIR):
            os.makedirs(cls.__BOOK_IMAGES_DIR, exist_ok=True)

        if not os.path.exists(cls.__BOOK_DIR):
            os.makedirs(cls.__BOOK_DIR, exist_ok=True)

    async def save_ebook_file(self, epub_file: UploadFile) -> None:
        """
        Save the uploaded EPUB file to a temporary directory.
        """
        self.book_original_file_name = epub_file.filename
        self.book_storaged_file_path = os.path.join(
            EpubService.__BOOK_DIR, generate_uuid_string(self.book_original_file_name)
        )

        with open(self.book_storaged_file_path, 'wb') as file:
            file.write(await epub_file.read())

    def get_image_from_ebook(self, compressed_file_extension='zip') -> dict[str, str]:
        book_images = []
        compressed_file_name = (
            f'{self.book_original_file_name}.{compressed_file_extension}'
        )
        compressed_file_type_header = EpubService.__COMPRESSED_FILE_TYPE_HEADER.get(
            compressed_file_extension
        )
        images_dir = os.path.join(
            EpubService.__BOOK_IMAGES_DIR, self.output_images_dir_name
        )

        book = epub.read_epub(self.book_storaged_file_path)

        if not os.path.exists(images_dir):
            os.makedirs(images_dir, exist_ok=True)

        for image in book.get_items_of_type(ITEM_IMAGE):
            image_name: str = image.get_name().split('/').pop()
            image_path: str = os.path.join(images_dir, image_name)

            with open(image_path, 'wb') as img_file:
                img_file.write(image.get_content())

            book_images.append(image_path)

        compressed_file_path = f'{images_dir}/{compressed_file_name}'

        with zipfile.ZipFile(compressed_file_path, 'w') as zipf:
            for image_path in book_images:
                zipf.write(image_path, os.path.basename(image_path))

        return {
            'file_name': compressed_file_name,
            'compressed_file_path': compressed_file_path,
            'filetype_header': compressed_file_type_header,
        }
