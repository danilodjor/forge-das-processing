import os
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

"""
DAS Data - Catalog Association Script

This script associates seismic catalog events with corresponding DAS data files based on 
temporal matching. It has been tested and validated on FORGE DAS HDF5 files from the 
Petabyte storage system.

File Format Compatibility:
- Primarily tested with HDF5 (.h5) files from FORGE Petabyte storage
- Also applicable to SEGY files, provided they follow the same naming convention:
  Format: "16B_StrainRate_YYYYMMDDTHHMMSS+0000_NNNNN.[h5|segy]"
  
Usage Notes:
- Tested on Utah FORGE April 2024 dataset
- Handles timezone conversion (local time + 6 hours = UTC)
- Finds the closest DAS file timestamp that precedes each seismic event

Author: Danilo Dordevic
Last Updated: August 2025
"""


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
        # Note: This logic works for both HDF5 and SEGY files with the same naming convention
        for filename in os.listdir(folder_path):
            if filename.endswith(".h5") or filename.endswith(".segy"):  # Support both HDF5 and SEGY formats
                # Extract the timestamp from the filename
                # Expected format: 16B_StrainRate_YYYYMMDDTHHMMSS+0000_NNNNN.[h5|segy]
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
    """
    Process all FORGE CSV catalog files in a directory and associate them with DAS data files.
    
    Parameters:
    csv_directory (str): Directory containing FORGE*.csv catalog files
    folder_path (str): Directory containing DAS data files (HDF5 or SEGY format)
    
    Note: This function has been tested with FORGE Petabyte storage HDF5 files
    and is compatible with SEGY files using the same naming convention.
    """
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith(".csv") and f.startswith("FORGE")]

    # Process each CSV file with tqdm progress bar
    for csv_file in tqdm(csv_files, desc="Processing CSV files"):
        csv_path = os.path.join(csv_directory, csv_file)
        update_csv_with_matching_file(csv_path, folder_path)

# Example usage
# Paths tested with Utah FORGE Petabyte storage system (April 2024 dataset)
# Note: Replace these paths with your local directory structure
csv_directory = "/scratch/ddordevic/FORGE/GES16Aand16BStimulationMonitoringApril2024/16BStimulationCatalogues/"
folder_path = "/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v1.0.0/"  # Contains HDF5 files

# For SEGY files, ensure they follow the same naming convention: 16B_StrainRate_YYYYMMDDTHHMMSS+0000_NNNNN.segy
process_all_csvs(csv_directory, folder_path)
