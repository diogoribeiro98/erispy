import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from astropy.visualization import (PercentileInterval, AsinhStretch, ImageNormalize, LogStretch)

from .data import get_science_data

def plot_file_frame(file, output_folder='./figures/',  frame=0):

	output_name = output_folder + os.path.basename(file)[:-5] + "_frame_{}.png".format(frame)
	data = get_science_data(file).astype(np.float32)
	image = data[frame]
	upper_limit = np.percentile(np.nan_to_num(image, nan=0.0), 99.95)

	fig, ax = plt.subplots(figsize=(10, 10),dpi=300)
	imshow_settings = { 'cmap' : 'cubehelix', 'norm': LogNorm(vmin=0.99, vmax=upper_limit), 'origin': 'lower'}

	ax.imshow(image, **imshow_settings)
	ax.set_title("Source Image")
	fig.savefig(output_name)
	plt.close()

def plot_data_with_zoomin(data,x0,y0,w,percentile=99.95, cmap='gray'):
	
	cmap = plt.cm.gray  # Choose a colormap suitable for astronomical data
	cmap.set_bad(color='black')  # Optionally, set NaN color to black

	#stretch = AsinhStretch()  # Try LogStretch, SqrtStretch, etc. to see different effects
	stretch = LogStretch()#, SqrtStretch, etc. to see different effects
	interval = PercentileInterval(percentile)  # Cuts off outliers at the extremes

	imshow_settings = { 
		'cmap' : cmap, 
		'norm': ImageNormalize(data, interval=interval, stretch=stretch), 
		'origin': 'lower'}

	fig, (ax1,ax2) = plt.subplots(ncols=2, figsize=(10,10),dpi=150)
	ax1.imshow(data, **imshow_settings)
	ax2.imshow(data, **imshow_settings)

	ax2.set_xlim(x0-w/2,x0+w/2)
	ax2.set_ylim(y0-w/2,y0+w/2)

	return fig, (ax1,ax2)


def plot_in_axis(ax,data, percentile=99.95, cmap='gray'):
	
	stretch = AsinhStretch()  # Try LogStretch, SqrtStretch, etc. to see different effects
	interval = PercentileInterval(percentile)  # Cuts off outliers at the extremes

	imshow_settings = { 
		'cmap' : cmap, 
		'norm': ImageNormalize(data, interval=interval, stretch=stretch), 
		'origin': 'lower'}

	ax.imshow(data, **imshow_settings)
	
	return
