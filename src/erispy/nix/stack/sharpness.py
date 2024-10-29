import numpy as np
from scipy.optimize import curve_fit

#Measure the sharpness of an image
def gaussian_2d(xy, amplitude, xo, yo, sigma_x, sigma_y, offset):
	""" Defines a 2D Gaussian function for curve fitting. """
	x, y = xy
	g = offset + amplitude * np.exp(
		-(((x - xo) ** 2) / (2 * sigma_x ** 2) + ((y - yo) ** 2) / (2 * sigma_y ** 2))
	)
	return g.ravel()

def measure_sharpness(image, star_position, crop_size=15):
	""" Measures sharpness by fitting a Gaussian to a specific star in the image.
		Returns the fitted Gaussian standard deviation (sigma) as a sharpness metric.
	"""
	x, y = star_position
	half_size = crop_size // 2

	# Crop a small region around the star
	sub_image = image[y - half_size : y + half_size, x - half_size : x + half_size]

	# Prepare data for Gaussian fit
	x_vals = np.linspace(0, crop_size - 1, crop_size)
	y_vals = np.linspace(0, crop_size - 1, crop_size)
	x_mesh, y_mesh = np.meshgrid(x_vals, y_vals)

	# Initial guesses for Gaussian parameters
	initial_guess = (sub_image.max(), crop_size / 2, crop_size / 2, 3, 3, sub_image.min())

	try:
		# Fit a 2D Gaussian to the star's region
		popt, _ = curve_fit(gaussian_2d, (x_mesh, y_mesh), sub_image.ravel(), p0=initial_guess)
		
		# Extract fitted Gaussian standard deviations (sigma_x and sigma_y)
		sigma_x, sigma_y = popt[3], popt[4]
		
		# Calculate a combined sharpness metric (average of sigma_x and sigma_y)
		sharpness_metric = (sigma_x + sigma_y) / 2
		return sharpness_metric

	except RuntimeError:
		# If the fit fails, return a high value indicating blurriness
		return float('inf')