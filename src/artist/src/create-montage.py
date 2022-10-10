from sys import argv
import pdb
import imageio
import preprocessing
import main
import numpy as np
import os
from pathlib import Path

IMG_NUM = 'single'
RESOLUTION = [1920,1080]
LAYERS = 6
WIDTH = 5
ACTIVATION = 'tanh'

FREQ_BANDS = {"Alpha":[8,13],"Beta":[13,30],"Delta":[1,4],"Theta":[4,8],"Gamma":[30,100]}

SAMPLE_RATE = 250

def generate_seed(data,method='time-series'):

	"""
	Generate seed from EEG data by extracting power from freq. bands
	
	Returns an integer seed.
	"""
	
	seed = ''
	
	if method == 'power':
	
		for band in list(FREQ_BANDS.keys()):
			
			bandpower = preprocessing.bandpower(FREQ_BANDS[band],data)
			channel_mean_pow = np.mean(bandpower,axis=0)
			#import pdb; pdb.set_trace()
			
			seed += str(int(np.mean(channel_mean_pow)) % 10)
			#bandmean = 10 * np.mean(channel_mean_pow) / np.linalg.norm(channel_mean_pow) # normalize
			#seed += str(int(bandmean)) 

	if method == 'time-series':
	
		print("Using time-series to generate seed since chunk size is too small for fft!")
		
		for channel in range(np.shape(data)[0]):
		
			x = data[channel,:]
			
			# seed_digit = np.abs(np.mean(x))
			# pdb.set_trace()
			# seed_digit = 10 * seed_digit / np.linalg.norm(seed_digit)
			
			seed_digit = (x - np.min(x)) / (np.max(x) - np.min(x))
			#pdb.set_trace()
			seed_digit = np.mean(seed_digit)
			print(seed_digit)
			seed += str(int(seed_digit * 10))
	
	return int(seed)


def create_montage_from_eeg(filename,chunk_size=10,loop=True):

	"""
	Read in csv, preprocess, and pass a seed into the art generator.
	Do this several times to create multiple images and collate into a montage video.
	Chunk_size (seconds) means how many seconds of data to chunk together in one image
	"""
	
	print("Separating data into chunks of approx. {} seconds.".format(chunk_size))
	
	filtered_data = preprocessing.filter_signal(filename)

	chunk_samples = SAMPLE_RATE * chunk_size
	chunk_indices = np.linspace(0,len(filtered_data[1]),int(np.shape(filtered_data)[1]/chunk_samples))
	num_chunks = len(chunk_indices)
	
	#pdb.set_trace()
	
	csv_i = filename.find('.csv')
	gif_name = filename[0:csv_i]+'.gif'
	
	image_data = []
	if (not loop):
		blank_start = list(np.zeros([1080,1920,3]))
		image_data.append(blank_start)
	
	for current_chunk,chunk_i in enumerate(chunk_indices[0:-1]):
		print("-----------------------------------------------------\n\n\n")
		#pdb.set_trace() #check chunk_indices and stuff
		chunk = filtered_data[:,int(chunk_i):int(chunk_i)+chunk_samples]
		print("Generating image {} of {} in montage........".format(current_chunk+1,num_chunks-1))

		if (chunk_size < 1):
			seed = generate_seed(chunk,method='time-series')
		
		else:
			seed = generate_seed(chunk,method='power')

		jpg_name = main.single_img_generation(RESOLUTION,seed,LAYERS,WIDTH,ACTIVATION)
		#pdb.set_trace() # check name. wdir or ??
		
		image_data.append(imageio.imread('images/'+jpg_name)) # save for gif creation
		
		print("-----------------------------------------------------\n\n\n")
		
	output_directory_fullpath = os.path.join(str(Path.cwd()), 'montages')
	Path(output_directory_fullpath).mkdir(parents=True, exist_ok=True)
	file_full_path = os.path.join(output_directory_fullpath, gif_name)

	imageio.mimwrite(file_full_path,image_data,format='.gif',fps=3)
	
if __name__ == "__main__":

	if (len(argv) > 2):
		if (len(argv) > 3):
			create_montage_from_eeg(argv[1],int(argv[2]),bool(argv[3]))
		else:
			create_montage_from_eeg(argv[1],int(argv[2]))
	else:
		raise ValueError("Correct usage: create.py [filename] [chunk length (s)]")
		

	
	print("Done!")

