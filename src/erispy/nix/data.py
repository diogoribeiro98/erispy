import numpy as np
from astropy.io import fits

def get_science_data(file, nanto=0.0):
	with fits.open(file, mode='update') as hdul:
		data = hdul[0].data
	return data

def get_calib_data(file):
	with fits.open(file, mode='update') as hdul:
		data = hdul[1].data
	return data

def get_offset_rows(data, nrows=2):
	lrows  = data[-nrows:, :]    
	return lrows

def save_to_fits(data,fname):
	primary_hdu = fits.PrimaryHDU(data=data)
	hdul = fits.HDUList([primary_hdu])
	hdul.writeto(fname, overwrite=True)
	hdul.close()

	return