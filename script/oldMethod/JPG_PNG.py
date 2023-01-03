# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 21:02:50 2019

@author: pierr
"""

# Convertion des images au format PNG 

import glob
import os 
from PIL import Image # on importe le module pour avoir les dim de l'image 

def jpg_to_png(chemin) : 

    for filename in glob.glob(chemin+"*.jpg") : # toutes les photos en jpg, on veut les mettre en png 
        im = Image.open(filename) # on ouvre l'image 
        im.save(str(filename.split(".jpg")[0]) +"New.png") # on l'enregistre au format png 
        os.remove(str(filename)) # on supprime l'ancienne image 

jpg_to_png("../test2/")