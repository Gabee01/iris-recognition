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
import math

#getting images
# irisRec = IrisRec()
casiaIris = CASIAIris()
# ubiIris = UBIRIS()

images = casiaIris.EyeImages


for image in images:
    my_utils = CvUtils()
    my_utils.add_to_plot(image, [0,0])

    blurSquareWindow = (20,20)
    blurredImage = my_utils.smooth_blur(image, blurSquareWindow, [0, 1])
    blurredImage = my_utils.smooth_blur(blurredImage, blurSquareWindow, [1, 1])

    # blurSquareWindow = (5, 5)
    # gaussianBlurredImage = my_utils.smooth_gaussian_blur(image, blurSquareWindow, [1, 0])

    minTreshold = 100
    maxTreshold = 180
    pupilMaskBinary = my_utils.grayscale_threshold(blurredImage, minTreshold, maxTreshold, [1,0])

    blurSquareWindow = (5, 5)
    gaussianBlurredImage = my_utils.smooth_gaussian_blur(pupilMaskBinary, blurSquareWindow, [2, 0])

    # minTreshold = 100
    # maxTreshold = 180
    # pupilMaskBinary = my_utils.grayscale_threshold(gaussianBlurredImage, minTreshold, maxTreshold, [2, 0])

    dp = 1
    minDist = math.sqrt(image.size)/8
    minRadius = 0
    maxRadius = 0
    param1 = 100
    param2 = 10
    pupilCircle = my_utils.get_circles(pupilMaskBinary, dp, minDist, param1, param2, minRadius, maxRadius, [2,1])

    irisCircle = pupilCircle
    # irisCircle[2] += 65
    my_utils.draw_circle(irisCircle, image)
    my_utils.draw_circle(pupilCircle, image, 1)
    my_utils.add_to_plot(image, [0,0])

    irisCenter = (irisCircle[0], irisCircle[1])
    irisRadius = irisCircle[2]

    crop_initial = (math.ceil(irisCenter[0] - irisRadius), math.ceil(irisCenter[1] - irisRadius))
    crop_final = (math.ceil(irisCenter[0] + irisRadius), math.ceil(irisCenter[1] + irisRadius))
    cropped_image = my_utils.crop_image(image, crop_initial, crop_final)
    my_utils.add_to_plot(cropped_image, [0, 0])

    my_utils.plot()
