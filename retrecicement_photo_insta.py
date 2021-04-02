# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:15:16 2019

@author: pierr
"""
import glob
import os 
from PIL import Image # on importe le module pour avoir les dim de l'image 

# =============================================================================
# Code pour récuperér une photo instagram après un screen
# =============================================================================

chemin = input("veuillez rentrer le chemin de là où il y a les photos :\n ") # on demande à l'utilisateur de rentrer le chemin et le nom de la photo 

image_list = [] # on créer un tableau dans lequel on va mettre toutes les images 
name_image = [] # on créer un tableau dans lequel on va mettre les noms des images 

for filename in glob.glob(chemin+"\*.jpg") : # toutes les photos en jpg, on veut les mettre en png 
    im = Image.open(filename) # on ouvre l'image 
    im.save(str(filename)+".png") # on l'enregistre au format png 
    os.remove(str(filename)) # on supprime l'ancienne image 

for filename in glob.glob(chemin+"\*.png"): # I browse all.jpg files that are in the directory indicated by the variable "chemin".
    im=Image.open(filename) # on ouvre l'image 
    image_list.append(im) # I add the image to a table
    name_image.append(filename) # on enregistre l'image avec son nom dans une case du tableau
    
    
for p in range(len(image_list)) : # on parcoure toutes les images du tableau 
    ima = image_list[p] # on choisit la photo 
    largeur, hauteur = ima.size  # on prend ses dimensions 

    if largeur == 1080 and hauteur == 2340 : 
        pix = ima.load() # on la charge (pour les pixels)
        lim_haute = 0 # on initialise la limite haute a 0, comme ça s'il y a un problème, la photo n'est pas coupé 
        lim_basse = hauteur # on initialise la limite basse au max, comme ca s'il y a un problème, la photo n'est pas coupé 
        diff = 0 # compteur de pixel blanc pour la limite haute 
        h_1 = int(hauteur/2) # on part du milieu de la hauteur 
        g_1 = 79 # on met la largeur a 79 pixel en partant de la gauche 
        nb_blanc = 0 # on initialise le nombre de pixel blanc à 0 
        for i in range(h_1) : # on parcoure la moitié de l'image 
            i = h_1 - i  # on commence au milieu de l'image pour repartir en haut 
            r,g,b = pix[g_1,i] # on chope le code rgb 
            if (r,g,b)!= (255,255,255) and (r,g,b) != (255,241,229) and r != 253 and (g < 142 or g>145) and (b<51 or b>53) : # on regarde si le pixel présent est différent de blanc 
                nb_blanc = 0 # si le pixel du moment est différent de blanc  on remet a 0 
            elif (r,g,b) == (255,255,255) or (r,g,b) == (255,241,229) or (r == 253 and g >= 142 and g <= 145 and b >= 51 and b <= 53) : # on regarde si le pixel présent est blanc ou orange pour le cercle de la story 
                nb_blanc = nb_blanc + 1 # le pixel est blanc donc on augmente le nombre de pixel blanc 
            if nb_blanc == 29 : # si le nombre de pixel blanc d'affilé est 29 
                if pix[g_1,i] == (255,255,255) and pix[121,i-42] == (255,255,255) and pix[37,i-42] == (255,255,255) and pix[g_1,i-85]==(255,255,255) or pix[g_1,i] == (0,0,0) and pix[121,i-42] == (0,0,0) and pix[37,i-42] == (0,0,0) and pix[g_1,i-85]==(0,0,0): # or pix[g_1,i] == (255,255,255) and pix[121,i-42] == (255,255,255) and pix[37,i-42] == (255,255,255) or pix[g_1,i] == (255,255,255) and pix[121,i-42] == (254,254,254) and pix[37,i-42] == (255,255,255) : # on regarde 4 points autour si c'est blanc ou non 
                    if pix[51,i-75] == (255,255,255) and pix[107,i-75] == (255,255,255) and pix[51,i-10] == (255,255,255) and pix[107,i-10] == (255,255,255) or pix[51,i-75] == (0,0,0) and pix[107,i-75] == (0,0,0) and pix[51,i-10] == (0,0,0) and pix[107,i-10] == (0,0,0):#or pix[51,i-10] == (255,255,255) and pix[107,i-10] == (255,255,255) : # on regarde si 4 points sur les diag sont blancs 
                        if pix[g_1,i-42] != (255,255,255) or pix[g_1,i-1] != (255,255,255) or pix[g_1,i-83] != (255,255,255) or pix[g_1,i-42] != (0,0,0) or pix[g_1,i-1] != (0,0,0) or pix[g_1,i-83] != (0,0,0) : # si le pixel qui est censé etre au centre du rond n'est pas blanc, alors on est bien sur la photo de profil 
                            lim_haute = i + 29 # on place la limite 
                            break # on a trouvé la limite donc on s'en va 
            
    
        g_1 = 57 # on met la largeur a 57 pixel en partant de la gauche
        nb_blanc = 0 # on initialise le nombre de pixel blanc à 0 
        
        for i in range(h_1) : # on parcoure la moitié de l'image 
            i = h_1 + i # on commence au milieu vers le bas 
            if pix[g_1,i] != (255,255,255) : # on regarde si le pixel présent est différent de blanc 
                nb_blanc = 0 # si le pixel du moment est différent de blanc on remet à 0 
            elif pix[g_1,i] == (255,255,255) : # on regarde si le pixel préent est blanc 
                nb_blanc = nb_blanc + 1 # le pixel est blanc donc on augmente le nombre de pixel blanc 
            if nb_blanc >= 35 : # si le nombre de pixel blanc d'affilé est de 35 
                if (pix[g_1,i+3] == (38,38,38) and pix[g_1,i+1] == (177,177,177) and pix[g_1+30,i+1] == (177,177,177)) or  (pix[g_1,i+3] == (38,38,38) and pix[g_1,i+55] == (255,255,255)) : # si le pixel a l'intérieur du coeur est noir et celui en dessous du coeur est blanc 
                    lim_basse = i - 35 # on place la limite 
                    break # on a trouvé la limite donc on s'en va 
                if pix[g_1,i+5] ==(237, 73, 86) and pix[g_1+30,i+3] == (237, 73, 86) : # on regarde si le coeur est rouge 
                    lim_basse = i - 35 # on place la limite 
                    break # on a trouvé la limite donc on s'en va 
      
        ima = ima.crop((0,lim_haute,largeur-1,lim_basse)) # on découpe la photo 
    

    largeur, hauteur = ima.size  # on prend ses dimensions 
    # avant de les enregistrer, il faut les mettre a la bonne hauteur pour la suite 
    coef = 440 / hauteur # on calcule le coef avec lequel on va changer la taille de l'image 
    new_h = int(hauteur * coef) # on calcule la nouvelle hauteur ( qui doit être égale a 440 normalement )
    new_l = int(largeur * coef) # on calcule la nouvelle largeur 
    ima = ima.resize((new_l,new_h), Image.ANTIALIAS) # on redimensionne l'image avec les nouvelles dimensions que l'on vient de calculer 
    # maintenant on peut les enregistrer
    ima.save(str(chemin)+'\\done\\photo_'+str(p)+'.png') # on la ré-enregistre sous un autre nom  
    os.remove(str(name_image[p])) # on supprime l'ancienne image 

