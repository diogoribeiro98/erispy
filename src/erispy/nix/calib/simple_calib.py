import os
import numpy as np
from astropy.io import fits
from ..data import get_science_data, get_calib_data, save_to_fits
from  .detector import correct_offset

#Do simple calibration
def simple_calibration(data_file,masterdark,masterflat,mastersky):
	""" Given a datafile, calibrates it by subtracting a dark and dividing by a flat
	"""
	
	print('Calibrating file: ', os.path.basename(data_file) )
	dark  = get_calib_data(masterdark)
	flat  = get_calib_data(masterflat)[:-2]
	sky = get_science_data(mastersky)
	output_name = os.path.basename(data_file)[:-5] + "_simple_calib.fits"

	#Create a copy of the original file where we will make the changes
	print('Creating a copy of the original file')
	with fits.open(data_file) as hdul:
		hdul.writeto(output_name, overwrite=True)

	print('Calibrating frames')
	with fits.open(output_name, mode='update') as hdul:
		
		#Acess science data
		data = hdul[0].data-dark
		
		for idx,frame in enumerate(data):
			image_calibrated,_ = correct_offset(frame, nrows=-1,percentile=20)
			data[idx] = image_calibrated/flat-sky 
			
			#hdul[0].data[idx] = image_calibrated/flat-sky 
		
		hdul[0].data = data.astype(np.float32)
		print('Saving calibrated data')
		hdul.flush()  

	print('Done')