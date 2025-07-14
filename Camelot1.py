import camelot
import cv2
import pdfplumber
import numpy as np

# Загружаем таблицы с Camelot
tables = camelot.read_pdf("downloaded_pdf_files/Finaliz_proced_reorg_2021_2024.pdf", pages="1", flavor="lattice")

image = tables[0].get_pdf_image()

# Преобразуем в OpenCV-формат (grayscale)
image_cv = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Бинаризация изображения
_, thresh = cv2.threshold(image_cv, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Морфологический фильтр для выделения горизонтальных линий
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
horizontal_lines_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

# Поиск контуров
contours, _ = cv2.findContours(horizontal_lines_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Получаем высоту страницы PDF
with pdfplumber.open("downloaded_pdf_files/Finaliz_proced_reorg_2021_2024.pdf") as pdf:
    page_height = pdf.pages[0].height

# Преобразуем координаты из OpenCV в PDF-подобные
converted_coords = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    pdf_x0 = x
    pdf_y0 = page_height - (y + h)
    pdf_x1 = x + w
    pdf_y1 = page_height - y
    converted_coords.append((pdf_x0, pdf_y0, pdf_x1, pdf_y1))

# Вывод результата
print("📐 Преобразованные координаты для pdfplumber:")
for i, bbox in enumerate(sorted(converted_coords, key=lambda b: b[1], reverse=True), 1):
    print(f"{i}: {bbox}")
