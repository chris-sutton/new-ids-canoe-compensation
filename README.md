# New IDs CANOE Compensation Pipeline

This is a Python data pipeline for managing new CANOE compensation IDs, fetching records from REDCap, processing them, and writing results back. It’s designed to run nightly via a cronjob.

## Installation Instructions

Follow these steps to set up and run the pipeline from the latest release:

- **Download the Latest Release**  
  Go to the [Releases page](https://github.com/chris-sutton/new-ids-canoe-compensation/releases) and download the latest `runtime-vX.Y.Z.zip` file (e.g., `runtime-v0.2.4.zip`).

- **Unzip the Release**  
  Extract the zip file to your desired directory (e.g., `/path/to/app`):
  ```bash
  unzip runtime-vX.Y.Z.zip -d /path/to/app
  ```
  This creates a folder with `requirements.txt`, `src/` (containing `main.py`, `error_handler.py`, `redcap_functions.py`, and `__init__.py`), and an `install.sh` script.

- **Manual Setup**  
  If you prefer to set it up manually:
  1. Navigate to the project directory:
     ```bash
     cd /path/to/app
     ```
  2. Create a virtual environment with Python 3.13:
     ```bash
     python3.13 -m venv venv
     ```
  3. Activate the virtual environment:
     - On Linux/macOS:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
  4. Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```
  5. Create a `.env` file in `/path/to/app/` with:
     ```
     C2G_TOKEN=your_c2g_token
     CVU_TOKEN=your_cvu_token
     COMPENSATION_TOKEN=your_compensation_token
     ERROR_TOKEN=your_error_token
     API_URL=https://redcap.your-institution.org/api/
     ```
     Replace the placeholders with your REDCap tokens and API URL.
  6. Test the pipeline:
     ```bash
     python src/main.py
     ```
     Check `log.txt` for output.

- **Automated Setup**  
  For a quicker setup, use the included `install.sh` script:
  1. Navigate to the project directory:
     ```bash
     cd /path/to/app
     ```
  2. Run the script:
     ```bash
     ./install.sh
     ```
     This creates a Python 3.13 virtual environment, installs dependencies from `requirements.txt`, and generates a `.env` template if one doesn’t exist. Edit `.env` with your REDCap credentials as prompted.
  3. Test it:
     ```bash
     source venv/bin/activate
     python src/main.py
     ```

- **Running Nightly**  
  To schedule the pipeline to run at midnight every day, set up a cronjob (Linux/macOS example):
  ```bash
  crontab -e
  ```
  Add this line:
  ```bash
  0 0 * * * /path/to/app/venv/bin/python /path/to/app/src/main.py >> /path/to/app/log.txt 2>&1
  ```

If you encounter issues, open an issue on this repo or contact the maintainers.
```

---

### Notes on Automation
- **Workflow Integration**: The `install.sh` script is already included in the `runtime-vX.Y.Z.zip` via the updated workflow from my last response. When you push a new commit (e.g., `fix: update readme`), the release will contain:
  ```
  runtime-vX.Y.Z/
  ├── install.sh
  ├── requirements.txt
  └── src/
      ├── __init__.py
      ├── error_handler.py
      ├── main.py
      └── redcap_functions.py
  ```
