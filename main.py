#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ISAT 690
Summer 2022
Assignment #2

@Author: Jenna Dauzat
"""
import glob
import imageio as iio
from matplotlib import pyplot as plt
import os
from skimage.feature import corner_harris, corner_peaks

img_folder = 'rsrc'
keys = {}

def find_and_plot_corners():
    for image in glob.iglob(f'{img_folder}/*.jpg'):
        img = iio.imread(image, as_gray=True)
        coords = corner_peaks(corner_harris(img), min_distance=5, threshold_rel=0.02)
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.plot(coords[:,1], coords[:,0], color='cyan', marker='o', linestyle='None', markersize=6)
        filename = os.path.basename(image)
        plt.savefig("output/corners/{}".format(filename))
        keys.update({f'{filename}': coords})

def define_corner_descriptor():
    pass

if __name__ == '__main__':
    find_and_plot_corners()
    define_corner_descriptor()
