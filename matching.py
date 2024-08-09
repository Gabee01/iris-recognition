import numpy as np
from scipy.spatial.distance import hamming

def hamming_distance(template1, template2):
    """
    Calculate the Hamming distance between two iris templates.
    """
    return hamming(template1, template2)

def match_templates(template1, template2, threshold=0.3):
    """
    Match two iris templates using Hamming distance.
    Returns True if the templates match (distance is below the threshold).
    """
    distance = hamming_distance(template1, template2)
    return distance < threshold

def find_best_match(probe_template, gallery_templates):
    """
    Find the best match for a probe template in a gallery of templates.
    Returns the index of the best match and the corresponding distance.
    """
    distances = [hamming_distance(probe_template, template) for template in gallery_templates]
    best_match_index = np.argmin(distances)
    return best_match_index, distances[best_match_index]