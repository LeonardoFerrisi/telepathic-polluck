import preprocessing
from sys import argv
import numpy as np
import main

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

	return int(seed)

def create_image_from_eeg(filename):

	"""
	Read in csv, preprocess, and pass a seed into the art generator.
	
	"""
	
	filtered_data = preprocessing.filter_signal(filename)
	seed = generate_seed(filtered_data)
	
	print("Generating image.............")
	main.single_img_generation(RESOLUTION,seed,LAYERS,WIDTH,ACTIVATION)
	

if __name__ == "__main__":

	if (len(argv) != 2):
		raise ValueError("Correct usage: create.py [filename]")
		
	create_image_from_eeg(argv[1])
	
	print("Done!")
