from PyPDF2 import PdfReader, PdfWriter


def extract_one_page(input_pdf_path, output_pdf_path):
    pdf_reader = PdfReader(input_pdf_path)

    if len(pdf_reader.pages) == 0:
        print("PDF-файл пустой.")
        return

    pdf_writer = PdfWriter()

    # pdf_writer.add_page(pdf_reader.pages[4])



    for index in [44]:
        if 0 <= index < len(pdf_reader.pages):
            pdf_writer.add_page(pdf_reader.pages[index])
        else:
            print(f"Page index {index} is out of range.")


    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"One page saved into {output_pdf_path}")


input_pdf = "archive/20250727_1359_Denumirea_2008_2024.pdf"
output_pdf = "files_to_parse/20250727_1359_Denumirea_2008_2024_1.pdf"
extract_one_page(input_pdf, output_pdf)