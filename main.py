from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from enum import Enum
from Text import TextTransformer
from pydantic import BaseModel, Field


class ExtractResponse(BaseModel):
    file_type: str = Field(..., example='PDF', description="Тип загруженного файла")
    content: str = Field(..., example='Большой документ', description="Извлечённый текст")


app = FastAPI(
    title="Text Extraction API",
    description="API для извлечения текста из изображений и PDF файлов",
    version="1.0.0"
)


class SupportedLanguages(str, Enum):
    eng = "eng"
    rus = "rus"
    eng_rus = "eng+rus"


@app.post("/extract-text", summary="Извлечение текста из файла", tags=["Text Extraction"],
          response_model=ExtractResponse
          )
async def extract_text(
        file: UploadFile = File(..., description='Файл pdf-формата или изображение с текстом'),
        languages: SupportedLanguages = Form(SupportedLanguages.eng_rus, description='Язык текта документа')

):
    content = await file.read()
    file_type = file.content_type
    pict = TextTransformer(content)
    text = pict.process_file(file_type, languages)

    if text:
        response = ExtractResponse(file_type='IMAGE', content=text)

    else:
        raise HTTPException(status_code=400, detail="Uploaded file is not an image or PDF")

    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
