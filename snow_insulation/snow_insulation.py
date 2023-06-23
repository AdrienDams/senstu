# Make wenli graph
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.colors as colors
from matplotlib.colors import TwoSlopeNorm
import os
import sys

folder = os.environ['scratch_dir'] + "/snow_insulation/"
output_dir = os.environ['senstu'] + "/figures/snow_insulation/"
os.makedirs(output_dir, exist_ok=True)
zero_abs = 273.15

# select stations
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.txt", delimiter=" ", dtype=int)
stations = index_table[:,1]

# open files and extract variables
ds_a = xr.open_dataset(folder + os.environ['run_name_a'] + ".nc")
ds_b = xr.open_dataset(folder + os.environ['run_name_b'] + ".nc")

tsa_a = ds_a["TSA"][:,stations].values-zero_abs
tsa_b = ds_b["TSA"][:,stations].values-zero_abs
tsoi_a = ds_a["TSOI"][:,4,stations].values-zero_abs # 3 = take at 16 cm
tsoi_b = ds_b["TSOI"][:,4,stations].values-zero_abs # 4 = take at 21 cm (for CLM45 run)
snow_a = ds_a["SNOW_DEPTH"][:,stations].values
snow_b = ds_b["SNOW_DEPTH"][:,stations].values
snow_a = snow_a[:,:]*100 # convert into cm
snow_b = snow_b[:,:]*100 # convert into cm

print("open data done")

# calculate winter_offset
winter_offset_a = tsoi_a[:,:] - tsa_a[:,:]
winter_offset_b = tsoi_b[:,:] - tsa_b[:,:]

# Define the snow bin edges
snow_bin_edges = np.arange(0, 101, 5)
snow_bins = np.arange(5,96,5)

# Define the air temperature regimes
tsa_edges = [float('-inf'), -25, -15, -5]
tsa_labels = ['TSA < -25', '-25 < TSA < -15', '-15 < TSA < -5']
tsa_colors = ['blue', 'orange', 'red']

# create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

for i in range(len(tsa_labels)):
    # filter data based on air temperature regime
    idx_a = np.where((tsa_a > tsa_edges[i]) & (tsa_a <= tsa_edges[i+1]))[0]
    print(idx_a) # is this wrong?
    idx_b = np.where((tsa_b > tsa_edges[i]) & (tsa_b <= tsa_edges[i+1]))[0]

    # calculate winter offset mean and standard deviation for each snow bin
    winter_offset_mean_a = np.zeros(np.size(snow_bins))
    winter_offset_mean_b = np.zeros(np.size(snow_bins))
    winter_offset_std_a = np.zeros(np.size(snow_bins))
    winter_offset_std_b = np.zeros(np.size(snow_bins))

    for j in range(0, len(snow_bins)):
        winter_offset_mean_a[j] = np.nanmean(winter_offset_a[idx_a][(snow_a[idx_a]>=snow_bin_edges[j]) & (snow_a[idx_a]<snow_bin_edges[j+1])])
        winter_offset_mean_b[j] = np.nanmean(winter_offset_b[idx_b][(snow_b[idx_b]>=snow_bin_edges[j]) & (snow_b[idx_b]<snow_bin_edges[j+1])])
        winter_offset_std_a[j] = np.nanstd(winter_offset_a[idx_a][(snow_a[idx_a]>=snow_bin_edges[j]) & (snow_a[idx_a]<snow_bin_edges[j+1])])/2
        winter_offset_std_b[j] = np.nanstd(winter_offset_b[idx_b][(snow_b[idx_b]>=snow_bin_edges[j]) & (snow_b[idx_b]<snow_bin_edges[j+1])])/2

    # plot scatter and errorbars for each snow bin
    ax1.scatter(snow_bins, winter_offset_mean_a, color=tsa_colors[i], linewidth=2, label=tsa_labels[i])
    ax1.errorbar(snow_bins, winter_offset_mean_a, yerr=winter_offset_std_a, fmt='none', ecolor=tsa_colors[i], alpha=0.3)
    ax2.scatter(snow_bins, winter_offset_mean_b, color=tsa_colors[i], linewidth=2, label=tsa_labels[i])
    ax2.errorbar(snow_bins, winter_offset_mean_b, yerr=winter_offset_std_b, fmt='none', ecolor=tsa_colors[i], alpha=0.3)

# add legend to the plots
#ax1.legend()
ax2.legend()
ax1.set_xlabel('Snow depth (cm)')
ax1.set_ylabel('Winter offset (°C)')
ax2.set_xlabel('Snow depth (cm)')
#ax2.set_ylabel('Winter offset (°C)')
ax1.set_title(str(os.environ['run_name_a']))
ax2.set_title(str(os.environ['run_name_b']))

# set y-axis limits
ax1.set_ylim([0, 30])
ax2.set_ylim([0, 30])

plot_name = output_dir + "snow_insulation.diff." + os.environ['run_name_a'] + "-" + os.environ['run_name_b']
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()
