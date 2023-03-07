# print a linear plot between modelled (from CTSM output) and observed data (from station)

import numpy as np
import netCDF4 as nc
import matplotlib.pylab as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import TwoSlopeNorm
import os
from os import sys
from plotting_functions import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

var1 = "TSOI"
var2 = "SOILLIQ"
var3 = "SOILICE"
run_name_a = os.environ['run_name_a']
run_name_b = os.environ['run_name_b']

output_dir = os.environ['senstu'] + "/figures/time_series/" + var1 + var2 + var3 + "/"
os.makedirs(output_dir, exist_ok=True)

# open netcdf
file_a = "/work/aa0049/a271098/archive/" + run_name_a + "/lnd/hist/daily/" + run_name_a + ".clm2.h0.2000.vars.nc" 
file_b = "/work/aa0049/a271098/archive/" + run_name_b + "/lnd/hist/daily/" + run_name_b + ".clm2.h0.2000.vars.nc"

dfile_a = nc.Dataset(file_a, 'r') # read only
dfile_b = nc.Dataset(file_b, 'r') # read only

loc = 86662

levgrnd_a = dfile_a["levgrnd"][:]
levgrnd_b = dfile_b["levgrnd"][:]

# write variables stations
var1_a = dfile_a[var1][:,:,loc]
var2_a = dfile_a[var2][:,:,loc]
var3_a = dfile_a[var3][:,:,loc]
var1_b = dfile_b[var1][:,:,loc]
var2_b = dfile_b[var2][:,:,loc]
var3_b = dfile_b[var3][:,:,loc]

# define a custom color map from green to brown
cmap = plt.cm.get_cmap('terrain')

# set up the figure
fig, axs = plt.subplots(3, 2, figsize=(15, 15))

# loop through each variable
for i, (var, num_layers) in enumerate(zip(['var1', 'var2', 'var3'], [15, 10, 10])):
    
    # get the data for each dataset
    data_a = eval(f'{var}_a')
    data_b = eval(f'{var}_b')
    
    # plot each layer on its own subplot
    for j, layer in enumerate(range(1, num_layers)):
        
        # get the data for this layer
        layer_data_a = data_a[:, layer]
        layer_data_b = data_b[:, layer]
        
        # plot the data on the appropriate subplot
        axs[i, 0].plot(layer_data_a, color=cmap(j/num_layers), label=f'Dataset CLM5 Layer {layer}')
        axs[i, 1].plot(layer_data_b[:8], color=cmap(j/num_layers), label=f'Dataset CLM45 Layer {layer}')
        
    # set the title and axis labels for this subplot
    axs[i, 0].set_title(f'{var} (Dataset CLM5)')
    axs[i, 1].set_title(f'{var} (Dataset CLM45)')
    axs[i, 0].set_xlabel('Days')
    axs[i, 0].set_ylabel(var)
    axs[i, 1].set_xlabel('Days')
    axs[i, 1].set_ylabel(var)
    
# add a single legend at the bottom of the figure
#fig.legend(bbox_to_anchor=(0.5, 0), loc='lower center', ncol=2)

plt.show()

# show the final plot
plt.show()
