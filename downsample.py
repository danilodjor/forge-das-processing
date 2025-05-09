import os
import h5py
import time
import shutil
import logging
import argparse
import pickle
import numpy as np
from datetime import datetime
from scipy.signal import resample_poly, resample


# Function definitions
def timestamp2datetime(timestamp):
    return datetime.strptime(timestamp, "%Y%m%dT%H%M%S")


def timestampFromFilename(filename):
    return filename.split("StrainRate_")[1].split("+")[0]


def process_files(source_dir, target_dir, start_idx, end_idx, up, down, filenames):
    resample_ratio = up / down

    # Sort the filenames according to the date
    if not os.path.exists(filenames):
        files = [f for f in os.listdir(source_dir) if f.endswith('.h5') and f.startswith('16B')]
        files = sorted(files, key=lambda f: timestamp2datetime(timestampFromFilename(f)))
        with open(filenames, "wb") as f:
            pickle.dump(files, f)
    else:
        with open(filenames, "rb") as f:
            files = pickle.load(f)

    # Process boundaries
    start_idx = max(0, start_idx)  # Ensure start_idx is not less than 0
    end_idx = min(len(files) - 1, end_idx)  # Ensure end_idx is not beyond the list length

    if end_idx == -1:
        end_idx = len(files) - 1

    files = files[start_idx:end_idx + 1]

    # Start downsampling
    logging.info(f"Starting downsampling of {len(files)} files...")

    # Process first file
    file1_path = os.path.join(source_dir, files[0])
    file2_path = os.path.join(source_dir, files[1])

    file1_path_new = os.path.join(target_dir, files[0])
    shutil.copyfile(file1_path, file1_path_new)

    with h5py.File(file1_path_new, 'r+') as f1, \
         h5py.File(file2_path, 'r') as f2:

        dataset1 = f1['Acoustic']
        dataset2 = f2['Acoustic']

        datasets_data = np.concatenate([dataset1, dataset2], axis=0)
        data_downsampled = resample_poly(datasets_data, up=up, down=down, axis=0)
        start_idx_sig2 = 0
        end_idx_sig2 = dataset1.shape[0]
        start_idx_resampled = int(np.round(start_idx_sig2 * resample_ratio))
        end_idx_resampled = int(np.round(end_idx_sig2 * resample_ratio))

        data_downsampled = data_downsampled[start_idx_resampled:end_idx_resampled]

        assert data_downsampled.shape[0] == dataset1.shape[0]/2.5 and data_downsampled.shape[1] == dataset1.shape[1]

        dataset1.resize(data_downsampled.shape)
        dataset1[...] = data_downsampled
        dataset1.attrs.modify('TimeSamplingInterval(seconds)',
                            dataset1.attrs['TimeSamplingInterval(seconds)']/resample_ratio)
        dataset1.attrs.modify('InterrogationRate(Hz)',
                            dataset1.attrs['InterrogationRate(Hz)']*resample_ratio)

    logging.info(f"Finished file {start_idx}/{len(files)} | {files[0]}")

    # Process triplets of consecutive files
    for i in range(1, len(files)-1):
        start_time = time.time()

        file1_path = os.path.join(source_dir, files[i-1])
        file2_path = os.path.join(source_dir, files[i])  # main file to process
        file3_path = os.path.join(source_dir, files[i+1])

        file2_path_new = os.path.join(target_dir, files[i])
        shutil.copyfile(file2_path, file2_path_new)

        with h5py.File(file1_path, 'r') as f1, \
             h5py.File(file2_path_new, 'r+') as f2, \
             h5py.File(file3_path, 'r') as f3:

            dataset1 = f1['Acoustic']
            dataset2 = f2['Acoustic']
            dataset3 = f3['Acoustic']

            datasets_data = np.concatenate([dataset1, dataset2, dataset3], axis=0)
            data_downsampled = resample_poly(datasets_data, up=up, down=down, axis=0)

            # Find indices for the second signal
            start_idx_sig2 = dataset1.shape[0]
            end_idx_sig2 = dataset1.shape[0]+dataset2.shape[0]
            start_idx_resampled = int(np.round(start_idx_sig2 * resample_ratio))
            end_idx_resampled = int(np.round(end_idx_sig2 * resample_ratio))

            data_downsampled = data_downsampled[start_idx_resampled:end_idx_resampled]

            assert data_downsampled.shape[0] == dataset2.shape[0]/2.5 and data_downsampled.shape[1] == dataset2.shape[1]

            dataset2.resize(data_downsampled.shape)
            dataset2[...] = data_downsampled
            dataset2.attrs.modify('TimeSamplingInterval(seconds)',
                                dataset2.attrs['TimeSamplingInterval(seconds)']/resample_ratio)
            dataset2.attrs.modify('InterrogationRate(Hz)',
                                dataset2.attrs['InterrogationRate(Hz)']*resample_ratio)

        os.remove(file1_path)

        logging.info(f"Finished file {i+start_idx}/{len(files)} | {files[i]} | Time elapsed: {time.time() - start_time:.2f} s")


    # Process last file
    file1_path = os.path.join(source_dir, files[-2])
    file2_path = os.path.join(source_dir, files[-1])

    file2_path_new = os.path.join(target_dir, files[-1])
    shutil.copyfile(file2_path, file2_path_new)

    with h5py.File(file1_path, 'r') as f1, \
         h5py.File(file2_path_new, 'r+') as f2:

        dataset1 = f1['Acoustic']
        dataset2 = f2['Acoustic']

        datasets_data = np.concatenate([dataset1, dataset2], axis=0)
        data_downsampled = resample_poly(datasets_data, up=up, down=down, axis=0)

        start_idx_sig2 = dataset1.shape[0]
        end_idx_sig2 = dataset1.shape[0]+dataset2.shape[0]
        start_idx_resampled = int(np.round(start_idx_sig2 * resample_ratio))
        end_idx_resampled = int(np.round(end_idx_sig2 * resample_ratio))

        data_downsampled = data_downsampled[start_idx_resampled:end_idx_resampled]

        assert data_downsampled.shape[0] == dataset2.shape[0]/2.5 and data_downsampled.shape[1] == dataset2.shape[1]

        dataset2.resize(data_downsampled.shape)
        dataset2[...] = data_downsampled
        dataset2.attrs.modify('TimeSamplingInterval(seconds)',
                            dataset2.attrs['TimeSamplingInterval(seconds)']/resample_ratio)
        dataset2.attrs.modify('InterrogationRate(Hz)',
                            dataset2.attrs['InterrogationRate(Hz)']*resample_ratio)

    os.remove(file1_path)
    os.remove(file2_path)

    logging.info(f"Finished file {end_idx}/{len(files)} | {files[-1]}")


