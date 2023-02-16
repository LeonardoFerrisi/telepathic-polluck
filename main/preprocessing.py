import pandas as pd
from scipy import signal
from sys import argv
import numpy as np
from scipy.fft import fft,fftfreq
import pdb

from brainflow.data_filter import DataFilter, AggOperations, FilterTypes, NoiseTypes, WindowOperations, DetrendOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets

HIGHPASS_THRESHOLD = 1
LOWPASS_THRESHOLD = 60
NOTCH_BAND = [58,62]
SAMPLE_RATE = 250
NUM_CHAN = 8

ARTEFACT_THRESHOLD_mV = 4 # do we want artefact rejection?

def filter_signal(filename="", datastream=None, filter_order=2):

	"""
	Basic filtering of EEG data from a CSV file.
	
	Return : numpy array of filtered data
	
	"""
	if filename != "" and datastream is None:
		data = pd.read_csv(filename)
	elif datastream is not None and filename == "":
		ds_transposed = datastream.transpose()
		if type(datastream) == np.ndarray: data = pd.DataFrame(data=ds_transposed)
		else: data = ds_transposed
	else:
		raise ValueError("filename and datastream cannot both be None")
		
	data = data.iloc[:,0:NUM_CHAN] # get only interesting columns
	#pdb.set_trace()
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
	
	print(data_filt)

	print("Filtering complete!")
	
	return data_filt

def bandpower(band,data, boardID):

	"""
	Get power spectra of a specific frequency band.
	Data must be shaped : channel x time.
	
	Returns : Numpy array of power values (mV^2) : channel x frequency
	"""
	
	print("Extracting bandpower from {} to {} Hz.".format(band[0],band[1]))
	
	sampling_rate = BoardShim.get_sampling_rate(boardID)
	nfft = DataFilter.get_nearest_power_of_two(sampling_rate)

	powers = []
	for i, channel in enumerate(data):
		DataFilter.detrend(data[i], DetrendOperations.LINEAR.value)
		psd = DataFilter.get_psd_welch(data[i], nfft, nfft // 2, sampling_rate,
                                   WindowOperations.BLACKMAN_HARRIS.value)
		power = DataFilter.get_band_power(psd, band[0], band[1])
		powers.append(power)

	avg_power = np.mean(powers)
	print("*************************************************************")
	print(f"Average Power for range: {band[0]}, {band[1]}: {avg_power}")
	print("*************************************************************")

	return avg_power


	# yf = fft(data)
	# yf = np.abs(yf) # get power
	# N = np.shape(data)[1]
	# xf = fftfreq(N,1/SAMPLE_RATE)
	# try:
	# 	low_i = np.where(xf>=band[0])[0][0]
	# 	high_i = np.where(xf>=band[1])[0][0]
	# except:
	# 	raise ValueError("Issue in extracting bandpower! Desired frequency out of range.")
		
	# return yf[:,low_i:high_i]
	
def show_spect(data):

	"""
	Show spectral activity of data.
	
	Data must be shaped : channel x time
	"""
	N = np.shape(data)[1]
	yf = fft(data)
	xf = fftfreq(N,1/SAMPLE_RATE)

	import matplotlib.pyplot as plt

	
	plt.plot(xf[0:N//2], np.abs(np.mean(yf,axis=0))[0:N//2] ,'b')
	plt.xlabel("Frequency (Hz)")
	plt.ylabel("Power (mV^2)")
	plt.title("Spectra")
	plt.show()
