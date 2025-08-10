# FORGE DAS Data Downsampling Project

A comprehensive toolkit for processing, analyzing, and downsampling Distributed Acoustic Sensing (DAS) data from the Utah FORGE geothermal field. This project provides efficient methods for handling large-scale seismic datasets and performing temporal downsampling with anti-aliasing filtering.

## 🎯 Overview

This repository contains tools and analyses for processing DAS (Distributed Acoustic Sensing) data from the Utah FORGE geothermal site. The primary focus is on temporal downsampling of high-frequency DAS recordings while preserving signal integrity through proper anti-aliasing techniques.

### Key Features

- **Intelligent Downsampling**: Temporal downsampling with configurable ratios using scipy's polyphase filtering
- **Data Association**: Match seismic catalog events with corresponding DAS recordings
- **Visualization Tools**: Comprehensive plotting and spectral analysis capabilities
- **Channel Interpolation**: Spatial interpolation methods for DAS channel positioning
- **Batch Processing**: Parallel processing scripts for large datasets
- **Quality Control**: Validation and similarity checking utilities

## 📁 Project Structure

```
forge-downsampling/
├── README.md                              # Project documentation
├── downsample.py                          # Main downsampling script
├── utils.py                              # Utility functions
├── associate_catalog_dataset.py          # Event-data association
├── generate_filenames.py                 # File management utilities
├── check_similarity.py                   # Data validation tools
├── visualization.ipynb                   # Data visualization notebook
├── spectral_analysis.ipynb               # Frequency domain analysis
├── data_statistics.ipynb                 # Statistical analysis
├── plot_events.ipynb                     # Event visualization
├── inspect_csv.ipynb                     # CSV data inspection
├── channel_interpolation/                 # Channel positioning tools
│   ├── channel_interpolation.ipynb       # Spatial interpolation methods
│   ├── *.csv                             # Position data files
│   └── 16B(78)-32 Well Survey/           # Well survey data
├── GES16Aand16BStimulationMonitoringApril2024/ # Field campaign data
├── figures/                           # Analysis results and plots
├── downsample*.sh                        # Batch processing scripts
└── associate.sh                         # Association processing script
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8+
- Conda environment management
- Required packages:
  - `numpy`
  - `scipy`
  - `h5py`
  - `matplotlib`
  - `pandas`
  - `dascore`
  - `tqdm`

### Environment Setup

```bash
# Create the virtual environment folder
python -m venv ~/pyenv/dascore-env

# Activate the virtual environment
source ~/pyenv/dascore-env/bin/activate

# Install the required libraries
pip install -r requirements.txt
```

## 🚀 Usage

### 1. Data Downsampling

The main downsampling functionality is provided by `downsample.py`, which performs temporal downsampling with anti-aliasing:

```bash
python downsample.py \
    --source_dir /path/to/source/data \
    --target_dir /path/to/output/data \
    --log_dir /path/to/logs \
    --start_idx 0 \
    --end_idx 1000 \
    --up 2 \
    --down 5
