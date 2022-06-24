#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ISAT 690
Summer 2022
Assignment #2

Instructions:

1) Use the corner detection function available at “Skimage” library and detect the corners of the
given reference image as well as the transformed versions.

2) Define a descriptor for the detected corners and find the matching corners between the
reference image and each of the transformed versions. Then plot the matching corners using
a line from the reference to the transformed image.

An example of a simple descriptor is creating a nxn window around the corner point and
finding the average intensity. Then creating a 1x2 descriptor vector consists of the corner pixel
intensity value and the average intensity that you calculated from nxn window. Once you
define the descriptor, then you can use Euclidean distance to find the similarity between each
detected corner at the reference image and the transformed one. Finally, based on the similarity,
you can find the matching ones and plot a line in between.

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
