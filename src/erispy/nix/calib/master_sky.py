import numpy as np
from astropy.io import fits
from ..data import get_calib_data, get_science_data
from ..calib.detector import correct_offset

def create_master_sky(flist, master_dark,loflat, output='mastersky.fits'):
	""" Given a list of sky files and a master dark, calculates a fake
		offset mask used that can be used as a flat field
	"""
		 
	dark  = get_calib_data(master_dark)
	lflat = get_calib_data(loflat)[2:,:]+1e-10

	sky_frame = np.zeros_like(get_science_data(flist[0])[0],dtype=np.float64)

	nframes = 0
	for f in flist:
		
		data = get_science_data(f)
		
		for frame in data:
			sky_add, _ = correct_offset(frame-dark, nrows=-1,percentile=40)
			sky_frame += sky_add/lflat
			nframes+=1
			
	primary_hdu = fits.PrimaryHDU(data=sky_frame/nframes)
    
    # Create an HDU list and write it to a FITS file
	hdul = fits.HDUList([primary_hdu])
	hdul.writeto(output, overwrite=True)
	hdul.close()