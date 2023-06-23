import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.colors as colors
from matplotlib.colors import TwoSlopeNorm
import cartopy
import cartopy.crs as ccrs
import os
import sys

variable = os.environ['variable']

# output
output_dir = os.environ['senstu'] + "/figures/map_diff/" + variable + "/"
os.makedirs(output_dir, exist_ok=True)

# open files and extract variables
file_a = sys.argv[1]
file_b = sys.argv[2]
dfile_a = nc.Dataset(file_a, 'r') # read only
dfile_b = nc.Dataset(file_b, 'r') # read only

file_a = dfile_a.variables[variable][0,:,:] # remove useless dimension
file_b = dfile_b.variables[variable][0,:,:] # remove useless dimension
lon = dfile_a.variables['lon']
lat = dfile_a.variables['lat']

# make diff
diff = file_a - file_b

# Load glacier mask data
mask_file = os.environ['senstu'] + "/map_diff/mask_glacier.nc"
dfile_mask = nc.Dataset(mask_file, 'r')
glacier_mask = dfile_mask.variables['PCT_GLACIER'][:]

# Create masked diff variable
masked_diff = np.ma.masked_where(glacier_mask > 0, diff)

## Mapping diff
fig = plt.figure(figsize=[10, 10], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# set colorbar limits
vmax = np.ceil(np.percentile(np.abs(masked_diff.compressed()), 90))

# shade variables
filled = ax.pcolormesh(lon, lat, masked_diff, cmap='RdBu_r', norm=TwoSlopeNorm(vcenter=0., vmax=vmax, vmin=-vmax),
                       transform=ccrs.PlateCarree(), shading='auto')

# Set masked values to white
filled.set_facecolor('white')

# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

ax.set_title(os.environ['run_name_a'] + " - " + os.environ['run_name_b'], fontsize=16)

# draw land and ocean
ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.LAND, facecolor="silver")
ax.coastlines(linewidth=0.5, color='black')

# compute a circle in axes coordinates
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# gridlines labels
gl = ax.gridlines(draw_labels=True)

# legend
cbar = fig.colorbar(filled, extend='both', fraction=0.05)
cbar.set_label(os.environ['legendtitle'], rotation=-90, labelpad=13, fontsize=16)

plot_name = output_dir + variable + "." + os.environ['month'] + ".diff." + os.environ['run_name_a'] + "-" + os.environ['run_name_b']
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()

