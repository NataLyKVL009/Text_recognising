from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import magic

app = FastAPI()

# Путь к папке для загруженных файлов
UPLOAD_DIRECTORY = "./uploaded_files"

# проверить, что папка для загрузок существует
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Подключаем статическую папку для доступа к загруженным файлам
app.mount("/static", StaticFiles(directory=UPLOAD_DIRECTORY), name="static")


@app.get("/")
def main():
    content = """
    <body>
    <form action="/uploadfile/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # Читаем содержимое файла для определения его типа
    file_content = await file.read()

    # Используем magic для определения MIME-типа
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file_content)

    # Проверяем, что MIME-тип файла является изображением или PDF
    if not (file_mime_type.startswith("image/") or file_mime_type == "application/pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image or PDF")

    # Сохраняем файл на сервере
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(file_content)

    html_content = f"""
    <html>
    <body>
    <h1>Uploaded File: {file.filename}</h1>
    """

    # Если файл изображение, отображаем его
    if file_mime_type.startswith("image/"):
        html_content += f'<img src="/static/{file.filename}" alt="Image" />'
    else:
        html_content += f'<p>Uploaded PDF: <a href="/static/{file.filename}">{file.filename}</a></p>'

    html_content += """
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)
