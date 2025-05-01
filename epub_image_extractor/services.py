import os
import shutil

from ebooklib import ITEM_IMAGE, epub
from fastapi import UploadFile

from epub_image_extractor.helpers import (
    directory_creator,
    file_compressor,
    generate_uuid_string
)

class EpubService:
    __BOOK_IMAGES_DIR = 'storage/extracted_images/'
    __BOOK_DIR = 'storage/books/'

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
        directory_creator(cls.__BOOK_IMAGES_DIR)
        directory_creator(cls.__BOOK_DIR)

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

        images_dir = os.path.join(
            EpubService.__BOOK_IMAGES_DIR, self.output_images_dir_name
        )
        directory_creator(images_dir)

        book = epub.read_epub(self.book_storaged_file_path)

        for image in book.get_items_of_type(ITEM_IMAGE):
            image_name: str = image.get_name().split('/').pop()
            image_path: str = os.path.join(images_dir, image_name)

            with open(image_path, 'wb') as img_file:
                img_file.write(image.get_content())

            book_images.append(image_path)

        file_path, file_name, file_type_header = file_compressor(
            images_dir, book_images
        )

        return {
            'file_name': file_name,
            'compressed_file_path': file_path,
            'file_type_header': file_type_header,
        }

    def clean_up(self) -> None:
        """
        Delete temporary files and directories: book file and book images folder.
        """
        os.remove(self.book_storaged_file_path)

        images_dir = os.path.join(
            EpubService.__BOOK_IMAGES_DIR, self.output_images_dir_name
        )
        shutil.rmtree(images_dir, ignore_errors=True)
