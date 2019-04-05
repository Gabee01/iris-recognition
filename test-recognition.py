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
    plot_lines = 5
    plot_cols = 2
    my_utils = CvUtils(plot_lines, plot_cols)

    image_copy = image[:]
    # Plot original image
    my_utils.add_to_plot(image, [0,0])

    # generate and plot blurred image using avarage of square
    blurSquareWindow = (20,20)
    blurredImage = my_utils.smooth_blur(image, blurSquareWindow)
    blurredImage = my_utils.smooth_blur(blurredImage, blurSquareWindow)

    my_utils.add_to_plot(blurredImage, [1, 0])

    # generate and plot grayscale pupil image
    minTreshold = 100
    maxTreshold = 180
    pupilMaskBinary = my_utils.grayscale_threshold(blurredImage, minTreshold, maxTreshold)

    my_utils.add_to_plot(pupilMaskBinary, [2, 0])

    # applies gaussian blur to pupil image and plot
    blurSquareWindow = (15, 15)
    gaussianBlurredImage = my_utils.smooth_gaussian_blur(pupilMaskBinary, blurSquareWindow)

    my_utils.add_to_plot(gaussianBlurredImage , [3, 0])

    # generates and plot a blank image with the pupil circle drawn
    dp = 1
    minDist = math.sqrt(image.size)/8
    minRadius = 0
    maxRadius = 0
    param1 = 100
    param2 = 10
    pupilCircle, pupilCircleImage = my_utils.get_first_circle(pupilMaskBinary, dp, minDist, param1, param2, minRadius, maxRadius)
    pupilRadius = pupilCircle[2]
    my_utils.add_to_plot(pupilCircleImage, [0,1])

    # gets a concentric circle to identify the iris and plot
    irisCircle = pupilCircle[:]
    irisCircle[2] += 60
    irisCenter = (irisCircle[0], irisCircle[1])
    irisRadius = irisCircle[2]

    if ((irisCenter[0] + irisRadius > math.sqrt(image.size))
        or (irisCenter[1] + irisRadius > math.sqrt(image.size))):

        irisRadius -= (irisRadius - math.sqrt(image.size))
    elif ((irisCenter[0] - irisRadius < 0)
        or (irisCenter[1] - irisRadius < 0)):
        irisRadius -= (-1 * irisRadius)

    # creates and plot image with pupil and iris circles
    concentricCirclesImage = pupilCircleImage[:]
    my_utils.draw_circle(irisCircle, concentricCirclesImage)
    my_utils.add_to_plot(concentricCirclesImage, [1,1])

    # crops the image on the edges of the iris circle and plot
    crop_initial = (irisCenter[0] - irisRadius, irisCenter[1] - irisRadius)
    if (crop_initial[0] < 0):
        crop_initial = 0, crop_initial[1]
    if (crop_initial[1] < 0):
        crop_initial = crop_initial[0], 0

    crop_final = (irisCenter[0] + irisRadius, irisCenter[1] + irisRadius)
    if (crop_final[0] > math.sqrt(image.size)):
        crop_final = math.sqrt(image.size), crop_final[1]
    if (crop_final[1] > math.sqrt(image.size)):
        crop_final = crop_final[0], math.sqrt(image.size)

    crop_initial = math.floor(crop_initial[0]), math.floor(crop_initial[1])
    crop_final = math.floor(crop_final[0]), math.floor(crop_final[1])

    cropped_image = my_utils.crop_image(image, crop_initial, crop_final)
    my_utils.add_to_plot(cropped_image, [2,1])

    # creates an polar coordinate system representing the iris extracted
    radianInterval = 200
    twoTimesPi = 2 * np.pi
    reasultWidth = math.ceil(radianInterval * twoTimesPi)

    irisRadius = math.ceil(irisRadius)
    pupilRadius = math.floor(pupilRadius)
    resultHeight = irisRadius - pupilRadius

    polar_image = my_utils.create_blank(reasultWidth, resultHeight)
    for radius in range(pupilRadius, irisRadius):
        rads = np.arange(0, twoTimesPi , 1/radianInterval)
        for radian in rads:
            # x = r * cos(ø)
            # y = r * sen(ø)

            x = math.floor((radius * math.cos(radian)) + irisCenter[1])
            y = math.floor((radius * math.sin(radian)) + irisCenter[0])

            # if (radian < np.pi / 2):
            pixel = image_copy[x, y]
            concentricCirclesImage[x, y] = 0

            my_utils.plot_pixel(polar_image, math.floor(radian * radianInterval), math.floor(radius), pixel)

    my_utils.add_to_plot(concentricCirclesImage, [3, 1])
    my_utils.add_to_plot(polar_image, [4, 1])
    my_utils.add_to_plot(image_copy, [4,0])


    # plot images added to plot
    my_utils.plot()
