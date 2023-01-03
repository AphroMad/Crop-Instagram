import glob
import os 
from PIL import Image # on importe le module pour avoir les dim de l'image 
from JPG_PNG import jpg_to_png 

chemin = "../test/"

# =============================================================================
# All images to .png
# =============================================================================
jpg_to_png(chemin) 

# =============================================================================
# Let's go through each image
# =============================================================================
for filename in glob.glob(chemin+"*.png"): # I browse all.jpg files that are in the directory indicated by the variable "chemin".
    with Image.open(filename) as curr_image:
        print(filename)
    