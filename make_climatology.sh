#!/bin/bash

# Define input directories and output directory
input_dir="data/$run_name/monthly"
output_dir="data/$run_name/climatology"

mkdir -p $output_dir

# Loop through months and calculate period average
for month in {01..12}; do
  # Define input and output file names
  input_files="${input_dir}/*${month}.nc"
  output_file="${output_dir}/${run_name}.${month}.nc"
  
  # Use NCO to calculate period average
  
done

