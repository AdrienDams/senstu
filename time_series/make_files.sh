#!/bin/bash

#SBATCH --partition=shared
#SBATCH --ntasks=1
#SBATCH --time=8:00:00
#SBATCH --account=aa0049
#SBATCH --mem-per-cpu=60G

export var1="SNOW_DEPTH" # 2D variable
export var2="TSA" # 2D variable
export var3="TSOI" # 3D variable

export year=1981

export run_name_a="57_DOM02_001"
export run_name_b="57_DOM02_047"

export location=132022

ncrcat -O -v $var1,$var2,$var3 /work/aa0049/a271098/archive/$run_name_a/lnd/hist/daily/$run_name_a.clm2.h0.$year-??-??.ext.nc /scratch/a/a271098/time_series/$run_name_a.clm2.h0.time_series.nc
ncrcat -O -v $var1,$var2,$var3 /work/aa0049/a271098/archive/$run_name_b/lnd/hist/daily/$run_name_b.clm2.h0.$year-??-??.ext.nc /scratch/a/a271098/time_series/$run_name_b.clm2.h0.time_series.nc

python time_series.py
