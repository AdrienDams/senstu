#!/bin/bash

#SBATCH --partition=shared
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=60G

export var1="TSOI" # 3D variable
export var2="SNOW_DEPTH" # 2D variable

levelname="levgrnd" #"levgrnd" #nlevsoi #time
depth=9

export year=1980

export run_name_a="57_DOM02_001"
export run_name_b="57_DOM02_047"

export location=26735

ncrcat -O -d $levelname,$depth -v $var1,$var2 /work/aa0049/a271098/archive/$run_name_a/lnd/hist/daily/$run_name_a.clm2.h0.$year-??-??.ext.nc /scratch/a/a271098/time_series/$run_name_a.clm2.h0.time_series.nc
ncrcat -O -d $levelname,$depth -v $var1,$var2 /work/aa0049/a271098/archive/$run_name_b/lnd/hist/daily/$run_name_b.clm2.h0.$year-??-??.ext.nc /scratch/a/a271098/time_series/$run_name_b.clm2.h0.time_series.nc

python time_series.py
