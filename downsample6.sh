#!/bin/bash

conda run -n dascore python downsample.py --source_dir /scratch/ddordevic/FORGE/validation_data_source \
                                          --target_dir /scratch/ddordevic/FORGE/validation_data_target \
                                          --log_dir /scratch/ddordevic/FORGE/downsample_logs \
                                          --start_idx 124330 \
                                          --end_idx 149194 \
                                          --filenames /scratch/ddordevic/FORGE/validation_data_source/filenames.pkl \
                                          --up 2 \
                                          --down 5 \

exit 0