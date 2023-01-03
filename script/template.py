import cv2
import numpy as np
import glob
import tkinter as tk
from PIL import Image, ImageTk
import os 

def combine_overlapping_rectangles(rectangles):
    # Create a list to store the combined rectangles
    combined_rectangles = []

    # Iterate over the rectangles
    for rectangle in rectangles:
        # Check if the rectangle overlaps with any of the combined rectangles
        overlaps = False
        for combined_rectangle in combined_rectangles:
            if (abs(rectangle[0][0] - combined_rectangle[0][0]) < 10 and
                    abs(rectangle[0][1] - combined_rectangle[0][1]) < 10 and
                    abs(rectangle[1][0] - combined_rectangle[1][0]) < 10 and
                    abs(rectangle[1][1] - combined_rectangle[1][1]) < 10):
                # The rectangle overlaps with the combined rectangle, so merge them
                combined_rectangle[0] = (min(combined_rectangle[0][0], rectangle[0][0]),
                                         min(combined_rectangle[0][1], rectangle[0][1]))
                combined_rectangle[1] = (max(combined_rectangle[1][0], rectangle[1][0]),
                                         max(combined_rectangle[1][1], rectangle[1][1]))
                overlaps = True
                break
        if not overlaps:
            # The rectangle does not overlap with any of the combined rectangles, so add it to the list
            combined_rectangles.append(rectangle)

    # Return the combined rectangles
    return combined_rectangles


def find_template_resized(filename, filename2):
    # Load images 
    img = cv2.imread(filename)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(filename2)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # search 
    w, h = template_gray.shape[::-1]
    res = cv2.matchTemplate(img_gray,template_gray,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    points = []
    # Draw rectangle
    for pt in zip(*loc[::-1]):
        pt2 = (pt[0] + w, pt[1] + h)
        cv2.rectangle(img, pt,pt2, (0,0,255), 2)
        points.append([pt,pt2])
    # Combine overlapping rectangles and return the result
    if len(points) != 0: 
        """plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
        cv2.imwrite('../result/'+name+'.png',img_rgb)"""
        return combine_overlapping_rectangles(points)
    return False 
        

def test_template():
    chemin = "../test2/"
    template = "../template/"
    for filename in glob.glob(chemin+"*.png"):
        for filename2 in glob.glob(template+"*.png"):
            name = filename.split("test2/")[1].split(".")[0] + " " + filename2.split("template/")[1].split(".")[0]
            print(filename, filename2, name)
            find_template_resized(filename, filename2)

test_template()