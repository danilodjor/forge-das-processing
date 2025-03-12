import os
import h5py
import numpy as np
import os
import numpy as np
from datetime import datetime
import shutil
import h5py
from scipy.signal import resample_poly, resample
import logging

# Setup source and target folders
source_dir = "validation_data_source/" # "/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v1.0.0"
target_dir = "validation_data_traget/" # "/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v1.0.0/downsampled"
log_dir = "./downsample_logs"

os.makedirs(target_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Setup logging
logging.basicConfig(filename="validation.log",
                    filemode="w",
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',)

# Function definitions
def timestamp2datetime(timestamp):
    return datetime.strptime(timestamp, "%Y%m%dT%H%M%S")


def timestampFromFilename(filename):
    return filename.split("StrainRate_")[1].split("+")[0]


def process_files(source_dir, target_dir):
    # Sort the filenames according to the date
    files = [f for f in os.listdir(source_dir) if f.endswith('.h5') and f.startswith('16B')]
    files = sorted(files, key=lambda f: timestamp2datetime(timestampFromFilename(f)))

    logging.info(f"Starting downsampling of {len(files)} files...")

    # Process first file
    file1_path = os.path.join(source_dir, files[0])
    file2_path = os.path.join(source_dir, files[1])

    file1_path_new = os.path.join(target_dir, files[0])
    shutil.copy2(file1_path, file1_path_new)

    f1 = h5py.File(file1_path_new, 'r+')
    f2 = h5py.File(file2_path, 'r')

    dataset1 = f1['Acoustic']
    dataset2 = f2['Acoustic']

    datasets_data = np.concatenate([dataset1, dataset2], axis=0)
    # resample_poly(datasets_data, up=1, down=2, axis=0)
    data_downsampled = resample(datasets_data, num=datasets_data.shape[0]//2, axis=0)
    data_downsampled = data_downsampled[:dataset1.shape[0]//2]

    assert data_downsampled.shape[0] == dataset1.shape[0]//2 and data_downsampled.shape[1] == dataset1.shape[1]

    dataset1.resize(data_downsampled.shape)
    dataset1[...] = data_downsampled
    dataset1.attrs.modify('TimeSamplingInterval(seconds)',
                          dataset1.attrs['TimeSamplingInterval(seconds)']*2)
    dataset1.attrs.modify('InterrogationRate(Hz)',
                          dataset1.attrs['InterrogationRate(Hz)']/2)

    f1.close()
    f2.close()

    logging.info(f"Finished file 1/{len(files)} | {files[0]}")

    # Process triplets of consecutive files
    for i in range(1, len(files)-1):
        file1_path = os.path.join(source_dir, files[i-1])
        file2_path = os.path.join(source_dir, files[i])  # main file to process
        file3_path = os.path.join(source_dir, files[i+1])

        file2_path_new = os.path.join(target_dir, files[i])
        shutil.copy2(file2_path, file2_path_new)

        f1 = h5py.File(file1_path, 'r')
        f2 = h5py.File(file2_path_new, 'r+')
        f3 = h5py.File(file3_path, 'r')

        dataset1 = f1['Acoustic']
        dataset2 = f2['Acoustic']
        dataset3 = f3['Acoustic']

        datasets_data = np.concatenate([dataset1, dataset2, dataset3], axis=0)
        # resample_poly(datasets_data, up=1, down=2, axis=0)
        data_downsampled = resample(datasets_data, num=datasets_data.shape[0]//2, axis=0)
        data_downsampled = data_downsampled[dataset1.shape[0] // 2:dataset1.shape[0]//2+dataset2.shape[0]//2]

        assert data_downsampled.shape[0] == dataset2.shape[0]//2 and data_downsampled.shape[1] == dataset2.shape[1]

        dataset2.resize(data_downsampled.shape)
        dataset2[...] = data_downsampled
        dataset2.attrs.modify('TimeSamplingInterval(seconds)',
                              dataset2.attrs['TimeSamplingInterval(seconds)']*2)
        dataset2.attrs.modify('InterrogationRate(Hz)',
                              dataset2.attrs['InterrogationRate(Hz)']/2)

        f1.close()
        f2.close()
        f3.close()

        os.remove(file1_path)

        logging.info(f"Finished file {i+1}/{len(files)} | {files[i]}")


    # Process last file
    file1_path = os.path.join(source_dir, files[-2])
    file2_path = os.path.join(source_dir, files[-1])

    file2_path_new = os.path.join(target_dir, files[-1])
    shutil.copy2(file2_path, file2_path_new)

    f1 = h5py.File(file1_path, 'r')
    f2 = h5py.File(file2_path_new, 'r+')

    dataset1 = f1['Acoustic']
    dataset2 = f2['Acoustic']

    datasets_data = np.concatenate([dataset1, dataset2], axis=0)
    # resample_poly(datasets_data, up=1, down=2, axis=0)
    data_downsampled = resample(
        datasets_data, num=datasets_data.shape[0]//2, axis=0)
    data_downsampled = data_downsampled[dataset1.shape[0] //
                                        2:dataset1.shape[0]//2+dataset2.shape[0]]

    assert data_downsampled.shape[0] == dataset2.shape[0]//2 and data_downsampled.shape[1] == dataset2.shape[1]

    dataset2.resize(data_downsampled.shape)
    dataset2[...] = data_downsampled
    dataset2.attrs.modify('TimeSamplingInterval(seconds)',
                          dataset2.attrs['TimeSamplingInterval(seconds)']*2)
    dataset2.attrs.modify('InterrogationRate(Hz)',
                          dataset2.attrs['InterrogationRate(Hz)']/2)

    f1.close()
    f2.close()

    os.remove(file1_path)
    os.remove(file2_path)

    logging.info(f"Finished file {len(files)}/{len(files)} | {files[-1]}")
    logging.info("Finished processing all files.")



def main():
    process_files(source_dir, target_dir)


if __name__ == "__main__":
    main()
