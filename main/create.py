import preprocessing
from sys import argv
import numpy as np
# from main import single_img_generation
# from main import *
import matplotlib.pyplot as plt
import math 
import random
import os
import datetime

DIRNAME = os.path.dirname(__file__)

IMG_NUM = 'single'
RESOLUTION = [1920,1080]
# LAYERS = 30
# WIDTH = 15
LAYERS = 10
WIDTH = 9

# Fewer Layers = Prettier Image
ACTIVATION = 'tanh'

FREQ_BANDS = {"Alpha":[8,13],"Beta":[13,30],"Delta":[1,4],"Theta":[4,8],"Gamma":[30,60]}

### For single image gen
import argparse
import random
from art_net import NumpyArtGenerator
from file_util import save_numpy_image

seed_min = 0
seed_max = 2147483647
layers_min = 0
layers_max = 50
width_min = 0
width_max = 20
default_resolution = (1920, 1080)
OUTPUT_DIRECTORY = "images"

# Single image gen

def single_img_generation(resolution,seed,layers,width,activation, output_dir='', username='', startfile=True):

    generator = NumpyArtGenerator(resolution,seed,layers,width,activation)
    numpy_image = generator.run(True)

    if output_dir == '':
        output_dir = OUTPUT_DIRECTORY
    
    name = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    filename = username + "_" + name + "_seed-" + str(seed) + "_" + ".png"
    # filename = str(generator) + ".png"
    save_numpy_image(numpy_image, filename, output_dir)

    # using pillow
    file_full_path = os.path.join(output_dir, filename)


    if startfile:
        os.startfile(file_full_path)
    
    return filename


# ######################

def generate_seed(data, weight=10):

    """
    Generate seed from EEG data by extracting power from freq. bands
    
    Returns an integer seed.
    """
    
    seed = ''
    
    bands = []
    bands_norm = []
    weighted_bands_norm = []

    for band in list(FREQ_BANDS.keys()):
        
        bandpower = preprocessing.bandpower(FREQ_BANDS[band],data)


        channel_mean_pow = np.mean(bandpower,axis=0)
        
        # if channel_mean_pow == []:
        # 	channel_mean_pow = np.mean(bandpower, axis=1)

        #import pdb; pdb.set_trace()
        full_avg = np.mean(channel_mean_pow) # % 10)

        print(f"Channel mean pow: {channel_mean_pow} >> {full_avg}")
        
        bands.append(full_avg)
    print(f"\n-----\nBands: {bands}\n-----\n")
    sum_bands = sum(bands)
    norm = [float(i)/sum_bands for i in bands]

    for n in norm:
        bands_norm.append( round(n,2) )
        weighted_bands_norm.append( round (n*weight, 2) )
        #bandmean = 10 * np.mean(channel_mean_pow) / np.linalg.norm(channel_mean_pow) # normalize
        #seed += str(int(bandmean)) 

    for nb in weighted_bands_norm:
        seed += str( round(nb,1) )

    seed = "".join(num for num in seed.split("."))
    print("\n----------------------\n")
    print("RESULTING SEED:")
    print("Seed Key: Delta - Theta - Alpha - Beta - Gamma")
    print(f"Bands: {bands}, Bands Normalized: {bands_norm}")
    print(f"Weight Bands Normalized: {weighted_bands_norm}")

    print(f"Weight = {weight}")
    print(f"Seed: {seed}")
    print("\n----------------------\n")
    return int(seed)

def create_image_from_eeg(filename, username, output_dir=''):

    """
    Read in csv, preprocess, and pass a seed into the art generator.
    
    """
    name = input("Please input the participant's name: ")
    filtered_data = preprocessing.filter_signal(filename=filename)
    seed = generate_seed(filtered_data)
    
    print("Generating image.............")
    single_img_generation(RESOLUTION,seed,LAYERS,WIDTH,ACTIVATION, output_dir, username) # Imported as a method from main

def create_image_from_stream(data, username, output_dir=''):

    """
    Read in csv, preprocess, and pass a seed into the art generator.
    """
    filtered_data = preprocessing.filter_signal(datastream=data)
    seed = generate_seed(filtered_data)
    
    print("Generating image.............")
    single_img_generation(RESOLUTION,seed,LAYERS,WIDTH,ACTIVATION, output_dir, username) # Imported as a method from main


