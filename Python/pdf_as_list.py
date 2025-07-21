from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTPage, LTItem, LTContainer, LTLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

INPUT_FILE_PATH = "downloaded_pdf_files/Finaliz_proced_reorg.pdf"

def print_horizontal_lines(indent: str, layout_item: LTItem, found_lines: list) -> None:
    if isinstance(layout_item, LTLine):
        # Горизонтальная линия, если разница по Y мала, а по X значительная
        if abs(layout_item.y0 - layout_item.y1) < 1 and abs(layout_item.x1 - layout_item.x0) > 10:
            print(f"x0={layout_item.x0}, y0={layout_item.y0}, x1={layout_item.x1}, y1={layout_item.y1}")
            found_lines.append(True)

    if isinstance(layout_item, LTContainer):
        for child in layout_item:
            print_horizontal_lines(indent + "--", child, found_lines)

def print_layout(page_layout: LTPage) -> None:
    found_lines = []
    print_horizontal_lines('', page_layout, found_lines)
    if not found_lines:
        print("Горизонтальные линии не найдены.")

def main():
    input_file_path = input("Введите путь к файлу PDF или нажмите Enter "
                            f"(по умолчанию будет прочитан файл \"{INPUT_FILE_PATH}\"): ") or INPUT_FILE_PATH

    with open(input_file_path, 'rb') as f:
        # Парсер, который будет разбирать основную структуру файла
        parser = PDFParser(f)
        # Документ, в который парсер будет складывать всю информацию
        doc = PDFDocument(parser)
        parser.set_document(doc)

        # Менеджер ресурсов
        resources_mgr = PDFResourceManager()
        # "Устройство" для внутреннего рендеринга объектов
        device = PDFPageAggregator(resources_mgr, laparams=LAParams())
        # Интерпретатор потока данных, который будет "рисовать" в контексте устройства
        interpreter = PDFPageInterpreter(resources_mgr, device)

        # Получаем первую страницу
        pages_iter = PDFPage.create_pages(doc)
        page0 = next(pages_iter)
        # Запускаем на ней интерпретатор и забираем отрендеренные объекты
        interpreter.process_page(page0)
        page_layout = device.get_result()
        # Распечатываем координаты горизонтальных линий
        print_layout(page_layout)

if __name__ == '__main__':
    main()