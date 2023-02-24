#!/bin/bash
export run_name_a="57_DOM02_001" # default run
export run_name_b="57_DOM02_043"

export var1="H2OSOI"
export var2="SOILLIQ"
export var3="SOILICE"

echo "Map soil hum averages"
for i in {01..12}; do
	export month=$i
	echo $month

	file_1=$senstu/data/$run_name_a/climatology/remap/remap.$run_name_a.$var1.$month.nc
	file_2=$senstu/data/$run_name_a/climatology/remap/remap.$run_name_a.$var2.$month.nc
	file_3=$senstu/data/$run_name_a/climatology/remap/remap.$run_name_a.$var3.$month.nc
	file_4=$senstu/data/$run_name_b/climatology/remap/remap.$run_name_b.$var1.$month.nc
	file_5=$senstu/data/$run_name_b/climatology/remap/remap.$run_name_b.$var2.$month.nc
	file_6=$senstu/data/$run_name_b/climatology/remap/remap.$run_name_b.$var3.$month.nc

	python $senstu/soil_hum/maps_soil_hum.py $file_1 $file_2 $file_3 $file_4 $file_5 $file_6
done
