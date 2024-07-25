import fastapi
from fastapi import FastAPI, File, UploadFile, HTTPException, Form

from fastapi.responses import StreamingResponse

from enum import Enum
import os
import Text

app = FastAPI(
    title="Text Extraction API",
    description="API для извлечения текста из изображений и PDF файлов",
    version="1.0.0"
)


class SupportedLanguages(str, Enum):
    eng = "eng"
    rus = "rus"
    eng_rus = "eng+rus"


@app.post("/extract-text", summary="Извлечение текста из файла", tags=["Text Extraction"])
async def extract_text(
        file: UploadFile = File(...),
        languages: SupportedLanguages = Form(SupportedLanguages.eng_rus)

):
    content = await file.read()
    file_type = file.content_type
    pict = Text.TextTransformer(content)

    if file_type == "application/pdf":
        text = pict.process_file(file_type)
        response = {'file_type': 'PDF', 'content': text}

    elif file_type.startswith("image/"):
        text = pict.process_file(file_type, languages)
        response = {'file_type': 'IMAGE', 'content': text}

    else:
        raise HTTPException(status_code=400, detail="Uploaded file is not an image or PDF")

    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
