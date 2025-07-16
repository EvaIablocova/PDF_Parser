import subprocess
import sys
import time
import json
import os
import importlib
date_module = importlib.import_module('0_2_date')
write_to_log_module = importlib.import_module('0_3_write_to_log')

def check_config(file_config, file_to_process):
    if 'Init_lichid_' in file_to_process:
        file_config ['sizes']= [
                0,
                60,
                105,
                170,
                370,
                600
            ]
    else:
        file_config ['sizes'] = [
            0,
            60,
            120,
            200,
            470,
            820
        ]
    return file_config

# subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirments"])


with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

download_dir = config['download_dir']
config_dates = config["config_last_dates_in_db"]
today_file = config["today_file"]

# subprocess.run([sys.executable, "1_load_dates_from_site.py", today_file], env=os.environ)

# for changing dates
subprocess.run([sys.executable, "once_create_json_with_dates.py"])

# files_to_process = ["Lichidarea.pdf", "Lichidarea_term_exp.pdf"
# ,"Sediul.pdf", "Reducere.pdf",
# "Init_lichid_2014_2024_MO.pdf",
# "Denumirea.pdf", "Denumirea_2008_2024.pdf",
# "Finaliz_proced_reorg.pdf","Finaliz_proced_reorg_2021_2024.pdf",
#                     "Inactive.pdf", "Init_reorg.pdf"]

# files_to_process=["Lichidarea.pdf", "Lichidarea_term_exp.pdf", "Lichidarea_2008_2024.pdf", "Lichidarea_term_exp_2018_2024.pdf"]

files_to_process = ["Sediul_2008_2024_1.pdf"]

# files_to_process = date_module.compare_dates(config_dates, today_file)

if files_to_process:
    print("Dates changed. Files to process: ", files_to_process)
else:
    print("No files to process because dates have not changed.")
    sys.exit(0)


files_to_process_str = ','.join(files_to_process)

write_to_log_module.write_step_message("Py.Loader", f"Identified {len(files_to_process)} files to be loaded: {files_to_process_str}")
result = subprocess.run([sys.executable, "2_download_changed_pdf.py", download_dir, files_to_process_str], env=os.environ)

keywords = [fc['keyword'] for fc in config['file_configs'] if any(fc['keyword'] in os.path.splitext(file)[0] for file in files_to_process)]

print("keywords: ", keywords)

missing_keywords = [file for file in files_to_process if not any(fc['keyword'] in os.path.splitext(file)[0] for fc in config['file_configs'])]

if missing_keywords:
    print("Parsing settings have not been found for the following files:")
    for file in missing_keywords:
        print(f"- {file}")
else:
    print("Parsing settings have been found for all files.")

if not keywords:
    print("No parsing settings found for the provided files.")
    sys.exit(0)

for keyword in keywords:
    print(f"\n{'*' * 50}")
    print(f"Processing keyword: {keyword}")
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    file_config = next((fc for fc in config['file_configs'] if fc['keyword'] == keyword), None)
    os.environ['FILE_CONFIG'] = json.dumps(file_config)

    files_to_process_keyword = [file for file in files_to_process if keyword in file]

    for file_to_process in files_to_process_keyword:

        print(f"\n{'*' * 50}")
        print(f"Processing file: {file_to_process}")

        if keyword == 'Init_lichid':
            file_config = check_config(file_config, file_to_process)
            os.environ['FILE_CONFIG'] = json.dumps(file_config)

        path_to_file = os.path.join(download_dir, file_to_process)
        os.environ['path_to_file'] = json.dumps(path_to_file)

        scripts = [
            "3_1_parser.py",
            "4_clean.py",
            "5_load_sql.py",
            "6_pdf_into_archive.py",
            "7_change_dates_in_config.py",
            "8_call_job.py",
        ]

        for script in scripts:
            print(f"Running {script}...")
            start_time = time.time()
            result = subprocess.run([sys.executable, script, keyword], env=os.environ)
            elapsed = time.time() - start_time
            if result.returncode != 0:
                print(f"Script {script} failed with exit code {result.returncode}")
                sys.exit(result.returncode)
            print(f"{script} finished successfully in {elapsed:.2f} seconds.\n")




