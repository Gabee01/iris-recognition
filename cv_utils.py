import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle

class CvUtils:

    def __init__(self):
        self._fig, self._aplt = plt.subplots(3, 2)

    def plot(self):
        plt.pause(0.3)
        plt.close()

    def add_to_plot(self, image, positionToPlot):
        self._aplt[positionToPlot[0], positionToPlot[1]].imshow(image, cmap='Greys_r')

    def draw_circle(self, circle, imageToDraw, color = 0):
        circleCenter = (circle[0], circle[1])
        circleRadius = circle[2]
        cv2.circle(imageToDraw, circleCenter, circleRadius, color, 3)

    def crop_image(self, image, initialCoordinates, finalCoordinates):
        return image[initialCoordinates[1]: finalCoordinates[1], initialCoordinates[0]:finalCoordinates[0]]

    # Smoothes the image and plot
    def smooth_blur(self, image, blurSquareWindow, positionToPlot):
        blurred_image = cv2.blur(image, blurSquareWindow)

        self.add_to_plot(blurred_image, positionToPlot)
        return blurred_image

    # Smoothes the image and plot
    def smooth_gaussian_blur(self, image, blurSquareWindow, positionToPlot):
        blurred_image = cv2.GaussianBlur(image, blurSquareWindow, 0)

        self.add_to_plot(blurred_image, positionToPlot)
        return blurred_image

    def grayscale_threshold(self, image, minTreshold, maxTreshold, positionToPlot):
        ret, treshold_applied_image = cv2.threshold(image, minTreshold, maxTreshold, cv2.THRESH_BINARY)

        self.add_to_plot(treshold_applied_image, positionToPlot)
        return treshold_applied_image

    def get_circles(self, singleChannelImage, dpAccumulator, centerMinDistance, param1, param2, minRadius, maxRadius, positionToPlot):
        circles = cv2.HoughCircles(singleChannelImage, cv2.HOUGH_GRADIENT, dpAccumulator, centerMinDistance, param1=param1, param2=param2, minRadius= minRadius, maxRadius=maxRadius)

        for circle in circles[0, :]:
            self.draw_circle(circle, singleChannelImage)
            self.add_to_plot(singleChannelImage, positionToPlot)
            return circle

        # return circles

    def bilinear_interpolation(image, pt0, pt1,pts):
        raise NotImplemented()



# Thresholds kinds
    # ret, thresh2 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    # ret, thresh3 = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)
    # ret, thresh4 = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)
    # ret, thresh5 = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO_INV)
    # titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    # images = [image, thresh1, thresh2, thresh3, thresh4, thresh5]
    # for i in range(6):