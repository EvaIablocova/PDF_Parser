# PDF Parser Pipeline

## Overview
This project automates the processing of data files, including downloading PDFs, parsing, cleaning, validating, and loading data into SQL databases. It uses Python scripts and a configuration file (`config.json`) to manage the pipeline.

## Features
- **Dynamic Configuration**: Uses `config.json` to manage file-specific settings.
- **Keyword Processing**: Processes data based on predefined keywords.
- **Change Detection**: Checks if data has changed before running the pipeline.
- **Modular Scripts**: Executes individual scripts for each stage of the pipeline.

## Requirements
- Python 3.x

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

## Usage
1. Ensure config.json is properly configured with file_configs for each keyword.
2. Run the entry point script:
    ```bash
    python 0_1_entry_point.py
   
## Scripts
- **1_download_pdf.py**: Downloads PDF files.
- **2_parser.py**: Parses the downloaded files.
- **3_clean.py**: Cleans the parsed data.
- **4_validation.py**: Validates the cleaned data.
- **5_load_sql.py**: Loads the validated data into an SQL database.

## Configuration
The config.json file contains settings for each keyword (file).