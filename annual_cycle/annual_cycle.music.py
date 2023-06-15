# compare mean annual cycles

import numpy as np
import pandas as pd
from datetime import date
import os
from os.path import exists
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import sys
from scipy import stats
from miditime.miditime import MIDITime

# OPEN CONTROL DATA (DATA-Import from CSV (12 months for every point))
all_result_ctrl = pd.DataFrame(np.array(
    pd.read_csv(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name_ctrl'] + ".csv",sep=',',header=None)),
                        columns=['year','month','station_lon','station_lat',
                                 'depth','obs','simulation'])

## OPEN EXPERIMENT DATA (DATA-Import from CSV (12 months for every point))
all_result_exp = pd.DataFrame(np.array(
    pd.read_csv(os.environ['cegio'] + "/evaluation/stations/make_figures/extracted_csv/results.tmp." + os.environ['run_name_exp'] + ".csv",sep=',',header=None)),
                        columns=['year','month','station_lon','station_lat',
                                 'depth','obs','simulation'])

# Make data lists
months  = all_result_ctrl['month'].astype(int)
depths  = all_result_ctrl['depth']
obs = all_result_ctrl['obs']

simulations_ctrl  = all_result_ctrl['simulation']
simulations_exp  = all_result_exp['simulation']

# Masked arrays with nan (-9999) values
invalid = -9999
valid_indexes_ctrl = (obs != invalid) & (simulations_ctrl != invalid) & (obs > -50)
valid_indexes_exp = (obs != invalid) & (simulations_exp != invalid) & (obs > -50)

# Define depths you want to extract
depths_to_extract = [20, 80, 160, 320]

# Create empty arrays to store the monthly averages and standard deviations
obs_avg = np.zeros((12, 4))
obs_std = np.zeros((12, 4))
ctrl_avg = np.zeros((12, 4))
ctrl_std = np.zeros((12, 4))
exp_avg = np.zeros((12, 4))
exp_std = np.zeros((12, 4))

# Loop through each month
for month in range(1, 13):
	# Create boolean arrays to filter by month and valid depth
	month_bool = months == month
	valid_depths_bool = np.isin(depths, depths_to_extract)
	#
	# Filter by valid month and depth
	obs_month = obs[month_bool & valid_depths_bool & valid_indexes_ctrl]
	simulations_ctrl_month = simulations_ctrl[month_bool & valid_depths_bool & valid_indexes_ctrl]
	simulations_exp_month = simulations_exp[month_bool & valid_depths_bool & valid_indexes_exp]
	depths_month = depths[month_bool & valid_depths_bool & valid_indexes_ctrl]
	#
	# Calculate monthly averages for each depth
	for i, depth in enumerate(depths_to_extract):
		obs_avg[month-1, i] = np.mean(obs_month[depths_month == depth])
		obs_std[month-1, i] = np.std(obs_month[depths_month == depth])
		ctrl_avg[month-1, i] = np.mean(simulations_ctrl_month[depths_month == depth])
		ctrl_std[month-1, i] = np.std(simulations_ctrl_month[depths_month == depth])
		exp_avg[month-1, i] = np.mean(simulations_exp_month[depths_month == depth])
		exp_std[month-1, i] = np.std(simulations_exp_month[depths_month == depth])

# Shift the data by four months
shift = 8
obs_avg = np.roll(obs_avg, -shift, axis=0)
obs_std = np.roll(obs_std, -shift, axis=0)/6
ctrl_avg = np.roll(ctrl_avg, -shift, axis=0)
ctrl_std = np.roll(ctrl_std, -shift, axis=0)/3
exp_avg = np.roll(exp_avg, -shift, axis=0)+2
exp_std = (np.roll(exp_std, -shift, axis=0)+2)/6

# Instantiate the class with a tempo (120bpm is the default) and an output file destination
mymidi = MIDITime(120, 'exp.mid')

# Convert your time series data into a list of notes
notes = []
for i in range(len(obs_avg)):
    notes.append([i, int(exp_avg[i][0]) + 60, 127, 1])

# Add a track with those notes
mymidi.add_track(notes)

# Output the .mid file
mymidi.save_midi()

exit()

# Define colors for each dataset
obs_color = 'black'
ctrl_color = 'blue'
exp_color = 'green'

# Set up the figure and subplots
fig, axs = plt.subplots(len(depths_to_extract), 1, figsize=(16, 20), sharex=True)
plt.subplots_adjust(hspace=0, wspace=0)

# Loop through each depth
for i, depth in enumerate(depths_to_extract):
	# Plot the obs data
	axs[i].plot(range(1, 13), obs_avg[:, i], color=obs_color, label='Observations')

	# Plot the control data
	axs[i].plot(range(1, 13), ctrl_avg[:, i], color=ctrl_color, label='Control')

	# Plot the experiment data
	axs[i].plot(range(1, 13), exp_avg[:, i], color=exp_color, label='Experiment')

	# Plot the standard deviation for each dataset using fill_between
	axs[i].fill_between(range(1, 13), obs_avg[:, i] - obs_std[:, i], obs_avg[:, i] + obs_std[:, i], alpha=0.2, color=obs_color)
	axs[i].fill_between(range(1, 13), ctrl_avg[:, i] - ctrl_std[:, i], ctrl_avg[:, i] + ctrl_std[:, i], alpha=0.2, color=ctrl_color)
	axs[i].fill_between(range(1, 13), exp_avg[:, i] - exp_std[:, i], exp_avg[:, i] + exp_std[:, i], alpha=0.2, color=exp_color)

	# Add axis labels and title for each subplot
	axs[i].text(-0.2, 4, f'-{depth} cm', rotation=90, verticalalignment='center', fontsize=10)

	# Add y-ticks and tick options
	loc = plticker.MultipleLocator(base=4.0) # this locator puts ticks at regular intervals
	axs[i].yaxis.set_major_locator(loc)
	axs[i].tick_params(direction='in')

	# Add a legend to the first subplot
	if i == 0:
		axs[i].legend(loc='best')

# Add axis label
plt.xticks(range(1, 13), ("Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"))

fig.suptitle('Monthly soil temperature in °C', fontsize=12, y=0.9)

# output
plt.show()

