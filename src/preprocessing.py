import pandas as pd
from scipy import signal
from sys import argv
import numpy as np
from scipy.fft import fft,fftfreq

HIGHPASS_THRESHOLD = 1
LOWPASS_THRESHOLD = 60
NOTCH_BAND = [58,62]
SAMPLE_RATE = 250
NUM_CHAN = 8

ARTEFACT_THRESHOLD_mV = 4 # do we want artefact rejection?

def filter_signal(filename,filter_order=2):

	"""
	Basic filtering of EEG data from a CSV file.
	
	Return : numpy array of filtered data
	
	"""
	
	data = pd.read_csv(filename)
	data = data.iloc[:,0:NUM_CHAN] # get only interesting columns
	data = np.transpose(np.asarray(data)) # make data shape : channels x time


	# highpass filter 0.1Hz
	print("Applying high pass filter at {} Hz.".format(HIGHPASS_THRESHOLD))
	b,a = signal.butter(filter_order,HIGHPASS_THRESHOLD,btype='highpass',fs=SAMPLE_RATE)
	data_filt = signal.filtfilt(b,a,data)

	#import pdb;pdb.set_trace()
	
	# lowpass filter 100Hz
	print("Applying high pass filter at {} Hz.".format(LOWPASS_THRESHOLD))
	b,a = signal.butter(filter_order,LOWPASS_THRESHOLD,btype='lowpass',fs=SAMPLE_RATE)
	data_filt = signal.filtfilt(b,a,data_filt)

	# notch filter 59-61Hz
	print("Applying high pass filter at from {} to {} Hz.".format(NOTCH_BAND[0],NOTCH_BAND[1]))
	b,a = signal.butter(filter_order,NOTCH_BAND,btype='bandstop',fs=SAMPLE_RATE)
	data_filt = signal.filtfilt(b,a,data_filt)
	
	# artefact rejection?
	
	# mean shift? normalize?
	
	print("Filtering complete!")
	
	return data_filt

def bandpower(band,data):

	"""
	Get power spectra of a specific frequency band.
	Data must be shaped : channel x time.
	
	Returns : Numpy array of power values (mV^2) : channel x frequency
	"""
	
	print("Extracting bandpower from {} to {} Hz.".format(band[0],band[1]))
	
	yf = fft(data)
	N = np.shape(data)[1]
	xf = fftfreq(N,1/SAMPLE_RATE)
	try:
		low_i = np.where(xf>=band[0])[0][0]
		high_i = np.where(xf>=band[1])[0][0]
	except:
		raise ValueError("Issue in extracting bandpower! Desired frequency out of range.")
		
	return yf[:,low_i:high_i]

def show_spect(data):

	"""
	Show spectral activity of data.
	
	Data must be shaped : channel x time
	"""
	N = np.shape(data)[1]
	yf = fft(data)
	xf = fftfreq(N,1/SAMPLE_RATE)

	import matplotlib.pyplot as plt
	plt.plot(xf,np.abs(np.mean(yf,axis=0)),'b')
	plt.xlabel("Frequency (Hz)")
	plt.ylabel("Power (mV^2)")
	plt.show()
