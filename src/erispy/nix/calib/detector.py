import numpy as np

def correct_offset(data,nrows=2,percentile=25):
	""" Given a data matrix, calculates the average of 64 columns (32 pixels each)
		and removes it from the original data depending on the percentile level of the data
	"""

	#From the NIX pipeline manual we have 
	ncols=64
	colsize=32

	data = np.nan_to_num(data, nan=1e10).astype(np.float64)

	if nrows==-1:
		combined_rows = data[:, :]      
		nrows = np.shape(data)[0]   
	else:
		combined_rows = data[-nrows:, :]         
	
	slits_average = np.zeros(ncols)
	

	#reshaped_data = combined_rows.reshape(ncols, nrows*colsize)

	detector_slits = combined_rows.T.reshape(ncols,nrows*colsize)

	for idx,slit in enumerate(detector_slits):
		cutoff = np.percentile(slit,percentile)
		lower_values = [x for x in slit if x < cutoff]
		slits_average[idx] = np.mean(lower_values)
	
	#averaged_columns = np.median(averaged_columns,axis=1,keepdims=True)
	
	#Remove offset from data
	offset_data = np.zeros_like(data)
	
	for i in range(0,ncols):
		offset_data[:,i*colsize:(i+1)*colsize] = slits_average[i]

	return data - offset_data , offset_data
