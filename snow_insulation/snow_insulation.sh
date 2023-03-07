#!/bin/bash
#SBATCH --partition=shared
#SBATCH --ntasks=2
#SBATCH --time=08:00:00
#SBATCH --account=aa0049

export run_name_a="57_DOM02_001" # default run
export run_name_b="57_DOM02_043"

folder_a=$senstu/data/$run_name_a/daily
folder_b=$senstu/data/$run_name_b/daily

vars="lat,lon,TSOI,TSA,SNOW_DEPTH"

mkdir -p $scratch_dir/snow_insulation

ncrcat -O -v $vars $folder_a/$run_name_a.clm2.h0.????-01-??.ext.nc $scratch_dir/snow_insulation/$run_name_a.01.nc
ncrcat -O -v $vars $folder_a/$run_name_a.clm2.h0.????-02-??.ext.nc $scratch_dir/snow_insulation/$run_name_a.02.nc
ncrcat -O -v $vars $folder_a/$run_name_a.clm2.h0.????-12-??.ext.nc $scratch_dir/snow_insulation/$run_name_a.12.nc

ncrcat -O -v $vars $scratch_dir/snow_insulation/$run_name_a.??.nc $scratch_dir/snow_insulation/$run_name_a.nc

ncrcat -O -v $vars $folder_b/$run_name_b.clm2.h0.????-01-??.ext.nc $scratch_dir/snow_insulation/$run_name_b.01.nc
ncrcat -O -v $vars $folder_b/$run_name_b.clm2.h0.????-02-??.ext.nc $scratch_dir/snow_insulation/$run_name_b.02.nc
ncrcat -O -v $vars $folder_b/$run_name_b.clm2.h0.????-12-??.ext.nc $scratch_dir/snow_insulation/$run_name_b.12.nc

ncrcat -O -v $vars $scratch_dir/snow_insulation/$run_name_b.??.nc $scratch_dir/snow_insulation/$run_name_b.nc
