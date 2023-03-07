import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.colors as colors
from matplotlib.colors import TwoSlopeNorm
import os
import sys

folder = os.environ['scratch_dir'] + "/snow_insulation/"
zero_abs = 273.15

# select stations
index_table = np.genfromtxt(os.environ['cegio'] + "/evaluation/stations/stations_ctsm_indexes.t2m.txt", delimiter=" ", dtype=int)
stations = index_table[:,0]

# open files and extract variables
ds_a = folder + os.environ['run_name_a'] + ".nc"
ds_b = folder + os.environ['run_name_b'] + ".nc"
data_a = nc.Dataset(ds_a,'r') # read only
data_b = nc.Dataset(ds_b,'r') # read only

tsa_a = data_a.variables["TSA"][:,stations].copy()-zero_abs
tsa_b = data_b.variables["TSA"][:,stations].copy()-zero_abs
tsoi_a = data_a.variables["TSOI"][:,2,stations].copy()-zero_abs # 2 = take at 9 cm
tsoi_b = data_b.variables["TSOI"][:,3,stations].copy()-zero_abs # 3 = take at 11 cm (for CLM45 run)
snow_a = data_a.variables["SNOW_DEPTH"][:,stations].copy()
snow_b = data_b.variables["SNOW_DEPTH"][:,stations].copy()
snow_a = snow_a[:,:]*100 # convert into cm
snow_b = snow_b[:,:]*100 # convert into cm

data_a.close()
data_b.close()

# calculate winter_offset
winter_offset_a = tsoi_a[:,:] - tsa_a[:,:]
winter_offset_b = tsoi_b[:,:] - tsa_b[:,:]

# Define the snow bin edges
snow_bin_edges = np.arange(0, 101, 10)
snow_bins = np.arange(5,96,10)

# Loop over the snow bins and calculate the winter_offset_a average for each bin
winter_offset_mean_a = np.zeros(np.size(snow_bins))
winter_offset_mean_b = np.zeros(np.size(snow_bins))
winter_offset_std_a = np.zeros(np.size(snow_bins))
winter_offset_std_b = np.zeros(np.size(snow_bins))

for i in range(0, len(snow_bins)):
	idx_a = np.where((snow_a >= snow_bin_edges[i]) & (snow_a < snow_bin_edges[i+1]))
	idx_b = np.where((snow_a >= snow_bin_edges[i]) & (snow_a < snow_bin_edges[i+1]))
	winter_offset_mean_a[i] = np.nanmean(winter_offset_a[idx_a])
	winter_offset_mean_b[i] = np.nanstd(winter_offset_b[idx_b])
	winter_offset_std_a[i] = np.nanstd(winter_offset_a[idx_a])
	winter_offset_std_b[i] = np.nanstd(winter_offset_b[idx_b])

# create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

# plot a
ax1.scatter(snow_bins, winter_offset_mean_a, color='blue', linewidth=2)
ax1.errorbar(snow_bins, winter_offset_mean_a, yerr=winter_offset_std_a, fmt='none', ecolor='blue')

# plot b
ax2.scatter(snow_bins, winter_offset_mean_b, color='blue', linewidth=2)
ax2.errorbar(snow_bins, winter_offset_mean_b, yerr=winter_offset_std_b, fmt='none', ecolor='blue')

# set y-axis limits
ax1.set_ylim([0, 25])
ax2.set_ylim([0, 25])

# set titles and labels
ax1.set_title(str(os.environ['run_name_a']))
ax2.set_title(str(os.environ['run_name_b']))
ax1.set_ylabel('Winter Offset (°C)')
ax2.set_ylabel('Winter Offset (°C)')
ax2.set_xlabel('Snow Depth (m)')

# show plot
plt.show()
