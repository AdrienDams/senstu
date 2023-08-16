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

variable = "SNOW_DEPTH"
folder = os.environ['cegio'] + "/data/" + os.environ['run_name'] + "/monthly/snow_depth/"
output_dir = os.environ['senstu'] + "/figures/effective_snow/"
os.makedirs(output_dir, exist_ok=True)

ctsmfile = folder + "SNOW_DEPTH.remap.period.10.nc" # october is first one
dctsm = nc.Dataset(ctsmfile, 'r') # read only
snow_eff = dctsm.variables[variable][0,:,:]*6 # remove useless dimension
sum_month = 0

month_seq = [11, 12, 1, 2, 3]
real_seq = [2, 3, 4, 5, 6]
for i in range(5):
	ctsmfile = folder + "SNOW_DEPTH.remap.period.{:02d}.nc".format(month_seq[i])
	dctsm = nc.Dataset(ctsmfile, 'r') # read only
	snow = dctsm.variables[variable][0,:,:] # remove useless dimension
    #
	snow_eff += (snow*(7-real_seq[i]))
	sum_month += real_seq[i]

snow_eff = snow_eff/sum_month

# extract variables
lon = dctsm.variables['lon']
lat = dctsm.variables['lat']

## Mapping diff
sbounds = np.linspace(0,0.5,6)
fig = plt.figure(figsize=[8, 8], constrained_layout=True)

ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo())

# shade variables
filled = ax.pcolormesh(lon, lat, snow_eff, cmap='RdBu',
                        transform=ccrs.PlateCarree(), shading='auto', norm=colors.BoundaryNorm(sbounds, 256))
# extent map
ax.set_extent([-180, 180, 90, 57], ccrs.PlateCarree())

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
cbar = fig.colorbar(filled, boundaries=sbounds, extend='max')
cbar.set_label(r"effective snow", rotation=-90, labelpad=13)

plot_name = output_dir + "effective_snow." + os.environ['run_name']
plt.savefig(plot_name +'.png', format='png', bbox_inches='tight', dpi=300)
plt.close()
