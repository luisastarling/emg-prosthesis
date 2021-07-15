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
    
def get_series(data):
    s = data.loc[:,'features'] 
    x=[]
    for index, value in s.items():
        series = value.strip('][').split(', ')
        series = np.array(series,dtype=np.float32)
        x.append(series)
    return x


def main():

    #Get train and test data
    train = pd.read_csv('train.csv')
    test = pd.read_csv('test.csv')
    
    #get X e Y
    X_train = get_series(train)
    X_test = get_series(test)
        
    Y_train = train['label'].values
    Y_test = test['label'].values
    
    #Kernels
    #svclassifier = SVC(kernel='poly', degree=8)
    svclassifier = SVC(kernel='rbf')
    #svclassifier = SVC(kernel='sigmoid')
       
    #Fit
    svclassifier.fit(X_train, Y_train)
    
    #Predict
    Y_pred = svclassifier.predict(X_test)
    
    #Report
    print(confusion_matrix(Y_test, Y_pred))
    print(classification_report(Y_test, Y_pred, zero_division=1))    
    
if __name__ == '__main__':
    main()
    
    
    
