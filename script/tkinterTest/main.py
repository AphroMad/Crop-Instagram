import tkinter as tk
from PIL import Image, ImageTk
import os

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
image = Image.open('image.jpg')

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

# Check if directories exists, if not create it / them 
directory1 = "./template/settings/"
directory2 = "./template/comment/"
if not os.path.exists(directory1):
    os.makedirs(directory1)
if not os.path.exists(directory2):
    os.makedirs(directory2)

# Si le premier rectangle est en dessous du second, on inverse les deux
if list_of_points[0][0][1] > list_of_points[1][0][1] :
    list_of_points[0], list_of_points[1] = list_of_points[1], list_of_points[0] 

# Crop image at the coordinates of the rectangles and save them 
for i in range(len(list_of_points)):
    #cropped_image = image.crop(tuple(zip(*list_of_points[i])))
    cropped_image = image.crop((list_of_points[i][0][0],list_of_points[i][0][1],list_of_points[i][1][0],list_of_points[i][1][1]))
    if i == 0 : cropped_image.save(directory1+'settings_icon_'+str(i)+'.jpg')
    if i == 1 : cropped_image.save(directory2+'comment_icon_'+str(i)+'.jpg')