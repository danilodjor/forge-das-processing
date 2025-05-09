#!/bin/bash

conda run -n dascore python downsample.py --source_dir /lab_downsize/v1.0.0 \
                                          --target_dir /lab_downsize/v2.0.0 \
                                          --log_dir /scratch/ddordevic/FORGE/downsample_logs \
                                          --start_idx 119354 \
                                          --end_idx 149190 \
                                          --filenames /scratch/ddordevic/FORGE/validation_data_source/filenames_FORGE.pkl \
                                          --up 2 \
                                          --down 5 \

exit 0