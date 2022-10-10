import preprocessing
from sys import argv
import numpy as np
import main
import matplotlib.pyplot as plt
from math import random

IMG_NUM = 'single'
RESOLUTION = [1920,1080]
LAYERS = 30
WIDTH = 15
ACTIVATION = 'tanh'

FREQ_BANDS = {"Alpha":[8,13],"Beta":[13,30],"Delta":[1,4],"Theta":[4,8],"Gamma":[30,100]}

def generate_seed(data):

	"""
	Generate seed from EEG data by extracting power from freq. bands
	
	Returns an integer seed.
	"""
	
	seed = ''
	
	for band in list(FREQ_BANDS.keys()):
		
		bandpower = preprocessing.bandpower(FREQ_BANDS[band],data)
		channel_mean_pow = np.mean(bandpower,axis=0)
		#import pdb; pdb.set_trace()
		
		seed += str(int(np.mean(channel_mean_pow)) % 10)
		#bandmean = 10 * np.mean(channel_mean_pow) / np.linalg.norm(channel_mean_pow) # normalize
		#seed += str(int(bandmean)) 

	return int(seed)

def create_image_from_eeg(filename):

	"""
	Read in csv, preprocess, and pass a seed into the art generator.
	
	"""
	
	filtered_data = preprocessing.filter_signal(filename)
	seed = generate_seed(filtered_data)
	
	print("Generating image.............")
	main.single_img_generation(RESOLUTION,seed,LAYERS,WIDTH,ACTIVATION)
	
def convert_rgb(array):
	r = np.max(array) - np.min(array)
	return [255 / (r * (val-np.min)) for val in array]
def create_convolved_image_from_eeg(filename):

	"""
	Read in csv, use the power of alpha, delta, and gamma mapped [0,255] for colour 
	convolve and show
	"""
	
	filtered_data = preprocessing.filter_signal(filename)
	
	# get channel averaged bandpowers!
	alpha_bandpower = np.mean(preprocessing.bandpower(FREQ_BANDS['Alpha'],filtered_data),axis=0)
	alpha_bandpower = convert_rgb(alpha_bandpower)
	
	gamma_bandpower = np.mean(preprocessing.bandpower(FREQ_BANDS['Gamma'],filtered_data),axis=0)
	gamma_bandpower = convert_rgb(alpha_bandpower)
	
	delta_bandpower = np.mean(preprocessing.bandpower(FREQ_BANDS['Delta'],filtered_data),axis=0)
	delta_bandpower = convert_rgb(alpha_bandpower)
	
	x_size = RESOLUTION[0]
	y_size = RESOLUTION[1]
	
	# build image by 
	# randomly sampling from the distribution of power values!
	# so we end up with [alpha,theta,gamma]
	img = np.zeros([x_size,y_size,3])
	
	for row in range(x_size):
		for col in range(y_size):
			
			alpha_val = alpha_bandpower[random.randint(0,len(alpha_bandpower)-1)]
			gamma_val = gamma_bandpower[random.randint(0,len(gamma_bandpower)-1)]
			delta_val = theta_bandpower[random.randint(0,len(delta_bandpower)-1)]
			
			img[row,col] = [alpha_val,gamma_val,delta_val]
	
	plt.show(img)

if __name__ == "__main__":

	if (len(argv) != 2):
		raise ValueError("Correct usage: create.py [filename]")
		
	create_image_from_eeg(argv[1])
	
	print("Done!")
