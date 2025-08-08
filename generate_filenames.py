"""
This script generates a list of filenames from a specified directory, and sorts them based on their timestamps.
It works on FORGE DAS HDF5 files, but can be adapted for other formats like SEGY, provided they follow the same naming convention.

The filenames are expected to be in the format:
"16B_StrainRate_YYYYMMDDTHHMMSS+0000_NNNNN.[h5|segy]"

The script saves the list of filenames sorted chronologically to a pickle file for later use.
Key use is the downsample.py script, which uses this list to process the files in the correct order.

Author: Danilo Dordevic
Last Updated: August 2025
"""

import os
import pickle
from datetime import datetime
from utils import timestamp2datetime, timestampFromFilename


source_dir = "/lab_downsize/v1.0.0"
filenames = "/scratch/ddordevic/FORGE/filenames_FORGE.pkl"

files = [f for f in os.listdir(source_dir) if f.endswith('.h5') and f.startswith('16B')]
files = sorted(files, key=lambda f: timestamp2datetime(timestampFromFilename(f)))
with open(filenames, "wb") as f:
    pickle.dump(files, f)
