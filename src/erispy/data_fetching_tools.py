import os
from astropy.io import fits

def get_file_list(directory, category, type, DIT=0.0):
	"""Returns the list of fits files with a specific category and type

	Args:
		directory (string): Path to directory
		category  (string): caterogy associated with the 'HIERARCH ESO DPR CATG' keyword
		type      (string): type associated with the 'HIERARCH ESO DPR TYPE' keyword

	Returns:
		array: list of files found
	"""	

	fits_files_with_keyword = []

	for file in os.listdir(directory):
		if file.endswith('.fits'):			
			#Get file's absolute path
			file_path = os.path.abspath(os.path.join(directory, file))

			#Check if the file is of the desired category    
			try:
				with fits.open(file_path) as hdul:

					if (hdul[0].header['HIERARCH ESO DPR CATG'] == category) and (hdul[0].header['HIERARCH ESO DPR TYPE'] == type):
						
						if (DIT == 0.0) or (hdul[0].header['HIERARCH ESO DET SEQ1 DIT'] == DIT):
							fits_files_with_keyword.append(file_path)
			except Exception as e:
				print('Error: {}'.format(e))

	return fits_files_with_keyword

def print_size_in_mb(data):
	print('Size of science data: ', data.nbytes / (1024 * 1024), 'Mb')
	return