import os
import json

data = [
    {"FileName": "Denumirea.pdf", "start_date": "2025-01-11", "end_date": "2025-06-27"},
    {"FileName": "Denumirea_2008_2024.pdf", "start_date": "2008-06-02", "end_date": "2024-12-31"},
    {"FileName": "Sediul.pdf", "start_date": "2025-01-01", "end_date": "2025-06-27"},
    {"FileName": "Sediul_2008_2024.pdf", "start_date": "2008-06-01", "end_date": "2024-12-31"},
    {"FileName": "Inactive.pdf", "start_date": "2008-06-01", "end_date": "2025-06-27"},
    {"FileName": "Lichidarea.pdf", "start_date": "2025-01-02", "end_date": "2025-06-27"},
    {"FileName": "Lichidarea_2008_2024.pdf", "start_date": "2008-06-01", "end_date": "2024-12-31"},
    {"FileName": "Lichidarea_term_exp.pdf", "start_date": "2025-01-01", "end_date": "2025-06-27"},
    {"FileName": "Lichidarea_term_exp_2018_2024.pdf", "start_date": "2018-01-01", "end_date": "2024-12-31"},
    {"FileName": "Reducere.pdf", "start_date": "2025-01-01", "end_date": "2025-06-27"},
    {"FileName": "Reducere_2007_2024.pdf", "start_date": "2007-11-20", "end_date": "2024-12-31"},
    {"FileName": "Init_reorg.pdf", "start_date": "2025-01-01", "end_date": "2025-06-27"},
    {"FileName": "Init_reorg_2014_2024_MO.pdf", "start_date": "2014-06-27", "end_date": "2024-12-31"},
    {"FileName": "Init_lichid.pdf", "start_date": "2025-09-01", "end_date": "2025-06-27"},
    {"FileName": "Init_lichid_2014_2024_MO.pdf", "start_date": "2014-06-27", "end_date": "2024-12-31"},
    {"FileName": "Finaliz_proced_reorg.pdf", "start_date": "2025-01-01", "end_date": "2025-06-04"},
    {"FileName": "Finaliz_proced_reorg_2021_2024.pdf", "start_date": "2021-01-02", "end_date": "2024-12-31"},
]

output_file = "config_last_dates_in_db.json"

# Save the data to a JSON file
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Data written to {output_file}")