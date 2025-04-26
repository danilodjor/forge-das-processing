#!/bin/bash

conda run -n dascore python downsample.py --source_dir /scratch/ddordevic/FORGE/validation_data_source \
                                          --target_dir /scratch/ddordevic/FORGE/validation_data_target \
                                          --log_dir /scratch/ddordevic/FORGE/downsample_logs \
                                          --start_idx 0 \
                                          --end_idx 24865 \
                                          --filenames /scratch/ddordevic/FORGE/validation_data_source/filenames.pkl \
                                          --up 2 \
                                          --down 5 \

exit 0