import os

from fastapi import UploadFile

from .helpers import generate_uuid_string


class EpubService:
    __BOOK_IMAGES_DIR = "/tmp/epub_image_extractor/extracted_images/"
    __BOOK_DIR = "/tmp/epub_image_extractor/books/"

    def __init__(self):
        EpubService.__create_storage_folders()
        self.book_storaged_file_name: str = ""
        self.book_original_file_name: str = ""

    @classmethod
    def __create_storage_folders(cls):
        """
        Create necessary directories for storing EPUB files and extracted images.
        """
        if not os.path.exists(cls.__BOOK_IMAGES_DIR):
            os.makedirs(cls.__BOOK_IMAGES_DIR, exist_ok=True)
    
        if not os.path.exists(cls.__BOOK_DIR):  
            os.makedirs(cls.__BOOK_DIR, exist_ok=True)

    

    async def save_ebook_file(self, epub_file: UploadFile):
        """
        Save the uploaded EPUB file to a temporary directory.
        """
        book_storage_folder = os.path.join(
            EpubService.__BOOK_DIR,
            generate_uuid_string()
        )

        with open(book_storage_folder, "wb") as file:
            file.write(await epub_file.read())