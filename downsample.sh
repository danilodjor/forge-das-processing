#!/bin/bash

conda run -n dascore python downsample.py --source_dir /scratch/ddordevic/FORGE/validation_data_source \
                                          --target_dir /scratch/ddordevic/FORGE/validation_data_traget \
                                          --log_dir /scratch/ddordevic/FORGE/downsample_logs

exit 0