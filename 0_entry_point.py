import subprocess
import sys
import time
import json
import os

keyword = "Inactive"

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

file_config = next((fc for fc in config['file_configs'] if fc['keyword'] == keyword), None)
os.environ['FILE_CONFIG'] = json.dumps(file_config)


subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirments"])

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