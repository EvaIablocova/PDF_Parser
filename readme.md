PDF Parser Project
This project automates the process of downloading PDF files, parsing the data, and validating the results. It is designed to streamline workflows involving PDF data extraction and processing.

---

Requirements:
Python 3.13 or higher

---

Installation:

Clone the repository:
git clone https://github.com/EvaIablocova/PDF_Parser.git

---

Usage:

Run the entry point script to execute the workflow:

python 0_entry_point.py

The script will:
1. Install all dependencies.
2. Sequentially execute the following scripts:
1_download_pdf.py,
2_create_xlsx.py,
3_parser.py,
4_validation.py
3. Display the execution time for each script.

