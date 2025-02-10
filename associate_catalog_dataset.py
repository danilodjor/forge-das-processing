import os
import pandas as pd
from datetime import datetime, timedelta

def find_matching_file(csv_path, folder_path):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Prepare a result dictionary
    result = []

    # Iterate over each row in the CSV
    for _, row in df.iterrows():
        # Parse the date and time from the CSV
        datetime_str = row[' Trig Date '].lstrip().rstrip() + ' ' + row['    Trig Time   '].lstrip().rstrip()
        csv_datetime = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S.%f") # local
        csv_datetime += timedelta(hours=7) # UTC = local + 6 hours
        
        # Initialize variables to store the best match
        closest_file = None
        closest_time = None

        # Iterate through the files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".h5"):
                # Extract the timestamp from the filename
                parts = filename.split("_")
                if len(parts) > 2:
                    file_datetime_str = parts[2].split("+")[0]  if len(parts) == 4 else parts[3].split('+')[0]
                    file_datetime = datetime.strptime(file_datetime_str, "%Y%m%dT%H%M%S") # UTCåß

                    # Check if this file is earlier than the CSV time and is closer than the current best match
                    if file_datetime <= csv_datetime and (closest_time is None or file_datetime > closest_time):
                        closest_time = file_datetime
                        closest_file = filename

        # Append the match to the result list
        if closest_file:
            result.append({" Trig Date ": row[" Trig Date "], "Trig Time": row["    Trig Time   "], "Matched File": closest_file})
        else:
            result.append({" Trig Date ": row[" Trig Date "], "Trig Time": row["    Trig Time   "], "Matched File": None})

    # Convert the result to a DataFrame and save or return
    result_df = pd.DataFrame(result)
    return result_df

# Example usage
csv_path = "/scratch/ddordevic/FORGE/GES16Aand16BStimulationMonitoringApril2024/16BStimulationCatalogues/FORGE16BApril24NetworkStage 3.csv"
folder_path = "/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v1.0.0/"
result_df = find_matching_file(csv_path, folder_path)
result_df.to_csv('test3.csv', index=False)