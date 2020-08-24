#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################################
# author: Nikolas Schnellbaecher
# contact: khx0@posteo.net
# date: 2020-08-24
# file: mpl_scatter_histogram.py
# tested with python 3.7.6 in conjunction with mpl version 3.2.2
##########################################################################################

import sys
sys.path.append('../')
import os
import platform
import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import legend

mpl.ticker._mathdefault = lambda x: '\\mathdefault{%s}'%x

today = datetime.datetime.now().strftime("%Y-%m-%d")

BASEDIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(BASEDIR, 'raw')
OUTDIR = os.path.join(BASEDIR, 'out')

os.makedirs(OUTDIR, exist_ok = True)

def getFigureProps(width, height, lFrac = 0.17, rFrac = 0.9, bFrac = 0.17, tFrac = 0.9):
    '''
    True size scaling auxiliary function to setup mpl plots with a desired size.
    Specify widht and height in cm.
    lFrac = left fraction   in [0, 1]
    rFrac = right fraction  in [0, 1]
    bFrac = bottom fraction in [0, 1]
    tFrac = top fraction    in [0, 1]
    returns:
        fWidth = figure width
        fHeight = figure height
    These figure width and height values can then be used to create a figure instance
    of the desired size, such that the actual plotting canvas has the specified
    target width and height, as provided by the input parameters of this function.
    '''
    axesWidth = width / 2.54    # convert to inches
    axesHeight = height / 2.54  # convert to inches
    fWidth = axesWidth / (rFrac - lFrac)
    fHeight = axesHeight / (tFrac - bFrac)
    return fWidth, fHeight, lFrac, rFrac, bFrac, tFrac

