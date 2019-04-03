#!/usr/bin/python

# This program first apply an gaussian blur filter to better distribute the collors
# than it finds a binary mask identifing the pupil
# then from this mask it's possible to find a concentric circle
# that represents an aproximation of the iris space in the picture
# that aproximation has an bilinear interpolation applyed,
# wich results in the linear (rectangular) image,
# where we can apply another binaryzation, finding the final image
# to be compared when trying to match an known iris.

from cv_utils import *
from irisrec_db_interface import *
from matplotlib import pyplot as plt

#getting images
# irisRec = IrisRec()
casiaIris = CASIAIris()
# ubiIris = UBIRIS()

images = casiaIris.EyeImages


for image in images:
    my_utils = CvUtils()
    my_utils.add_to_plot(image, [0,0])

    blurSquareWindow = (20,20)
    blurredImage = my_utils.smooth(image, blurSquareWindow, [0,1])
    blurredImage = my_utils.smooth(blurredImage, blurSquareWindow, [0, 1])

    minTreshold = 100
    maxTreshold = 180
    pupilMaskBinary = my_utils.grayscale_threshold(blurredImage, minTreshold, maxTreshold, [1,0])

    dp = 1
    minDist = 55
    minRadius = 0
    maxRadius = 0
    param1 = 65
    param2 = 35
    circles = my_utils.get_circles(pupilMaskBinary, dp, minDist, param1, param2, minRadius, maxRadius, [1,1])

    my_utils.plot()
