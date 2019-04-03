import cv2
import numpy as np
from matplotlib import pyplot as plt

class CvUtils:

    def __init__(self):
        self._fig, self._aplt = plt.subplots(2, 2)

    def plot(self):
        plt.pause(0.3)
        plt.close()

    def add_to_plot(self, image, positionToPlot):
        self._aplt[positionToPlot[0], positionToPlot[1]].imshow(image, cmap='Greys_r')

    def add_circle_to_plot(self, circle, positionToPlot):
        self._aplt[positionToPlot[0], positionToPlot[1]].Circle(circle, color='blue')
    # Smoothes the image and plot if required

    def smooth(self, image, blurSquareWindow, positionToPlot):
        blurred_image = cv2.blur(image, blurSquareWindow)

        # if (shouldPlot):
        #     if (plot == None and shouldPlot):
        #         raise Exception('need to know wich position to plot')
        #
        self.add_to_plot(blurred_image, positionToPlot)
        return blurred_image

    def grayscale_threshold(self, image, minTreshold, maxTreshold, positionToPlot):
        ret, treshold_applied_image = cv2.threshold(image, minTreshold, maxTreshold, cv2.THRESH_BINARY)
        self.add_to_plot(treshold_applied_image, positionToPlot)
        return treshold_applied_image

    def get_circles(self, singleChannelImage, dpAccumulator, centerMinDistance, param1, param2, minRadius, maxRadius, positionToPlot):
        circles = cv2.HoughCircles(singleChannelImage, cv2.HOUGH_GRADIENT, dpAccumulator, centerMinDistance, param1=param1, param2=param2, minRadius= minRadius, maxRadius=maxRadius)
        for circle in circles[0, :]:
            self.add_circle_to_plot(circle, positionToPlot)
        return circles

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