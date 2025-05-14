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