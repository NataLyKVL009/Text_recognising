import pdfplumber
import pandas as pd
import re


# Функция для извлечения текста из PDF
def extract_text_from_pdf(pdf_path):
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:  # Проверяем, что таблица не пустая
                for row in table:
                    if any(row):  # Проверяем, что строка не пустая
                        text_data.append(row)
    return text_data


# Функция для очистки и нормализации строк
def clean_string(s):
    return " ".join(s.strip().split())


# Функция для сопоставления заголовков с учетом различных форм написания
def normalize_header(header):
    header = header.replace("\n", " ").replace("\r", "").strip()
    header = re.sub(r'\s+', ' ', header)
    return header


# Функция для обработки данных и создания словаря
def process_data(text_data):
    # Сопоставление имен ячеек в PDF и имен на выходе
    mapping = {
        "NAME OF PROVIDER OR SUPPLIER": "Facility Name",
        "STREET ADDRESS, CITY, STATE, ZIP COD": "Facility Address",
        "(X1) PROVIDER/SUPPLIER/CLIA": "Facility ID #",
        "(X3) DATE SURVEY COMPLETED": "Deficiency Citation",
        "ID PREFIX TAG": "Category Citation",
        "SUMMARY STATEMENT OF DEFICIENCIE (EACH DEFICIENCY MUST BE PRECEDED BY FULL REGULATORY OR LSC IDENTIFYING "
        "INFORMATION": "Reason for Citation",
        "(X5)COMPLETION DATE": "Correction Action"
    }

    data_dict = {
        "Facility Name": "",
        "Facility Address": "",
        "Facility ID #": "",
        "Deficiency Citation": "",
        "Category Citation": "",
        "Reason for Citation": "",
        "Correction Action": ""
    }

    last_key = None  # Переменная для отслеживания последнего найденного заголовка

    for row in text_data:
        if row is None:  # Проверяем, что строка не None
            continue
        for cell in row:
            if not cell:
                continue

            cleaned_cell = clean_string(cell)
            normalized_cell = cleaned_cell.replace("\n", " ").replace("  ", " ")
            found_key = False

            for pdf_key, output_key in mapping.items():
                normalized_pdf_key = pdf_key.replace("\n", " ").replace("  ", " ")
                if normalized_pdf_key in normalized_cell:
                    last_key = output_key
                    data_dict[output_key] = normalized_cell.replace(normalized_pdf_key, "").strip()
                    found_key = True
                    break

            if not found_key and last_key:
                data_dict[last_key] += " " + cleaned_cell.strip()
                last_key = None

    return data_dict


# Функция для сохранения данных в Excel
def save_to_excel(data_list, output_path):
    df = pd.DataFrame(data_list)
    df.to_excel(output_path, index=False)


# Пример использования
pdf_path = "source/2567 Example for data extraction Columbia.pdf"
output_path = "output.xlsx"

text_data = extract_text_from_pdf(pdf_path)

# Изменение: собираем данные со всех страниц
all_data = []
for page_data in text_data:
    if page_data:  # Проверяем, что данные не пустые
        processed_data = process_data([page_data])
        all_data.append(processed_data)

save_to_excel(all_data, output_path)

print(f"Данные сохранены в {output_path}")
