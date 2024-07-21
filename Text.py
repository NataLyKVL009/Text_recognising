import pytesseract
from PIL import Image
import fitz
import io


class TextTransformer:
    def __init__(self, file_bytes):
        self.file_bytes = file_bytes

    def extract_text_from_image(self):
        image = Image.open(io.BytesIO(self.file_bytes))
        text = pytesseract.image_to_string(image, lang='rus')
        return text

    def extract_text_from_pdf(self):
        text = ""
        pdf_document = fitz.open(stream=self.file_bytes, filetype="pdf")
        for page in pdf_document:
            text += page.get_text()
        return text