def generate_statistics(self):
    """
    Function that generates an informative PNG file
    with information on:
        EEG Bandpower Metrics
        Topographical Average Activity
        General Associate Assumptions off of EEG activty <<-- May be easier said than done
    """
    pass

    
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
            delta_val = delta_bandpower[random.randint(0,len(delta_bandpower)-1)]
            
            img[row,col] = [alpha_val,gamma_val,delta_val]
    
    plt.show(img)

if __name__ == "__main__":

    # if (len(argv) != 2):
    # 	raise ValueError("Correct usage: create.py [filename]")
        


    # # create_image_from_eeg(argv[1])
    # file = r"C:\Users\leofe\neurotech\telepathic-polluck\data\UnicornRecorder_20221009_105023_Clean.csv"
    # filepath = os.path.join(DIRNAME, file)
    # create_image_from_eeg(file)


    def gen_seed_str(sub_seeds:list):
        seed = ""
        for s in sub_seeds:
            seed += str(s)
        assert len(seed) == 10 # The size of the max bands (5 right now) * 2 for the decimal places
        return seed

    def generate_sub_seed(value):
        # assert 0.0 < value <= 1.0
        # value = value * 10
        # print(value)
        # print(str(value).split("."))
        val = "".join(n for n in str(value).split("."))
        
        if int(val)<1.0: val=val*10
        val = int(val)

        if len(str(val)) != 2: val = val*10

        if len(str(int(val))) >= 3: 
            val = val[:2]
            val = int(val)
        
        return int(val)

    def get_rand_float(r1, r2, m, w, places):
        # m is max
        assert r2 < m
        res = random.uniform(r1, r2)*w
        maxmimum = w*m
        result = res/maxmimum
        return round(result,places)

    def test_band(band='alpha', weight = 20, maximum = 10, n_images = 20, startfile=False):
        print(f"\n----------\n Testing {band} \n----------\n")
        wd, wd1, wt, wt1, wa, wa1, wb, wb1, wg, wg1 = 1.0, 1.5, 1.0, 1.5, 1.0, 1.5, 1.0, 1.5, 1.0, 1.5
        if band == 'alpha':
            wa = 9.0
            wa1 = 9.9
        elif band == 'beta':
            wb = 9.0
            wb1 = 9.9
        elif band == 'gamma':
            wg = 9.0
            wg1 = 9.9
        elif band == 'theta':
            wt = 9.0
            wt1 = 9.9
        elif band == 'delta':
            wd = 9.0
            wd1 = 9.9
    
        for i in range(n_images):
            s = []
            s.append(generate_sub_seed(get_rand_float(wd, wd1, maximum, weight, places=2)))   # Delta
            s.append(generate_sub_seed(get_rand_float(wt, wt1, maximum, weight, places=2)))   # Theta
            s.append(generate_sub_seed(get_rand_float(wa, wa1, maximum, weight, places=2)))   # Alpha 
            s.append(generate_sub_seed(get_rand_float(wb, wb1, maximum, weight, places=2)))   # Beta 
            s.append(generate_sub_seed(get_rand_float(wg, wg1, maximum, weight, places=2)))   # Gamma
            print(f"current bands: {s}")
            seed = gen_seed_str(s)
            print(f"Seed: {seed}")
            single_img_generation(RESOLUTION,int(seed),LAYERS,WIDTH,ACTIVATION, f'test_images/{band}', startfile)
        print("\n\n")

    # =================================================
    test_band(band='alpha', weight = 20, n_images = 20, startfile=False)
    test_band(band='beta',  weight = 20, n_images = 20, startfile=False)
    test_band(band='gamma', weight = 20, n_images = 20, startfile=False)
    test_band(band='delta', weight = 20, n_images = 20, startfile=False)
    test_band(band='theta', weight = 20, n_images = 20, startfile=False)
    # def regen():
    # 	s = []
    # 	s.append(generate_sub_seed(get_rand_float(1.0, 1.1, 10, 20, places=2)))   # Delta
    # 	s.append(generate_sub_seed(get_rand_float(1.0, 1.1, 10, 20, places=2)))   # Theta
    # 	s.append(generate_sub_seed(get_rand_float(9.0, 9.9, 10, 20, places=2)))   # Alpha 
    # 	s.append(generate_sub_seed(get_rand_float(1.0, 1.1, 10, 20, places=2)))   # Beta 
    # 	s.append(generate_sub_seed(get_rand_float(1.0, 1.1, 10, 20, places=2)))   # Gamma
    # 	return s

    print("Done!")
