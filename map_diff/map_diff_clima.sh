#!/bin/bash

# What user need to change
export run_name_a="57_DOM02_001" # default run
export run_name_b="57_DOM02_043"
#(need to change period on make_climatology.sh line 18 or 22)
export variable="H2OSOI"

export dimension="3D"
export levelname="levsoi" # levsoi or levgrnd
export depth_a=9
export depth_b=8
export depthavg="yes" # yes or no
export topdepth_a=1 # if depthavg is yes
export topdepth_b=1 # if depthavg is yes

export legendtitle="column soil liquid water difference in kg/m3" # snow difference in m soil temperature difference at 1m in °C

echo "Make climatology averages"
export run_name=$run_name_a
export depth=$depth_a
export topdepth=$topdepth_a
$senstu/map_diff/make_climatology.sh
export run_name=$run_name_b
export depth=$depth_b
export topdepth=$topdepth_b
$senstu/map_diff/make_climatology.sh

echo "Map climatology averages"
for i in {01..12}; do
	export month=$i
	echo $month

	file_a=$senstu/data/$run_name_a/climatology/remap/remap.$run_name_a.$variable.$month.nc
	file_b=$senstu/data/$run_name_b/climatology/remap/remap.$run_name_b.$variable.$month.nc

	python $senstu/map_diff/map_diff.py $file_a $file_b
done
