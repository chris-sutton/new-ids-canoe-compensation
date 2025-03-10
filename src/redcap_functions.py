# redcap_functions.py

import pandas as pd
import requests
import json


def write_to_redcap(api_url, token, df):
    # Convert DataFrame to JSON format
    records = df.to_dict(orient="records")
    data = {
        "token": token,
        "content": "record",
        "format": "json",
        "type": "flat",
        "overwriteBehavior": "normal",
        "data": json.dumps(records),
        "returnContent": "count",
        "returnFormat": "json",
    }

    # Make the POST request to REDCap API
    response = requests.post(api_url, data=data)

    # Check the response
    if response.status_code == 200:
        response_json = response.json()
        if "count" in response_json and response_json["count"] > 0:
            print("Data successfully written to REDCap!")
            return True, response_json["count"]
        else:
            print("Failed to write data to REDCap.")
            print(response_json)
            return False, 0
    else:
        print("HTTP Status: " + str(response.status_code))
        print(response.text)
        return False, 0


def fetch_redcap_records(api_url, token, fields, filter_logic=None):
    # Prepare the data for the POST request
    data = {
        "token": token,
        "content": "record",
        "action": "export",
        "format": "json",
        "type": "flat",
        "csvDelimiter": "",
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "false",
        "exportDataAccessGroups": "false",
        "returnFormat": "json",
    }

    # Add fields to the data object
    for i, field in enumerate(fields):
        data[f"fields[{i}]"] = field

    # Add filter logic if provided
    if filter_logic:
        data["filterLogic"] = filter_logic

    # Make the POST request to REDCap API
    r = requests.post(api_url, data=data)

    # Check if the request was successful
    if r.status_code == 200:
        # Load the response JSON into a DataFrame
        df = pd.DataFrame(r.json())

        return df
    else:
        print("HTTP Status: " + str(r.status_code))
        return None
