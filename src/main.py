# main.py
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime
import os
from redcap_functions import fetch_redcap_records, write_to_redcap
from error_handler import write_error_to_redcap

# Load environment variables from .env file
load_dotenv()

# Retrieve the tokens and API URL from environment variables
c2g_token = os.getenv("C2G_TOKEN")
cvu_token = os.getenv("CVU_TOKEN")
cmp_token = os.getenv("COMPENSATION_TOKEN")
error_token = os.getenv("ERROR_TOKEN")
api_url = os.getenv("API_URL")

# Define the fields to be requested
fields = ["cfsubjid"]

try:
    # Fetch records from REDCap API
    base_c2g_records = fetch_redcap_records(api_url, c2g_token, fields)
    base_cvu_records = fetch_redcap_records(api_url, cvu_token, fields)
    base_cmp_records = fetch_redcap_records(api_url, cmp_token, fields)

    # Find records in base_c2g_records that do not exist in base_cmp_records
    unique_c2g_records = base_c2g_records[
        ~base_c2g_records["cfsubjid"].isin(base_cmp_records["cfsubjid"])
    ]

    # Find records in base_cvu_records that do not exist in base_cmp_records
    unique_cvu_records = base_cvu_records[
        ~base_cvu_records["cfsubjid"].isin(base_cmp_records["cfsubjid"])
    ]

    # Combine unique records from both DataFrames
    combined_unique_records = pd.concat([unique_c2g_records, unique_cvu_records])

    # Check if combined_unique_records contains any records
    if not combined_unique_records.empty:
        # Write the combined unique records to REDCap
        success, count = write_to_redcap(api_url, cmp_token, combined_unique_records)

        # Log the result to log.txt
        with open("log.txt", "a") as log_file:
            log_file.write(
                f"{datetime.now()}, {count} new records found, Write success: {success}\n"
            )
    else:
        # Log the result to log.txt with zero new records found
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}, 0 new records found, Write success: False\n")

except Exception as e:
    # Handle errors by logging them to REDCap
    write_error_to_redcap(
        url=api_url,
        token=error_token,
        fname="main.py",
        projectsystem="CANOE Compensation",
        actualerrormsg=str(e)
    )