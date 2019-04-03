import cv2
import numpy as np
from matplotlib import pyplot as plt

# Smoothes the image and plot if required
def smooth(image, shouldPlot = False, plot = None):
    blurSquareWindow = (5,5)
    blur = cv2.blur(image, blurSquareWindow)

    if (shouldPlot):
        if (plot == None and shouldPlot):
            raise Exception('need to know wich position to plot')

        plot[0, 0].imshow(image, cmap='Greys_r')

def grayscale_threshold(image, shouldPlot = False, plot = None):
    ret, thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO_INV)
    titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [image, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in range(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])