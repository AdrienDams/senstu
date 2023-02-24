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

var1 = os.environ['var1']
var2 = os.environ['var2']
var3 = os.environ['var3']

# output
output_dir = os.environ['senstu'] + "/figures/soil_hum/"
os.makedirs(output_dir, exist_ok=True)

# open files and extract variables

file_var1_a = sys.argv[1]
file_var2_a = sys.argv[2]
file_var3_a = sys.argv[3]
file_var1_b = sys.argv[4]
file_var2_b = sys.argv[5]
file_var3_b = sys.argv[6]

dfile_var1_a = nc.Dataset(file_var1_a, 'r') # read only
dfile_var2_a = nc.Dataset(file_var2_a, 'r')
dfile_var3_a = nc.Dataset(file_var3_a, 'r')
dfile_var1_b = nc.Dataset(file_var1_b, 'r')
dfile_var2_b = nc.Dataset(file_var2_b, 'r')
dfile_var3_b = nc.Dataset(file_var3_b, 'r')


var1_a = dfile_var1_a.variables[var1][0,:,:] # remove useless dimension
var2_a = dfile_var2_a.variables[var2][0,:,:]
var3_a = dfile_var3_a.variables[var3][0,:,:]
var1_b = dfile_var1_b.variables[var1][0,:,:]
var2_b = dfile_var2_b.variables[var2][0,:,:]
var3_b = dfile_var3_b.variables[var3][0,:,:]

lon = dfile_var1_a.variables['lon']
lat = dfile_var1_a.variables['lat']

# make diff
diff_var1 = var1_a-var1_b
diff_var2 = var2_a-var2_b
diff_var3 = var3_a-var3_b

# Mapping diff
# Set up your figure
fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(15, 15), subplot_kw={'projection': ccrs.NorthPolarStereo()})
fig.subplots_adjust(hspace=0.5)

data = [var1_a, var2_a, var3_a,
		var1_b, var2_b, var3_b,
		diff_var1, diff_var2, diff_var3]
titles = [var1, var2, var3,
		'', '', '',
		'difference', 'difference', 'difference']


for ax, var, title in zip(axs.flat, data, titles):# set colorbar limits
	# Set colorbar limits
	vmax = np.ceil(np.percentile(np.abs(var.compressed()), 90))

	# Shade variables
	filled = ax.pcolormesh(lon, lat, var, cmap='RdBu_r', norm=TwoSlopeNorm(vcenter=0., vmax=vmax, vmin=-vmax),
	transform=ccrs.PlateCarree(), shading='auto')
	# extent map
	ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

	ax.set_title(title)

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
	#gl = ax.gridlines(draw_labels=True)

	# legend
	cbar = fig.colorbar(filled, ax=ax, extend='both', fraction=0.05, orientation='horizontal')

plot_name = output_dir + os.environ['month'] + ".soil_hum"
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight')
plt.close()
