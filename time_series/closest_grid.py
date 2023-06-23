import netCDF4 as nc
import numpy as np

# Open the NetCDF file
file_path = "57_DOM02_001.clm2.h0.2022-01-01-00000.nc"
dataset = nc.Dataset(file_path, 'r')

# Read latitude and longitude variables
lat = dataset.variables['lat'][:]
lon_360 = dataset.variables['lon'][:]
lon = np.where(lon_360 > 180, lon_360 - 360, lon_360)

# Target coordinates
target_lat = 72.369555
target_lon = 126.475111

# Calculate the distance between target coordinates and each pixel
lat_diff = lat - target_lat
lon_diff = lon - target_lon
distance = np.sqrt(lat_diff ** 2 + lon_diff ** 2)

# Find the index of the closest pixel
closest_index = np.argmin(distance)

# Get the latitude and longitude values of the closest pixel
closest_lat = lat[closest_index]
closest_lon = lon[closest_index]

# Close the NetCDF file
dataset.close()

# Print the index and coordinates of the closest pixel
print("Closest Pixel Index:", closest_index)
print("Closest Pixel Latitude:", closest_lat)
print("Closest Pixel Longitude:", closest_lon)
