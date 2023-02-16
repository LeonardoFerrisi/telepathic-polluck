import matplotlib.pyplot as plt
import numpy as np
import os
import brainflow
from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter, AggOperations, FilterTypes, NoiseTypes
import pandas as pd


def generate_raw_plot(filename:str, boardID:int, data:pd.DataFrame, transpose:bool=True, descale_weight:int=10000, title:str='60 seconds of Raw EEG Data', show=True):    
    """
    Generate a plot of the raw EEG data
    """

    num_samples, num_channels = data.shape
    # Calculate the sampling rate (assuming the data is recorded at 250 Hz)
    sampling_rate = BoardShim.get_sampling_rate(boardID)

    # Create a time vector for the x-axis
    time = np.arange(num_samples) / sampling_rate

    channels = BoardShim.get_eeg_channels(boardID)
    boardINFO = BoardShim.get_board_descr(boardID)
    channelNames = boardINFO["eeg_names"]


    if type(channelNames) is str: channelNames = channelNames.split(",")


    # Get only relevant data
    
    print(data.shape)
    if transpose: data = np.transpose(data) # data is typically stored in a trasnposed format
    data = data[channels, :]
   
    # Filter
    for idx, channel in enumerate(data):
        DataFilter.perform_bandpass(channel, sampling_rate, 2.0, 50.0, 4, FilterTypes.BESSEL.value, 0)
        DataFilter.perform_highpass(channel, sampling_rate, 2.0, 4, FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.perform_lowpass(channel, sampling_rate, 50.0, 5, FilterTypes.CHEBYSHEV_TYPE_1.value, 1)
        DataFilter.remove_environmental_noise(channel, sampling_rate, NoiseTypes.FIFTY.value)

        DataFilter.perform_rolling_filter(channel, 3, AggOperations.MEAN.value)
        
    
    
    weight = 1/descale_weight
    data = data * weight # scale down eeg

    # set the y-axis limits to accommodate 32 channels
    plt.ylim(0, len(channels)+1)


    for i, channel in enumerate(data):
        # add an offset to each channel to separate them vertically
        
        plt.plot(time, channel+(i+1), label='{}'.format(channelNames[i]))

    # Plot the EEG data
    plt.xlabel('Time (seconds)')
    plt.ylabel('Channels')
    plt.title(title)
    plt.legend()
    plt.savefig(filename)
    if show: plt.show()

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = dir_path+os.sep+"muse.csv"
    eeg_data = np.loadtxt(filename)
    generate_raw_plot(filename="test.png", boardID=22, data=eeg_data, transpose=True, descale_weight=5000, show=True)