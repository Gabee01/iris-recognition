import cv2
import numpy as np

def gabor_filter(image, ksize=31, sigma=4.0, theta=0, lambda_=10.0, gamma=0.5, psi=0):
    """
    Apply Gabor filter to the input image.
    """
    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambda_, gamma, psi, ktype=cv2.CV_32F)
    filtered = cv2.filter2D(image, cv2.CV_8UC3, kernel)
    return filtered

def extract_features(normalized_iris):
    """
    Extract features from the normalized iris image using Gabor filters.
    """
    features = []
    for theta in np.arange(0, np.pi, np.pi / 8):
        filtered = gabor_filter(normalized_iris, theta=theta)
        features.append(filtered.flatten())
    return np.concatenate(features)

def lbp(image, P=8, R=1):
    """
    Compute Local Binary Pattern features for the input image.
    """
    rows, cols = image.shape
    result = np.zeros((rows-2*R, cols-2*R), dtype=np.uint8)
    for i in range(R, rows-R):
        for j in range(R, cols-R):
            center = image[i, j]
            binary = np.zeros(P, dtype=np.uint8)
            for k in range(P):
                theta = 2 * np.pi * k / P
                x = i + int(round(R * np.cos(theta)))
                y = j + int(round(R * np.sin(theta)))
                binary[k] = 1 if image[x, y] >= center else 0
            result[i-R, j-R] = int(''.join(str(d) for d in binary), 2)
    return result

def extract_lbp_features(normalized_iris):
    """
    Extract LBP features from the normalized iris image.
    """
    lbp_image = lbp(normalized_iris)
    return lbp_image.flatten()