#!/bin/bash
#SBATCH --job-name=associate_files      # Job name
#SBATCH --output=job_output.log      # Standard output and error log
#SBATCH --error=job_error.log        # Error log
#SBATCH --time=03:00:00              # Time limit hh:mm:ss
#SBATCH --mem=12G                      # Memory required per node

# Load necessary modules (if required by your environment)
source /scratch/ddordevic/miniconda3/etc/profile.d/conda.sh
conda activate dascore

# Define paths (update these before running)
csv_path="/scratch/ddordevic/FORGE/FORGE16BApril24NetworkBackgroundB.csv"
folder_path="/bedrettolab/E1B/DAS/2024_FORGE/DATA_RAW_fromOpenei/April_2024/v1.0.0/"
output_csv="matching_catalog_files_B.csv"

# Run the Python script
python your_script.py "$csv_path" "$folder_path" "$output_csv"

echo "Job completed successfully. Output saved to $output_csv"