def Plot(X, outname, outdir, pColors, xFormat, yFormat, titlestr = '',
         grid = False, saveEPS = False, savePDF = True, savePNG = False, datestamp = True):

    mpl.rcParams['xtick.top'] = False
    mpl.rcParams['xtick.bottom'] = True
    mpl.rcParams['ytick.right'] = False
    mpl.rcParams['xtick.direction'] = 'out'
    mpl.rcParams['ytick.direction'] = 'out'

    mpl.rc('font', **{'size': 10})
    mpl.rc('legend', **{'fontsize': 7.5})
    mpl.rc('axes', linewidth = 0.5)

    mpl.rc('font', **{'family' : 'sans-serif', 'sans-serif' : ['Helvetica']})
    mpl.rcParams['pdf.fonttype'] = 42

    mpl.rcParams['text.usetex'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['text.latex.preamble'] = \
        r'\usepackage{cmbright}' + \
        r'\usepackage{amsmath}'

    ######################################################################################
    # set up figure
    fWidth, fHeight, lFrac, rFrac, bFrac, tFrac =\
        getFigureProps(width = 5.0, height = 4.0,
                       lFrac = 0.15, rFrac = 0.95,
                       bFrac = 0.15, tFrac = 0.92)
    f, ax1 = plt.subplots(1)
    f.set_size_inches(fWidth, fHeight)
    f.subplots_adjust(left = lFrac, right = rFrac)
    f.subplots_adjust(bottom = bFrac, top = tFrac)
    ######################################################################################

    major_x_ticks = np.arange(0.0, 20.1, 5.0)
    minor_x_ticks = np.arange(0.0, 20.1, 1.0)
    ax1.set_xticks(major_x_ticks)
    ax1.set_xticks(minor_x_ticks, minor = True)

    major_y_ticks = np.arange(0.0, 1.1, 0.2)
    minor_y_ticks = np.arange(0.0, 1.1, 0.05)
    ax1.set_yticks(major_y_ticks)
    ax1.set_yticks(minor_y_ticks, minor = True)

    labelfontsize = 6.0
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize(labelfontsize)

    ax1.tick_params('both', length = 3.0, width = 0.5, which = 'major')
    ax1.tick_params('both', length = 1.5, width = 0.25, which = 'minor')

    ax1.tick_params(axis = 'x', which = 'major', pad = 2.0)
    ax1.tick_params(axis = 'y', which = 'major', pad = 2.0, zorder = 10)
    ######################################################################################
    # labeling
    plt.title(titlestr, fontsize = 7.0, y = 0.975)
    ax1.set_xlabel(r'theoretical quantiles',
                   fontsize = 7.0)
    ax1.set_ylabel(r'sample quantiles',
                   fontsize = 7.0)
    ax1.xaxis.labelpad = 2.5
    ax1.yaxis.labelpad = 2.5
    ######################################################################################

    xmin, xmax = xFormat[0], xFormat[1]
    xVals = np.linspace(1.05 * xmin, 1.05 * xmax, 500)
    yVals = 1.0 * xVals
    
    ax1.plot(xVals, yVals,
             alpha = 1.0,
             color = pColors[0],
             lw = 0.5,
             clip_on = True,
             zorder = 1)

    ax1.scatter(X[:, 0], X[:, 1],
                s = 15,
                lw = 0.5,
                facecolor = 'None',
                edgecolor = pColors[0],
                zorder = 2,
                label = r'sampled data')

    ######################################################################################
    # set plot range and scale
    if xFormat == None:
        pass # mpl autoscale
    else:
        xmin, xmax, xTicksMin, xTicksMax, dxMajor, dxMinor = xFormat
        major_x_ticks = np.arange(xTicksMin, xTicksMax, dxMajor)
        minor_x_ticks = np.arange(xTicksMin, xTicksMax, dxMinor)
        ax1.set_xticks(major_x_ticks)
        ax1.set_xticks(minor_x_ticks, minor = True)
        ax1.set_xlim(xmin, xmax) # set x limits last (order matters here)
    if yFormat == None:
        pass # mpl autoscale
    else:
        ymin, ymax, yTicksMin, yTicksMax, dyMajor, dyMinor = yFormat
        major_y_ticks = np.arange(yTicksMin, yTicksMax, dyMajor)
        minor_y_ticks = np.arange(yTicksMin, yTicksMax, dyMinor)
        ax1.set_yticks(major_y_ticks)
        ax1.set_yticks(minor_y_ticks, minor = True)
        ax1.set_ylim(ymin, ymax) # set y limits last (order matters here)
    ######################################################################################
    ax1.set_axisbelow(False)
    ######################################################################################
    # grid options
    if grid:
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.2, which = 'major',
                 linewidth = 0.4)
        ax1.grid(True)
        ax1.grid(color = 'gray', linestyle = '-', alpha = 0.05, which = 'minor',
                 linewidth = 0.2)
        ax1.grid(True, which = 'minor')
    ######################################################################################
    # save to file
    if datestamp:
        outname += '_' + today
    if savePDF: # save to file using pdf backend
        f.savefig(os.path.join(outdir, outname) + '.pdf', dpi = 300, transparent = True)
    if savePNG:
        f.savefig(os.path.join(outdir, outname) + '.png', dpi = 600, transparent = False)
    ######################################################################################
    # close handles
    plt.cla()
    plt.clf()
    plt.close()
    return None

if __name__ == '__main__':

    samples_list = [10, 20, 50, 100, 500, 1000]

    for n_samples in samples_list:

        outname = 'qqplot_example_plot'
        outname += f'n_{n_samples}'
        outname += '_Python_' + platform.python_version() + \
               '_mpl_' + mpl.__version__
    
        filename = f'qqplot_data_normal_dist_n_{n_samples}.npy'

        # load data
        X = np.load(os.path.join(RAWDIR, filename))    
        print(X.shape)
    
        xFormat = (-2.9, 2.9, -3.0, 2.51, 1.0, 0.5)
        yFormat = (-2.9, 2.9, -3.0, 2.51, 1.0, 0.5)

        # plot data
        Plot(X = X,
            outname = outname,
            outdir = OUTDIR,
            pColors = ['k'],
            xFormat = xFormat,
            yFormat = yFormat,
            titlestr = f'qq-plot for $n={len(X)}$')
