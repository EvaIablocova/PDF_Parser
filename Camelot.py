import camelot
import pandas as pd

file_path = "downloaded_pdf_files/Finaliz_proced_reorg_2021_2024.pdf"
output_file = "parsed_files/combined_table_output.csv"

tables = camelot.read_pdf(file_path, pages='all', flavor='lattice')

print(f"Found tables: {tables.n}")
#
# if tables.n > 0:
#     combined_df = pd.concat([table.df for table in tables], ignore_index=True)
#     combined_df.to_csv(output_file, sep='|', index=False, header=False)
#     print(f"All tables saved into {output_file}")
# else:
#     print("Tables not found in the PDF.")




for i, table in enumerate(tables):
    table.to_csv(f"table_{i+1}.csv")