```

**Parameters:**

- `--source_dir`: Directory containing input HDF5 files
- `--target_dir`: Directory for downsampled output files
- `--log_dir`: Directory for processing logs
- `--start_idx`: Starting file index for processing
- `--end_idx`: Ending file index for processing
- `--up`: Upsampling factor (default: 2)
- `--down`: Downsampling factor (default: 5)
- `--filenames`: Path to pickle file containing sorted filenames

Note: The resample_poly function from scipy.signal performs resampling of a N-dimensional signal by applying an anti-aliasing FIR filter followed by upsampling and downsampling. It takes two key arguments: *upsample_factor* and *downsample_factor*, which define the resampling ratio. The signal is first upsampled by inserting (upsample_factor - 1) zeros between samples, filtered to remove aliasing, and then downsampled by keeping every downsample_factor-th sample. For example, resample_poly(signal, up=1, down=4) reduces the sampling rate by a factor of 4, while resample_poly(signal, up=4, down=1) increases it by 4.

### 2. Batch Processing

Use the provided shell scripts for large-scale processing:

```bash
# Process different data segments in parallel
./downsample1.sh  # Process files 14075-29838
./downsample2.sh  # Process files 43705-59677
./downsample3.sh  # Process files 73672-89515
./downsample4.sh  # Process files 103514-119353
./downsample5.sh  # Process files 119354-149190
```

The scripts were used on the Bigstar cluster in parallel, and were ran by the following command, which allowed them to be ran for a long period of time in the background:

```bash
nohup ./downsample1.sh > output_info1.txt 2>&1 &
```

### 3. Event-Data Association

Associate seismic catalog events with DAS recordings:

```bash
python associate_catalog_dataset.py
```

This script matches temporal windows between seismic catalogs and DAS data files based on event trigger times. For each even in the catalog, it finds the corresponding h5 file, which contains the recording of the event, and a given 12 second time window around it. The output of this script is the path to the h5 file that contains the window, which includes the recordings of the events from the catalog. It appends a new column, titled "MatchedFIle", to the catalog .csv tables. This can be seen by inspecting the catalogs from the folder GES16Aand16BStimulationMonitoringApril2024.

### 4. Data Analysis and Visualization

Interactive Jupyter notebooks are provided for various analyses:

- **`visualization.ipynb`**: Basic data visualization and waterfall plots
- **`spectral_analysis.ipynb`**: Frequency domain analysis and FFT. Used to determine the adequate frequency for downsample the FORGE dataset to. It was chosen to be 4 kHz.
- **`data_statistics.ipynb`**: Statistical analysis of DAS data. Used as part of the exploratory data analysis step.
- **`plot_events.ipynb`**: Event-specific visualizations. Used as part of the exploratory data analysis step.
- **`channel_interpolation.ipynb`**: Spatial interpolation methods for the FORGE DAS cable. This notebook explores spatial interpolation methods to estimate arrival times across the FORGE DAS cable. The goal is to backproject known event arrival times onto each DAS channel using their 3D locations specified as (EASTING, NORTHING, DEPTH). By assuming a planar wavefront or using known event locations, the notebook computes expected arrival times at each channel, effectively creating a dense set of pseudo-labels. These interpolated arrival times can then be used as ground truth for training phase-picking models, which is especially useful given the large number of DAS channels and the difficulty of manual labeling at scale.

## 📊 Data Format

### Input Data Format

Each .h5 file contains a 12 seconds recording. The data is continous, so not every file contains an event. The original sampling frequency is 10 kHz, but it is resampled to 4 kHz. The data is saved on Petabyte storage, with the corresponding paths given below:

The full path to the raw FORGE April 2024 data is: `/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v1.0.0/`

The full path to the downsampled FORGE April 2024 data is: `/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v2.0.0/`

- **File Type**: HDF5 (.h5)
- **Naming Convention**: `16B_StrainRate_YYYYMMDDTHHMMSS+0000_NNNNN.h5`
- **Data Structure**:
  - Dataset: `/Acoustic`
  - Dimensions: `[time_samples, channels]`
  - Attributes: `TimeSamplingInterval(seconds)`, `InterrogationRate(Hz)`

### Output Data Format

- **Downsampled Files**: Same HDF5 structure with reduced temporal resolution
- **Modified Attributes**: Updated sampling interval and interrogation rate
- **Preserved Metadata**: All original file metadata maintained

## 🔬 Processing Methodology

### Downsampling Algorithm

1. **File Grouping**: Process files in overlapping triplets to ensure temporal continuity and to minimize aliasing and edge artifacts that may appear at the edges of the downsampling window.
2. **Concatenation**: Combine three consecutive files in the temporal domain
3. **Anti-aliasing**: Apply polyphase filtering using `scipy.signal.resample_poly`
4. **Extraction**: Extract the middle segment corresponding to the target file
5. **Metadata Update**: Adjust sampling rate and timing attributes of the .h5 file

### Key Features:

- **Ratio**: Default 2:5 upsampling to downsampling (net factor of 2.5), yielding a 4 kHz file from a 10 kHz file
- **Edge Handling**: Special processing for first and last files in sequence
- **Memory Efficiency**: Process files individually to handle large datasets
- **Quality Assurance**: Comprehensive logging and validation

## 📈 Signal Analysis

### Spectral Analysis

- 2D Fourier transforms of DAS data
- Frequency-wavenumber (f-k) analysis
- Power spectral density calculations per channel
- Spectrogram generation

### Event Analysis

- Event detection and characterization
- P-wave and S-wave arrival picking
- Noise spectrum analysis
- Multi-channel event correlation

### Channel Interpolation

- Spatial interpolation of channel positions
- Well trajectory integration
- Arc-length parameterization
- Cubic spline interpolation

## 🗂️ Data Sources

### FORGE Dataset

- **Location**: Utah FORGE geothermal field
- **Well**: 16B(78)-32
- **Campaign**: April 2024 stimulation monitoring
- **Sensors**: 16B DAS array, geophone networks
- **Duration**: Multi-week continuous recording

### Associated Data

- Seismic event catalogs
- Well survey and trajectory data
- Stimulation treatment records
- Multi-instrument coordination data

## 🔍 Validation and Quality Control

### Validation Tools

- **`check_similarity.py`**: Compare processed vs. original data
- **Statistical validation**: Distribution and spectral comparisons
- **Metadata verification**: Ensure attribute consistency
- **File integrity checks**: Validate HDF5 structure

### Quality Metrics

- Signal-to-noise ratio preservation
- Spectral content validation
- Temporal alignment verification
- Amplitude distribution analysis

## 📝 Logging and Monitoring

All processing operations generate comprehensive logs including:

- Processing timestamps and durations
- File-by-file status updates
- Error handling and recovery
- Performance metrics
- Parameter documentation

## 📄 License

MIT License

Copyright (c) 2025 FORGE DAS Downsampling Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**Note**: This license applies to the software code and tools in this repository. The FORGE dataset itself may be subject to separate data usage agreements and institutional policies. Please refer to the [FORGE Data Portal](https://gdr.openei.org/submissions/1375) for data-specific licensing terms.

## 🔗 Related Resources

- [Utah FORGE Project](https://utahforge.com/)
- [DASCore Documentation](https://github.com/DASDAE/dascore)
- [FORGE Data Portal](https://gdr.openei.org/submissions/1680)

---

*Last Updated: August 2025*
