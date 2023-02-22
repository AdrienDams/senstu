#!/bin/bash

# Define input directories and output directory
input_dir=$senstu/data/$run_name/monthly
output_dir=$senstu/data/$run_name/climatology

mkdir -p $output_dir
mkdir -p $output_dir/remap

echo $run_name

# Loop through months and calculate period average
for month in {01..12}; do
	echo $month

	# Make climatology averages and extract variable
	if [ "$dimension" = "2D" ]; then
		ncea -O -v $variable $input_dir/*.{1980..1985}-$month.nc $output_dir/$run_name.$variable.$month.nc
	fi
	# Select variable for 3D
	if [ "$dimension" = "3D" ]; then
		ncea -O -F -d $levelname,$depth -v $variable $input_dir/*.{1980..1985}-$month.nc $output_dir/$run_name.$variable.$month.nc
	fi
	
	# Regrid model
	cdo -r setgrid,$descriptiongrid -selvar,$variable $output_dir/$run_name.$variable.$month.nc $output_dir/remap/grid.$run_name.$variable.$month.tmp.nc
	# Remap model
	cdo -r remapnn,$descriptionreg -selvar,$variable $output_dir/remap/grid.$run_name.$variable.$month.tmp.nc $output_dir/remap/remap.$run_name.$variable.$month.tmp.nc
	# Crop model (not latitude above 90)
	ncks -O -F -d lat,0.,90. $output_dir/remap/remap.$run_name.$variable.$month.tmp.nc $output_dir/remap/remap.$run_name.$variable.$month.nc

	# Remove temporay files
	rm -f $output_dir/remap/*tmp.nc
done
