# Run with python3.10

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


chemin = "../echantillon_images/"
chemin_results = chemin+"done/"
template_settings = "../template/settings/"
template_comment = "../template/comment/"
all_ite = 0 
ite = 0 
# Create mkdir if not exist
if not os.path.exists(chemin_results):
    os.makedirs(chemin_results)
if not os.path.exists(template_settings):
    os.makedirs(template_settings)
if not os.path.exists(template_comment):
    os.makedirs(template_comment)
# Go through all the files we want to crop 
for filename in glob.glob(chemin+"*.png"):
    all_ite += 1
    name = filename.split("echantillon_images/")[1].split(".")[0] 
    print(filename) 
    settings_found = False 
    comment_found = False 
    # While we don't find both
    while not settings_found or not comment_found:
        # Try to find setting emplacment 
        for filename2 in glob.glob(template_settings+"*.png"):
            name2 = filename2.split("template/settings/")[1].split(".")[0]
            settings_place = find_template_resized(filename, filename2)
            if settings_place != False:
                settings_found = True
                lim_haute = settings_place[0][0][1] + int(2.1*cv2.imread(filename2).shape[0])
        # Try to find comment emplacment
        for filename2 in glob.glob(template_comment+"*.png"):
            name2 = filename2.split("template/comment/")[1].split(".")[0]
            comment_place = find_template_resized(filename, filename2)
            if comment_place != False:
                comment_found = True
                lim_basse = comment_place[0][1][1] - int(2.1*cv2.imread(filename2).shape[0])
        # Doesn't find at least one, tkinter time 
        if not settings_found or not comment_found:
            ite += 1
            # Define some global variables to store the points that the user selects
            point1 = None
            point2 = None
            list_of_points = []
            rectangle = None
            list_of_rectangles = []


            # This function draws a rectangle on the canvas using the two points that the user selected
            def draw_rectangle():
                global point1, point2, rectangle, list_of_points, list_of_rectangles
                rectangle = canvas.create_rectangle(point1[0], point1[1], point2[0], point2[1], outline='red')
                list_of_points.append([point1,point2])
                list_of_rectangles.append(rectangle)
                # Enable the buttons
                if len(list_of_rectangles) == 2:
                    validate_button['state'] = 'normal'
                elif len(list_of_rectangles) <= 2:
                    retake_button['state'] = 'normal'
                # Reset the points 
                point1 = None
                point2 = None

            # This function is called when the user clicks the "Validate" button
            def validate():
                # Close the window 
                root.destroy()

            # This function is called when the user clicks the "Already Ok" button
            def already_ok():
                # Close the window and forget the coordinates of the clicks
                global list_of_points
                list_of_points = []
                root.destroy()

            # This function is called when the user clicks the "Re-take" button
            def retake():
                global point1, point2, rectangle, list_of_points, list_of_rectangles
                # Remove the rectangle from the canvas
                for rect in list_of_rectangles:
                    canvas.delete(rect)
                # Reset the points and rectangle
                point1 = None
                point2 = None
                rectangle = None
                list_of_points = []
                list_of_rectangles = []
                # Disable the buttons
                if len(list_of_rectangles) < 2:
                    validate_button['state'] = 'disabled'
                    retake_button['state'] = 'disabled'

            # This function is called when the user clicks the mouse on the canvas
            def click(event):
                global point1, point2
                if len(list_of_rectangles) < 2:
                    if point1 is None:
                        point1 = (event.x, event.y)
                        #print(f'point1: {point1}')
                    elif point2 is None:
                        point2 = (event.x, event.y)
                        #print(f'point2: {point2}')
                        draw_rectangle()

            # Load the image
            image = Image.open(filename)

            # Calculate the new size of the image so that it fits within the canvas
            image_ratio = image.width / image.height
            canvas_width = 250
            canvas_height = int(canvas_width*image.height/image.width)
            new_width = int(canvas_height * image_ratio)
            new_height = canvas_height
            image = image.resize((new_width, new_height))

            # Create the main window
            root = tk.Tk()
            root.title('Rectangle Selector')

            # Create a canvas and put the image on it
            canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
            image_tk = ImageTk.PhotoImage(image)
            text_label = tk.Label(root, text='Click on the top left corner of the icon then on the bottom right corner to create a rectangle.\nYou have to get in the rectangle both those icons (entire icon has to fit in): \n- the settings icon of the publication\n- the comment icon of the publication\nYou need to have 2 rectangles on the image to click Validate.')
            text_label.pack()
            canvas.create_image(0, 0, anchor='nw', image=image_tk)
            canvas.pack()

            # Create the "Validate" and "Re-take" buttons and disable them initially
            validate_button = tk.Button(root, text='Validate', state='disabled', command=validate)
            validate_button.pack()
            retake_button = tk.Button(root, text='Re-take', state='disabled', command=retake)
            retake_button.pack()
            alreadyOk_button = tk.Button(root, text='Already Ok', state='active', command=already_ok)
            alreadyOk_button.pack()

            # Bind the click function to mouse button events on the canvas
            canvas.bind('<Button-1>', click)

            # Run the tkinter event loop
            root.mainloop()

            # Si le premier rectangle est en dessous du second, on inverse les deux
            if list_of_points[0][0][1] > list_of_points[1][0][1] :
                list_of_points[0], list_of_points[1] = list_of_points[1], list_of_points[0] 

            # Crop image at the coordinates of the rectangles and save them 
            image_need_crop = cv2.imread(filename)
            for i in range(len(list_of_points)):
                crop_y, crop_height_y = int(list_of_points[i][0][1] * len(image_need_crop) / new_height), int(list_of_points[i][1][1] * len(image_need_crop) / new_height )
                crop_x, crop_width_x = int(list_of_points[i][0][0] * len(image_need_crop[0]) / new_width), int(list_of_points[i][1][0] * len(image_need_crop[0]) / new_width )
                cropped_image = image_need_crop[crop_y:crop_height_y, crop_x:crop_width_x]
                if i == 0 : 
                    cv2.imwrite(template_settings+'settings_icon_'+str(ite)+'.png', cropped_image)
                if i == 1 : 
                    cv2.imwrite(template_comment+'comment_icon_'+str(ite)+'.png', cropped_image)



    # Crop the image at the coordinates of the rectangles and save them
    image_need_crop = cv2.imread(filename)
    cropped_image = image_need_crop[lim_haute:lim_basse, :]
    #cv2.imwrite(chemin_results+'publication_'+str(all_ite)+'.png', cropped_image)
    cv2.imwrite(chemin_results+name+'.png', cropped_image)
        


print("end")