def main():
    parser = argparse.ArgumentParser(description="Downsample DAS HDF5 files by a factor of 2.")
    parser.add_argument('--source_dir', type=str, required=True, help='Source directory containing original HDF5 files')
    parser.add_argument('--target_dir', type=str, required=True, help='Target directory to save downsampled HDF5 files')
    parser.add_argument('--log_dir', type=str, default='./downsample_logs', help='Directory to save log files')
    parser.add_argument('--start_idx', type=int, default=0, help='Index to start processing files from')
    parser.add_argument('--end_idx', type=int, default=-1, help='Index to stop processing files at')
    parser.add_argument('--filenames', type=str, default=None, help='Path to file containing filenames to process')
    parser.add_argument('--up', type=int, default=2, help='Upsampling factor')
    parser.add_argument('--down', type=int, default=5, help='Downsampling factor')

    args = parser.parse_args()

    # Setup logging
    date_stamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    logging.basicConfig(filename=os.path.join(args.log_dir, f"validation_{date_stamp}.log"),
                        filemode="w",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',)

    for arg, value in vars(args).items():
        logging.info(f'{arg} = {value}')

    # Setup source and target folders
    source_dir = args.source_dir
    target_dir = args.target_dir
    log_dir = args.log_dir
    start_idx = args.start_idx
    end_idx = args.end_idx
    filenames = args.filenames
    up = args.up
    down = args.down

    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    # Main processing
    process_files(source_dir, target_dir, start_idx, end_idx, up, down, filenames)

    logging.info("Finished processing all files.")


if __name__ == "__main__":
    main()
