import subprocess
import sys
import time

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirments"])

scripts = [
    "1_download_pdf.py",
    "2_create_xlsx.py",
    "3_parser.py",
    "4_clean.py",
    "5_validation.py",
    "6_load_sql.py"
]

for script in scripts:
    print(f"Running {script}...")
    start_time = time.time()
    result = subprocess.run([sys.executable, script])
    elapsed = time.time() - start_time
    if result.returncode != 0:
        print(f"Script {script} failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"{script} finished successfully in {elapsed:.2f} seconds.\n")