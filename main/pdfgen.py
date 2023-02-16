# importing modules
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
import os

import numpy as np
from scipy.fft import fft,fftfreq
import matplotlib.pyplot as plt


from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter, AggOperations, FilterTypes, NoiseTypes
import matplotlib.pyplot as plt
import pandas as pd
import random

def generate_raw_plot(filename:str, boardID:int, data:pd.DataFrame, transpose:bool=False, descale_weight:int=10000, title:str='60 seconds of Raw EEG Data', show=True):    
    """
    Generate a plot of the raw EEG data

    Data should be formatted in the format data[channels, :] - otherwise, set transpose to True
    """
    if transpose: data = np.transpose(data) # data is typically stored in a trasnposed format
    print(f"Data shape is {data.shape}")
    # data = data[channels, :]
    num_channels, num_samples = data.shape
    # Calculate the sampling rate (assuming the data is recorded at 250 Hz)
    sampling_rate = BoardShim.get_sampling_rate(boardID)

    # Create a time vector for the x-axis
    time = np.arange(num_samples) / sampling_rate

    channels = BoardShim.get_eeg_channels(boardID)
    boardINFO = BoardShim.get_board_descr(boardID)
    channelNames = boardINFO["eeg_names"]


    if type(channelNames) is str: channelNames = channelNames.split(",")


    # Get only relevant data
    
    
    print(f"Found {len(channels)} channels")

   
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
    print("SAVING PLOT")
    plt.savefig(filename)
    if show: plt.show()
    plt.clf()

def show_spect(data, filename, sampling_rate):

    """
    Show spectral activity of data.
    
    Data must be shaped : channel x time
    """
    N = np.shape(data)[1]
    yf = fft(data)
    xf = fftfreq(N,1/sampling_rate)
    plt.plot(xf[0:N//2], np.abs(np.mean(yf,axis=0))[0:N//2] ,'b')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (mV^2)")
    plt.title("Spectra")
    print("saving spectra")
    plt.savefig(filename)
    plt.clf()

def generate_report(
    data=None,
    dir_path:str=None,
    font_dir:str=None,
    subjectName:str="default",
    bandpowers:dict=None,
    subjectfilepath:str=None,
    desc:str=None,
    boardID:int=None
):
    if dir_path is None: dir_path = os.path.dirname(os.path.realpath(__file__))
    if font_dir is None: font_dir = os.path.dirname(os.path.realpath(__file__))
    print(f"\nGenerating Report. Directory path is {dir_path}\n")
    
    fileName = dir_path+os.sep+f'{subjectName}_report.pdf'
    documentTitle = subjectName+"_report"

    title = 'Union Neurotech 2023'
    subTitle = 'Thinking About U: Brain Generated Abstract Imagery Prototype'
    logo = font_dir+os.sep+"assets"+os.sep+'logo.png'

    # define some parameters
    MARGIN = 36.0   
    page_edge_horizontal = letter[0]
    page_edge_vertical = letter[1]
    page_margin_left = MARGIN
    page_margin_right = page_edge_horizontal - MARGIN
    page_margin_bottom = MARGIN
    page_margin_top = page_edge_vertical - MARGIN

    # creating a pdf object
    pdf = canvas.Canvas(fileName, pagesize=letter)

    # Set the title
    pdf.setTitle(documentTitle)

    # registering a external font in python
    pdfmetrics.registerFont(
        TTFont('Timeless', font_dir+os.sep+"assets"+os.sep+'Timeless.ttf')
    )
    pdfmetrics.registerFont(
        TTFont('Timelessbd', font_dir+os.sep+"assets"+os.sep+'Timeless-Bold.ttf')
    )

    # creating the title by setting it's font 
    # and putting it on the canvas
    pdf.setFont('Timelessbd', 44)
    pdf.drawString(120, 715, title)
    # drawing a logo
    pdf.drawInlineImage(logo, 40, 700, width=60, height=60)

    # creating the subtitle by setting it's font, 
    # colour and putting it on the canvas
    # pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont("Timelessbd", 18)
    pdf.drawCentredString(300, 670, subTitle)

    def draw_divider(y):
    # drawing a line - divider
        pdf.line(page_margin_left, y, page_margin_right, y)
    draw_divider(660)

    content = [
        f"Name: {subjectName}"
    ]

    if desc is not None: content.append(f"Description: {desc}")
    if boardID is not None:
        boardinfo = BoardShim.get_board_descr(boardID)
        boardname = boardinfo["name"]
        boardchannels = boardinfo["eeg_names"]
        content.append(f"Device Model: {boardname}")
        content.append(f"Device Channels: {boardchannels}")

    if bandpowers is not None:
        for key, value in bandpowers.items():
            content.append(f"{key}: {value}")

    # creating a multiline text using
    # textline and for loop
    text = pdf.beginText(page_margin_left, 620)
    text.setFont("Timeless", 20)
    
    for line in content:
        text.textLine(line)
        
    pdf.drawText(text)


    
            

    # Put brainwaves infographic
    brainwaves_info = os.path.dirname(os.path.realpath(__file__))+os.sep+"assets"+os.sep+"brainwaves.png"
    pdf.drawInlineImage(brainwaves_info, page_margin_right-200, 400, width=200, height=250)

    # Create EEG chart


    # Create Spectra Chart
    if data is not None:
        spectra_filepath=dir_path+os.sep+"graphs"+os.sep+documentTitle+str(random.randint(10000, 99999))+"_spectra.png"
        sample_rate = BoardShim.get_sampling_rate(boardID)
        show_spect(data, spectra_filepath, sample_rate)
        pdf.drawInlineImage(spectra_filepath, page_margin_right-200, 300, width=200, height=250)

        # Create Raw EEG chart
        raw_plot_filepath=dir_path+os.sep+"graphs"+os.sep+documentTitle+str(random.randint(10000, 99999))+"_raweeg.png"
        generate_raw_plot(raw_plot_filepath, boardID, data)
        pdf.drawInlineImage(raw_plot_filepath, page_margin_right-200, 200, width=200, height=250)

   

    # saving the pdf
    pdf.save()

    print("\nDone!\n")
    print(f"Report is available at {fileName}")


if __name__ == "__main__":
    generate_report(dir_path="generated"+os.sep+"reports", subjectName="Leonardo", desc="A cat", boardID=22)