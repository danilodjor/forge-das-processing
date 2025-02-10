import os
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

def update_csv_with_matching_file(csv_path, folder_path):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    if "Matched File" in df.columns:
        return None
    
    # Add a new column for matched files (initialize with None)
    df['Matched File'] = None

    # Iterate over each row in the CSV with tqdm progress bar
    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Processing {os.path.basename(csv_path)}"):
        # if type(row[' Trig Date ']) != str or type(row['    Trig Time   ']) != str or row.isna().any():
            # continue
        
        # Parse the date and time from the CSV
        datetime_str = row[' Trig Date '].strip() + ' ' + row['    Trig Time   '].strip()
        csv_datetime = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S.%f")  # Local time
        csv_datetime += timedelta(hours=6)  # Convert to UTC

        if csv_datetime < datetime(2024, 4, 7, 0, 0, 0):  # Skip rows before April 6, 2024
            continue 
        
        # Initialize variables to store the best match
        closest_file = None
        closest_time = None

        # Iterate through the files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".h5"):
                # Extract the timestamp from the filename
                parts = filename.split("_")
                if len(parts) > 2:
                    file_datetime_str = parts[2].split("+")[0] if len(parts) == 4 else parts[3].split('+')[0]
                    file_datetime = datetime.strptime(file_datetime_str, "%Y%m%dT%H%M%S")  # UTC

                    # Check if this file is earlier than the CSV time and is closer than the current best match
                    if file_datetime <= csv_datetime and (closest_time is None or file_datetime > closest_time):
                        closest_time = file_datetime
                        closest_file = filename

        # Update the DataFrame with the matched file
        df.at[idx, 'Matched File'] = closest_file

    # Save the updated CSV file
    df.to_csv(csv_path, index=False)

def process_all_csvs(csv_directory, folder_path):
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith(".csv") and f.startswith("FORGE")]
    
    # Process each CSV file with tqdm progress bar
    for csv_file in tqdm(csv_files, desc="Processing CSV files"):
        csv_path = os.path.join(csv_directory, csv_file)
        update_csv_with_matching_file(csv_path, folder_path)

# Example usage
csv_directory = "/scratch/ddordevic/FORGE/GES16Aand16BStimulationMonitoringApril2024/16BStimulationCatalogues/"
folder_path = "/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v1.0.0/"
process_all_csvs(csv_directory, folder_path)