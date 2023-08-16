import numpy as np
import netCDF4 as nc
import matplotlib.pylab as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import TwoSlopeNorm
import os
from os import sys
from matplotlib.dates import MonthLocator, DateFormatter
import warnings
import locale
warnings.filterwarnings("ignore", category=UserWarning) 

# Set the locale to use English language (not working)
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

var1 = os.environ['var1']
var2 = os.environ['var2']
var3 = os.environ['var3']
run_name_a = os.environ['run_name_a']
run_name_b = os.environ['run_name_b']

output_dir = os.environ['senstu'] + "/figures/time_series/" + var1 + var2 + var3 + "/"
os.makedirs(output_dir, exist_ok=True)

# open netcdf
file_a = "/scratch/a/a271098/time_series/" + run_name_a + ".clm2.h0.time_series.nc"
file_b = "/scratch/a/a271098/time_series/" + run_name_b + ".clm2.h0.time_series.nc"

dfile_a = nc.Dataset(file_a, 'r') # read only
dfile_b = nc.Dataset(file_b, 'r') # read only

loc = os.environ['location']

# write variables stations
var1_a = dfile_a[var1][:,loc]
var2_a = dfile_a[var2][:,loc]-273.15
var3_a = dfile_a[var3][:,:,loc]-273.15
var1_b = dfile_b[var1][:,loc]
var2_b = dfile_b[var2][:,loc]-273.15
var3_b = dfile_b[var3][:,:,loc]-273.15

# Calculate the differences between var3_a and var3_b
var2_diff = var2_a - var2_b

# Calculate the differences between var3_a and var3_b
var3_diff = var3_a - var3_b

# set up the figure with three subplots
fig, axs = plt.subplots(4, 1, figsize=(12, 18))

axs[0].plot(var1_a, label='Sturm run')
axs[0].plot(var1_b, label='Control run')
# Fill the area below a transparent color
axs[0].fill_between(range(len(var1_a)), var1_a, var1_b, where=(var1_a > var1_b), alpha=0.3)
axs[0].fill_between(range(len(var1_b)), var1_b, var1_a, where=(var1_b > var1_a), alpha=0.3)

axs[0].set_ylabel('snow depth (in m)')
axs[0].legend(loc='upper right')
axs[0].set_xlim(0, var1_a.shape[0])

axs[1].axhline(y=0, color='black', alpha=0.5, linewidth=0.7,)
axs[1].plot(var2_a)
axs[1].plot(var2_b)

axs[1].set_ylabel('air temperature (in °C)')
axs[1].set_xlim(0, var2_a.shape[0])

# Define the color gradients for var3
cmap_a = plt.cm.get_cmap('Blues')
cmap_b = plt.cm.get_cmap('Oranges')
cmap_diff = plt.cm.get_cmap('Greys')
line_styles = ['-', '--', '-.', ':', '-']  # Define the line styles

levgrnd = [0.01, 0.04, 0.09, 0.16, 0.26, 0.4, 0.58, 0.8, 1.06, 1.36, 1.7, 
           2.08, 2.5, 2.99, 3.58, 4.27, 5.06, 5.95, 6.94, 8.03, 9.795, 13.32777,
           19.48313, 28.87072, 41.99844]

axs[2].axhline(y=0, color='black', alpha=0.5, linewidth=0.7,)
# Loop for plotting var3 at every 5th depth
depths = range(0, var3_a.shape[1], 5)  # Every 5th depth
for i, depth in enumerate(depths):
	alpha = (depth / var3_a.shape[1]) * 0.5 + 0.5  # Adjust the alpha value for darker lines
	line_style = line_styles[i % len(line_styles)]  # Cycle through the line styles
	axs[2].plot(var3_a[:, depth], color=cmap_a(1 - depth / var3_a.shape[1]), linestyle=line_style, alpha=alpha, label=f"{levgrnd[depth]}m")
	axs[2].plot(var3_b[:, depth], color=cmap_b(1 - depth / var3_a.shape[1]), linestyle=line_style, alpha=alpha, label=f"{levgrnd[depth]}m")

axs[2].set_ylabel('soil temperature (in °C)')
axs[2].legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)
axs[2].set_xlim(0, var3_a.shape[0])

axs[3].axhline(y=0, color='black', alpha=0.5, linewidth=0.7,)
axs[3].plot(var2_diff, color='red', linewidth=1.5, label="air temp.")

# Loop for plotting var3 diff at every 5th depth
for i, depth in enumerate(depths):
	alpha = (depth / var3_diff.shape[1]) * 0.5 + 0.5  # Adjust the alpha value for darker lines
	line_style = line_styles[i % len(line_styles)]  # Cycle through the line styles
	axs[3].plot(var3_diff[:, depth], color=cmap_diff(1 - depth / var3_diff.shape[1]), linestyle=line_style, alpha=alpha, label=f"{levgrnd[depth]}m")

# Set x-axis tick positions and labels to display once per month
axs[3].xaxis.set_major_locator(MonthLocator())
axs[3].xaxis.set_major_formatter(DateFormatter("%b"))

axs[3].set_xlabel(os.environ['year'])
axs[3].set_ylabel('temperature differences (in °C)')
axs[3].legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)
axs[3].set_xlim(0, var3_diff.shape[0])

# adjust the spacing between subplots
plt.subplots_adjust(hspace=0)

# show and save the plot
plot_name = output_dir + loc + "." + var1 + var2 + var3 + "." + os.environ['year'] + ".time_series." + os.environ['run_name_a'] + "-" + os.environ['run_name_b']
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()

