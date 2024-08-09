#!/usr/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt
from cv_utils import CvUtils
from irisrec_db_interface import CASIAIris
from feature_extraction import extract_features, extract_lbp_features
from matching import match_templates, find_best_match
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_image(image, my_utils):
    try:
        # Plot original image
        my_utils.add_to_plot(image, [0,0])

        # Preprocessing
        blurSquareWindow = (20,20)
        blurredImage = my_utils.smooth_blur(image, blurSquareWindow)
        blurredImage = my_utils.smooth_blur(blurredImage, blurSquareWindow)
        my_utils.add_to_plot(blurredImage, [1, 0])

        # Pupil detection
        minTreshold, maxTreshold = 100, 180
        pupilMaskBinary = my_utils.grayscale_threshold(blurredImage, minTreshold, maxTreshold)
        my_utils.add_to_plot(pupilMaskBinary, [2, 0])

        # Iris localization
        pupilCircle, pupilCircleImage = my_utils.get_first_circle(pupilMaskBinary, 1, np.sqrt(image.size)/8, 100, 10, 0, 0)
        my_utils.add_to_plot(pupilCircleImage, [0,1])

        irisCircle = list(pupilCircle)
        irisCircle[2] += 60
        irisCenter = (irisCircle[0], irisCircle[1])
        irisRadius = min(irisCircle[2], np.sqrt(image.size) - max(irisCenter))

        # Create image with pupil and iris circles
        concentricCirclesImage = pupilCircleImage.copy()
        my_utils.draw_circle(irisCircle, concentricCirclesImage)
        my_utils.add_to_plot(concentricCirclesImage, [1,1])

        # Normalization
        normalized_iris = normalize_iris(image, pupilCircle, irisCircle)
        my_utils.add_to_plot(normalized_iris, [2,1])

        # Feature extraction
        gabor_features = extract_features(normalized_iris)
        lbp_features = extract_lbp_features(normalized_iris)

        return gabor_features, lbp_features

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return None, None

def normalize_iris(image, pupil_circle, iris_circle):
    height, width = 64, 512
    normalized = np.zeros((height, width))

    pupil_center, pupil_radius = pupil_circle[:2], pupil_circle[2]
    iris_center, iris_radius = iris_circle[:2], iris_circle[2]

    for y in range(height):
        for x in range(width):
            theta = 2 * np.pi * x / width
            r = y / height

            rx = (1-r) * pupil_radius + r * iris_radius
            ry = rx

            px = int(pupil_center[0] + rx * np.cos(theta))
            py = int(pupil_center[1] + ry * np.sin(theta))

            if 0 <= px < image.shape[1] and 0 <= py < image.shape[0]:
                normalized[y, x] = image[py, px]

    return normalized

def main():
    casiaIris = CASIAIris()
    images = casiaIris.EyeImages

    gallery_features_gabor = []
    gallery_features_lbp = []

    for i, image in enumerate(images):
        my_utils = CvUtils(3, 2)
        gabor_features, lbp_features = process_image(image, my_utils)
        
        if gabor_features is not None and lbp_features is not None:
            gallery_features_gabor.append(gabor_features)
            gallery_features_lbp.append(lbp_features)
            
            if i == 0:  # Use the first image as a probe for demonstration
                probe_features_gabor = gabor_features
                probe_features_lbp = lbp_features

        my_utils.plot()

    # Matching demonstration
    best_match_gabor, distance_gabor = find_best_match(probe_features_gabor, gallery_features_gabor)
    best_match_lbp, distance_lbp = find_best_match(probe_features_lbp, gallery_features_lbp)

    logging.info(f"Best match (Gabor): Image {best_match_gabor}, Distance: {distance_gabor}")
    logging.info(f"Best match (LBP): Image {best_match_lbp}, Distance: {distance_lbp}")

if __name__ == "__main__":
    main()
