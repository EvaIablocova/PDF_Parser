import subprocess
import sys
import time
import json
import os
import importlib
date_module = importlib.import_module('0_2_date')

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirments"])

keywords = ["Denumirea",
            "Denumirea_2008_2024",
            "Sediul",
            "Sediul_2008_2024",
            "Inactive",
            "Reducere",
            "Reducere_2007_2024",]

for keyword in keywords:
    print(f"Processing keyword: {keyword}")
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    file_config = next((fc for fc in config['file_configs'] if fc['keyword'] == keyword), None)
    os.environ['FILE_CONFIG'] = json.dumps(file_config)



    is_data_changed = date_module.check_data_change(file_config)

    if not is_data_changed:
        print("Data has not changed, skipping the pipeline.")
        continue
    else:
        print("Data has changed, proceeding with the pipeline.")


    scripts = [
        "1_download_pdf.py",
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




