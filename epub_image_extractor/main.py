import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from epub_image_extractor.routes import router

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
