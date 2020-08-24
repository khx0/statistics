#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-08-24
# file: main.py
# tested with python 3.7.6
##########################################################################################

import os
import datetime
import numpy as np
from scipy import stats

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(RAWDIR, exist_ok = True)

if __name__ == '__main__':

    # create samples from the standard normal distribution
    samples_list = [10, 20, 50, 100, 500, 1000]
    
    for n_samples in samples_list:
        
        np.random.seed(123456789)
        X = np.random.randn(n_samples)

        X_sorted = np.sort(X)
        
        x_support = (np.arange(1, n_samples + 1, 1) - 0.5) / float(n_samples)
        assert x_support.shape == X_sorted.shape, "Shape assertion failed."
    
        q_values = stats.norm.ppf(x_support)
        assert q_values.shape == x_support.shape, "Shape assertion failed."
    
        res = np.zeros((n_samples, 2))
        res[:, 0] = q_values
        res[:, 1] = X_sorted
    
        outname = f'qqplot_data_normal_dist_n_{n_samples}.npy'
        np.save(os.path.join(RAWDIR, outname), res)
