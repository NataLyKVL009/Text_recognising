from fastapi import FastAPI, File, UploadFile, HTTPException
import Text

app = FastAPI()


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    content = await file.read()
    pict = Text.TextTransformer(content)

    if file.content_type == "application/pdf":
        text = pict.extract_text_from_pdf()
        response = {'file_type': 'PDF', 'content': text}

    elif file.content_type.startswith("image/"):
        text = pict.extract_text_from_image()
        response = {'file_type': 'IMAGE', 'content': text}

    else:
        raise HTTPException(status_code=400, detail="Uploaded file is not an image or PDF")

    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
