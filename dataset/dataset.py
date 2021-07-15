#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.io import loadmat
from sys import argv
from ast import literal_eval
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

HEADERS = ['raw','features','label']

data = pd.DataFrame(columns=HEADERS)
data.to_csv('dataset.csv', index=False)

def sliding_window_features(data, window_size, step):
    VAR = []
    RMS = []
    ITG = []
    MAV = []
    WVL = []


    for index in range(window_size, data.size, step):
        window = data[index - window_size:index]

        VAR.append(variance(window))
        RMS.append(root_mean_square(window))
        ITG.append(integral(window))
        MAV.append(mean_absolute_value(window, window_size))
        WVL.append(waveform_lenght(window))
        
    features = get_features_vector(VAR, RMS, ITG, MAV, WVL)
    
    return features

def max_abs_norm(data):
    norm = data/np.amax(np.absolute(data))

    return norm
    
def variance(window):
    var = np.var(window)
    
    return var
    
def root_mean_square(window):
    rms = np.sqrt(np.mean(window**2))
    
    return rms
    
def integral(window):
    itg = np.sum(abs(window))
    
    return itg
    
def mean_absolute_value(window, window_size):
    mav = np.sum(np.absolute(window))/window_size
    
    return mav
    
def waveform_lenght(window):   
    wvl = np.sum(abs(np.diff(window)))
    
    return wvl
    

def get_series(data):
    s = data.loc[:,'features'] 
    x=[]
    for index, value in s.items():
        series = value.strip('][').split(', ')
        series = np.array(series,dtype=np.float32)
        x.append(series)
    return x
        
def get_features_vector(var,rms,itg,mav,wvl):
    features = []
    features.extend(var)
    features.extend(rms)
    features.extend(itg)
    features.extend(mav)
    features.extend(wvl)
    
    return features

def get_movement(n):
    if n <= 106000:
        mov = 1
    elif n >= 490000:
        mov = 3
    else:
        mov = 2
        
    return mov
    
def get_raw_emg(sensor1, sensor2, sensor3):
    sensors = []
    sensors.extend(sensor1)
    sensors.extend(sensor2)
    sensors.extend(sensor3)
    raw_emg = np.array(sensors)
    
    return sensors, raw_emg
    

def get_data (emg, startpoint, endpoint):
    sensor1 = []
    sensor2 = []
    sensor3 = []
    n = startpoint
    while n < endpoint:
        for i in range(n, n + 16000):
            sensor1.append(emg[i][0])
            sensor2.append(emg[i][1])
            sensor3.append(emg[i][2])

        data, npdata = get_raw_emg(sensor1,sensor2,sensor3)
        norm = max_abs_norm(npdata)       
        features = sliding_window_features(norm, 600, 500)       
        movement = get_movement(n)

        sensors = pd.DataFrame([[data, features, movement]])
        sensors.to_csv('dataset.csv', mode='a', index=False,
                       header=False)
        n = n + 16000
        sensor1 = []
        sensor2 = []
        sensor3 = []

def split_dataset(dataset, ratio):
    splitpoint = int(ratio*dataset.shape[0])
    train = dataset.iloc[:splitpoint,:]
    test = dataset.iloc[splitpoint:,:]
    train.to_csv('train.csv',index=False)
    test.to_csv('test.csv',index=False)
    
    return train, test
    
def build_dataset(minsub, maxsub) :
    for subject in range(minsub,maxsub):
        dataset = loadmat('S' + str(subject) + '_E2_A1.mat')
        emg = dataset['emg']
        get_data(emg, 10000,202000)
        get_data(emg,490000,586000)

def main():
    
    #Build dataset
    build_dataset(1,2)
    build_dataset(3,11)
        
    #Load dataset
    dataset = pd.read_csv('dataset.csv')
    
	#Shuffle dataset
    data = dataset.sample(frac=1)
    data.to_csv('dataset.csv',index=False)

    #Split dataset
    train, test = split_dataset(data, 0.75)
    
    
if __name__ == '__main__':
    main()
    
    
    
