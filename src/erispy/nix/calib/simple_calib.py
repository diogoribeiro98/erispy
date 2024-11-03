import os
import numpy as np
from astropy.io import fits
from ..data import get_science_data, get_calib_data, get_bpm
from  .detector import correct_offset

#Do simple calibration
def simple_calibration(data_file,masterdark,masterflat,mastersky, threshold=5e3):
	""" Given a datafile, calibrates it by subtracting a dark and dividing by a flat
	"""
	
	print('Calibrating file: ', os.path.basename(data_file) )
	dark  = get_calib_data(masterdark)
	flat  = get_calib_data(masterflat)[:-2]
	sky   = get_science_data(mastersky)
	bpm   = (get_bpm(masterdark) != 0)

	#Correct the flat to avoid dividing by zero
	flat = np.where( np.abs(flat)<1e-2, 1, flat)

	#Output file
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

			#Correct the detector
			image,_ = correct_offset(frame, nrows=-1,percentile=50)
			
			#Correct sky
			image = image/flat - sky

			#Correct put bad pixels to zero
			image[bpm==1] = 0.0

			#Correct hot-pixels
			image[np.abs(sky) > threshold] = 0.0

			#Overwrite file
			data[idx] = image 
					
		hdul[0].data = data.astype(np.float32)
		print('Saving calibrated data')
		hdul.flush()  

	print('Done')