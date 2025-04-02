import os

from fastapi import UploadFile 


class EpubService:
    __BOOK_IMAGES_DIR = "/tmp/epub_image_extractor/extracted_images/"
    __BOOK_DIR = "/tmp/epub_image_extractor/books/"

    def __init__(self):
        EpubService.__create_storage_folders()

    @classmethod
    def __create_storage_folders(cls):
        """
        Create necessary directories for storing EPUB files and extracted images.
        """
        if not os.path.exists(cls.__BOOK_IMAGES_DIR):
            os.makedirs(cls.__BOOK_IMAGES_DIR, exist_ok=True)
    
        if not os.path.exists(cls.__BOOK_DIR):  
            os.makedirs(cls.__BOOK_DIR, exist_ok=True)


