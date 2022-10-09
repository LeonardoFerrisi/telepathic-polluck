import numpy as np
import pandas as pd
from sys import argv

#CHANNELS = {}
CHANNELS = [1,2,3,4,5,6,7,8]
SAMPLE_RATE = 250 # 250Hz

def make_timestamps(length,fs=SAMPLE_RATE):

	"""
	Create timestamps based on sample rate.
	
	Return : Numpy array of floats
	"""
	
	if (fs <= 0): # check for valid sample rate
		raise ValueError("Invalid Sample Rate {} Hz.".formate(fs))
	
	timevec = [] # time vector (output)
	dt = fs**(-1) # timestep
	
	for index in range(length): # built output vector
		
		timevec.append(index*dt)
		
	return np.asarray(timevec)
	
def add_timestamps_csv(filename):

	data = pd.read_csv(filename) # read csv
	
	length = np.shape(data)[0] # get length to make time vec
	
	t = make_timestamps(length)
	
	# add timevec to columns
	data.insert(0,column='Time (s)',value=t)
	
	# save csv
	i = filename.find(".csv")
	new_name = filename[0:i]+"_neuropype_format.csv"
	data.to_csv(new_name)
	
	
if __name__ == "__main__":

	if (len(argv) < 2):
		raise ValueError("Call as : format_csv.py [filename.csv]")
		
	add_timestamps_csv(argv[1])
