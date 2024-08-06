import pytesseract
from PIL import Image
import fitz
import io
import re
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('punkt')

lemmatizer = WordNetLemmatizer()

class TextTransformer:
    def __init__(self, file_bytes):
        self.file_bytes = file_bytes

    def extract_text_from_image(self, image_bytes, lang="eng+rus"):
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image, lang=lang)
        return text

    def extract_text_from_pdf(self, languages="eng+rus"):
        text = ''
        pdf_document = fitz.open(stream=self.file_bytes, filetype="pdf")
        for page in pdf_document:
            page_text = page.get_text()
            text += page_text  # Добавляем текст из текстового слоя
            # Также обрабатываем изображения на странице для OCR
            pix = page.get_pixmap()
            image_bytes = pix.tobytes(output='png')
            ocr_text = self.extract_text_from_image(image_bytes, languages)
            text += ocr_text
            text += '\n\n'
        return text

    @staticmethod
    def clean_text(text):
        # Удалить специальные символы
        text = re.sub(r'[^\w\s]', '', text)
        text = ' '.join(text.split())
        # Токенизация текста
        words = nltk.word_tokenize(text)
        # Лемматизация
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        cleaned_text = ' '.join(lemmatized_words)
        return cleaned_text

    def process_file(self, file_type, languages="eng+rus"):
        if file_type == "application/pdf":
            text = self.extract_text_from_pdf(languages)
        elif file_type.startswith("image/"):
            text = self.extract_text_from_image(self.file_bytes, languages)
        else:
            raise ValueError("Unsupported file type")

        cleaned_text = self.clean_text(text)
        return cleaned_text

