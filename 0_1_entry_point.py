import subprocess
import sys
import time
import json
import os
import importlib
date_module = importlib.import_module('0_2_date')

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirments"])

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

download_dir = config['download_dir']

# result = subprocess.run([sys.executable, "0_1_1_download_all_pdf.py", download_dir], env=os.environ)


# files_to_process = [file for file in os.listdir(download_dir) if file.endswith(".pdf")]
files_to_process = "Lichidarea.pdf"
# files_to_process = "Init_reorg.pdf"
# files_to_process = "Init_lichid.pdf"
# files_to_process = "Finaliz_proced_reord.pdf"

print("files_to_process: ", files_to_process)

keywords = [fc['keyword'] for fc in config['file_configs'] if fc['keyword'] in [os.path.splitext(file)[0] for file in files_to_process]]

print("keywords: ",keywords)

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

        path_to_file = os.path.join(download_dir, file_to_process)
        os.environ['path_to_file'] = json.dumps(path_to_file)

        # is_data_changed = date_module.check_data_change(file_config)
        is_data_changed = True

        if not is_data_changed:
            print("Data has not changed, skipping the pipeline.")
            continue
        else:
            print("Data has changed, proceeding with the pipeline.")


        scripts = [
            # "0_1_1_download_all_pdf.py",
            "2_parser.py",
            "3_clean.py",
            "4_validation.py",
            "5_load_sql.py"
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




