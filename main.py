#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ISAT 690
Summer 2022
Assignment #2

@Author: Jenna Dauzat
"""
from matplotlib import pyplot as plt
from skimage.feature import corner_harris, corner_peaks, plot_matches

import glob
import imageio as iio
import numpy as np
import os

img_folder = 'rsrc'
corner_images = {}

class corner_image:
    def __init__(self, img, filename, coords):
        self.img = img
        self.filename = filename
        self.coords = coords

    def get_img(self):
        return self.img

    def get_filename(self):
        return self.filename

    def get_coords(self):
        return self.coords

def find_and_plot_corners():
    for image in glob.iglob(f'{img_folder}/*.jpg'):
        img = iio.imread(image, as_gray=True)
        coords = corner_peaks(corner_harris(img), min_distance=5, threshold_rel=0.02)
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.plot(coords[:,1], coords[:,0], color='cyan', marker='o', linestyle='None', markersize=6)
        filename = os.path.basename(image)
        plt.savefig("output/corners/{}".format(filename))
        i = corner_image(img, filename, coords)
        corner_images.update({"{}".format(filename): i})

def define_corner_descriptor(val, coord):
    metadata = {}
    #print('filename: {}, coords: {}, img: {}'.format(corner.get_filename(), corner.get_coords(), corner.get_img()))
    x = coord[1]
    y = coord[0]
    img = np.array(val.get_img())
    img.astype(int)
    pt = int(img[y,x])
    # create 16x16 window around each point
    slice = img[y-8:y+8, x-8:x+8]
    #find avg intensity
    avg_intensity = int(np.average(slice))
    #create 1x2 vector containing corner pixel value and the avg. pixel intensity value
    vector = np.array([pt, avg_intensity])
    metadata.update({"({}, {})".format(x, y): vector})

    return metadata

def compare_reference_to_transformed_images():
    keypoints1 = corner_images.get('Reference_Image.jpg').get_coords()

    #{"{filename}.jpg": corner_img-Object}
    for key, value in corner_images.items():
        if (key.__contains__("Transformed")):
            matches = []
            for coordinates in value.get_coords():
                euclids = []
                #map (x,y) => [[{pixel-intensity-value-at(x,y)}, {avg-pixel-intensity-for-16x16-window-where-(x,y)-is-center}]]
                info = define_corner_descriptor(value, coordinates)
                for kp in keypoints1:
                    #returns pixel value and avg pixel intensity
                    kp_info = define_corner_descriptor(corner_images.get('Reference_Image.jpg'), kp)
                    #get euclidean distance between keypoint in ref. image + avg. intensity and coord in transformed image + avg. intensity
                    sum_sq = np.sum(np.square(list(info.values())[0] - list(kp_info.values())[0]))
                    print("comparing ({},{}) from {} to ({},{}) in Reference Image: value,avg={}, VS value,avg={}; distance = {}"
                         .format(coordinates[1],
                         coordinates[0],
                         key, kp[1], kp[0],
                         list(info.values())[0],
                         list(kp_info.values())[0], sum_sq))
                    euclids.append([kp, sum_sq])

                #after getting euclidean distance between coordinate and all keypoints from reference image, record pair with smallest distance as a match
                min_euclid = euclids[0][1]
                for euclid in euclids:
                    if euclid[1] < min_euclid:
                        min_euclid = euclid[1]
                        ref_coord = euclid[0]
                matches.append([ref_coord, coordinates])

            keypoints2 = value.get_coords()
            fig, ax = plt.subplots()
            ref_image = corner_images.get('Reference_Image.jpg').get_img().astype('double')
            transformed_image = corner_images.get('{}'.format(key)).get_img().astype('double')
            matches = np.array(matches)
            ax.axis('off')
            ax.set_title('Original Image vs. {}'.format(key))
            plot_matches(ax, ref_image, transformed_image, keypoints1, keypoints2, matches)


if __name__ == '__main__':
    find_and_plot_corners()
    compare_reference_to_transformed_images()