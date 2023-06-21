# print a linear plot between modelled two CTSM runs

import numpy as np
import netCDF4 as nc
import matplotlib.pylab as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import TwoSlopeNorm
import os
from os import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

var1 = os.environ['var1']
var2 = os.environ['var2']
run_name_a = os.environ['run_name_a']
run_name_b = os.environ['run_name_b']

output_dir = os.environ['senstu'] + "/figures/time_series/" + var1 + var2 + "/"
os.makedirs(output_dir, exist_ok=True)

# open netcdf
file_a = "/scratch/a/a271098/time_series/" + run_name_a + ".clm2.h0.time_series.nc"
file_b = "/scratch/a/a271098/time_series/" + run_name_b + ".clm2.h0.time_series.nc"

dfile_a = nc.Dataset(file_a, 'r') # read only
dfile_b = nc.Dataset(file_b, 'r') # read only

loc = os.environ['location']

# write variables stations
var1_a = dfile_a[var1][:,0,loc]
var2_a = dfile_a[var2][:,loc]
var1_b = dfile_b[var1][:,0,loc]
var2_b = dfile_b[var2][:,loc]

# set up the figure with two subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# plot the data for variable 1
axs[0].plot(var1_a, label=run_name_a)
axs[0].plot(var1_b, label=run_name_b)

# set the title and axis labels for variable 1
axs[0].set_xlabel('Days')
axs[0].set_ylabel(var1)
axs[0].legend()

# plot the data for variable 2
axs[1].plot(var2_a, label=run_name_a)
axs[1].plot(var2_b, label=run_name_b)

# set the title and axis labels for variable 2
axs[1].set_xlabel('Days')
axs[1].set_ylabel(var2)
axs[1].legend()

# adjust the spacing between subplots
plt.subplots_adjust(hspace=0.2)

# show and save the plot
plot_name = output_dir + loc + "." + var1 + "-" + var2 + "." + os.environ['year'] + ".time_series." + os.environ['run_name_a'] + "-" + os.environ['run_name_b']
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()
