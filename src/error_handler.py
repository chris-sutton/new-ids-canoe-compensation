import pandas as pd
from datetime import datetime
import requests
import json

def log_error(fname, projectsystem, actualerrormsg, failuremessage=""):
    # Create a DataFrame with the specified columns
    error_log = pd.DataFrame(columns=["fname", "projectsystem", "failuremessage", "failuredatetime", "actualerrormsg"])
    
    # Get the current date and time in the specified format
    failuredatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a dictionary with the error information
    error_info = {
        "record_id":1,
        "fname": fname,
        "projectsystem": projectsystem,
        "failuremessage": failuremessage,
        "failuredatetime": failuredatetime,
        "actualerrormsg": actualerrormsg
    }
    
    # Convert the dictionary to a DataFrame
    error_row = pd.DataFrame([error_info])
    
    # Concatenate the new row to the error_log DataFrame
    error_log = pd.concat([error_log, error_row], ignore_index=True)
    
    return error_log

def write_error_to_redcap(url, token, fname, projectsystem, actualerrormsg, failuremessage=""):
    # Log the error and get the DataFrame
    error_log = log_error(fname, projectsystem, actualerrormsg, failuremessage)
    
    # Convert the DataFrame to JSON format
    json_data = error_log.to_json(orient='records')
    
    # Create form data for the POST request
    form_data = {
        "token": token,
        "content": 'record',
        "action": 'import',
        "format": 'json',
        "type": 'flat',
        "overwriteBehavior": 'normal',
        "forceAutoNumber": 'true',
        "data": json_data,
        "returnContent": 'count',
        "returnFormat": 'json'
    }
    
    # Send the POST request to REDCap
    response = requests.post(url, data=form_data)
    
    # Check the response status and print the result
    if response.status_code == 200:
        print("Data successfully written to REDCap:", response.json())
    else:
        print("Failed to write data to REDCap:", response.text)

# Example usage
#try:
#    # Code that may raise an exception
#    raise ValueError("An example error occurred")
#except Exception as e:
#    write_error_to_redcap(
#        url="https://redcap.vumc.org/api/",
#        token="91FF6A9DC244FAB0CAF4888B4490AFA9",
#        fname="example_file.py",
#        projectsystem="ExampleProject",
#        actualerrormsg=str(e)
#    )