import pytesseract
from PIL import Image
import fitz
import io
import re
import nltk
from nltk.stem import WordNetLemmatizer


nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()


class TextTransformer:

    def __init__(self, file_bytes):
        self.file_bytes = file_bytes

    def extract_text_from_image(self, lang="eng+rus"):
        image = Image.open(io.BytesIO(self.file_bytes))
        text = pytesseract.image_to_string(image, lang)
        return text

    def extract_text_from_pdf(self):
        text = ''
        pdf_document = fitz.open(stream=self.file_bytes, filetype="pdf")
        for page in pdf_document:
            text += page.get_text()
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
            text = self.extract_text_from_pdf()
        elif file_type.startswith("image/"):
            text = self.extract_text_from_image(languages)
        else:
            raise ValueError("Unsupported file type")

        cleaned_text = self.clean_text(text)

        return cleaned_text
