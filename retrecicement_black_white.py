# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 13:05:15 2020

@author: pierr
"""

import glob
import os 
from PIL import Image # on importe le module pour avoir les dim de l'image 

# =============================================================================
# Code pour récuperér une photo instagram après un screen
# =============================================================================

chemin = input("veuillez rentrer le chemin de là où il y a les photos :\n ") # on demande à l'utilisateur de rentrer le chemin et le nom de la photo 
#chemin = "D:\Prog&Job\Perso\Instagram_fond_ecran\test"
image_list = [] # on créer un tableau dans lequel on va mettre toutes les images 
name_image = [] # on créer un tableau dans lequel on va mettre les noms des images 

# =============================================================================
# On transforme tout les types de photos en .png et rentre dans un tableau
# =============================================================================
print("Préparation des photos et ré-enregistrement dans le bon format")

for filename in glob.glob(chemin+"\*.jpg") : # toutes les photos en jpg, on veut les mettre en png 
    #print("jpg")
    im = Image.open(filename) # on ouvre l'image 
    im.save(str(filename)+".png") # on l'enregistre au format png 
    os.remove(str(filename)) # on supprime l'ancienne image 
    
for filename in glob.glob(chemin+"\*.jpeg") : # toutes les photos en jpg, on veut les mettre en png 
    #print("jpg")
    im = Image.open(filename) # on ouvre l'image 
    im.save(str(filename)+".png") # on l'enregistre au format png 
    os.remove(str(filename)) # on supprime l'ancienne image 

for filename in glob.glob(chemin+"\*.png"): # I browse all.jpg files that are in the directory indicated by the variable "chemin".
    #print("png")
    im=Image.open(filename) # on ouvre l'image 
    image_list.append(im) # I add the image to a table
    name_image.append(filename) # on enregistre l'image avec son nom dans une case du tableau
    
# =============================================================================
# On va parcourir le tableau pour s'occuper de toute les photos
# =============================================================================
print("on commence")

for p in range(len(image_list)) : # on parcoure toutes les images du tableau 
    ima = image_list[p] # on choisit la photo 
    #print(type(ima),ima)
    largeur, hauteur = ima.size  # on prend ses dimensions 
    
    if largeur == 1080 and hauteur == 2340 or largeur == 1242 and hauteur == 2208 : 
        
        pix = ima.load() # on la charge (pour les pixels)
        
        # =============================================================================
        # On définit si la photo est sur fond blanc ou noir 
        # =============================================================================
        try : 
            (a,b,c) = pix[45,2130]
            (d,e,f) = pix[370,15]
        except : 
            (a,b,c,h) = pix[45,2130]
            (d,e,f,h) = pix[370,15]

        if  (a,b,c) == (18,18,18) or (d,e,f) == (18,18,18) : # si ce pixel a l'intérieur de l'icone maison est noir, alors la photo est sous fond noire
            fond_blanc = False
        else : 
            fond_blanc = True

        # =============================================================================
        # Création des variables 
        # =============================================================================
        lim_haute = 0 # on initialise la limite haute a 0, comme ça s'il y a un problème, la photo n'est pas coupé 
        lim_basse = hauteur # on initialise la limite basse au max, comme ca s'il y a un problème, la photo n'est pas coupé 
        diff = 0 # compteur de pixel blanc pour la limite haute 
        h_1 = int(hauteur/2) # on part du milieu de la hauteur 
        g_1 = 79 # on met la largeur a 79 pixel en partant de la gauche 
        nb_blanc = 0 # on initialise le nombre de pixel blanc à 0 
        nb_noir = 0 # on intitialise le nombre de pixel noir à 0 

        
        # =============================================================================
        # On determine ou couper l'image par le haut 
        # =============================================================================
        
        for i in range(h_1) : # on parcoure la moitié de l'image 
            
            i = h_1 - i  # on commence au milieu de l'image pour repartir en haut 
            #if i%20 == 0 : 
               # print(pix[g_1,i])
            """if i < 400 and i > 340 : 
                print(i)
                print(pix[g_1,i])
            """
            try : 
                (r,g,b) = pix[g_1,i] # on chope le code rgb 
            except : 
                (r,g,b,k) = pix[g_1,i] # on chope le code rgb 
            
            if fond_blanc : # si fond blanc
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
            
            #print(nb_noir)
            else : # si fond noir
                
                if (r<= 30 and g <= 30 and b <=30) or (r<=40 and g ==0 and b == 0) or (r<= 60 and g <= 20)or (r >= 190 and r <= 255 and g >= 135 and g <= 170 and b >= 50 and b <= 120) or (r>= 115 and r<= 145 and g >= 80 and g<= 95 and b >= 30 and b <= 60) or ((r>= 35 and r<= 80 or r>= 115 and r<=140 ) and g>= 50 and g<= 90 and (b>=100 and b<= 130 or b>= 190 and b<=220 or b>=10 and b<= 60)) or (r>= 100 and r<= 200 and g>= 20 and g<= 90 and b>= 40 and b<= 90) or (r>= 70 and r<= 125 and g>= 100 and g<=200 and b>= 40 and b<= 70): # on regarde si le pixel présent est blanc ou orange pour le cercle de la story ou cercle multicolor
                    nb_noir = nb_noir + 1 # le pixel est blanc donc on augmente le nombre de pixel blanc 
                    #if i >= 506 and i <= 539 : 
                        #print(i,nb_noir)
                else : 
                    nb_noir = 0
                    
                if nb_noir == 32 : # si le nombre de pixel blanc d'affilé est 22 
                    #print("on y est",i )

                    try : 
                        (a,be,c) = pix[126,i-50]
                        (aa,bb,cc) = pix[29,i-50]
                        
                    except : 
                        (a,be,c,d) = pix[126,i-50]
                        (aa,bb,cc,dd) = pix[29,i-50]
                    
                    #print("noir 32 : ", i+32,r,g,b,a,be,c,aa,bb,cc)

                    if (r<= 20 and g <= 20 and b <=20) and (a<= 12 and be <= 12 and c<= 12 )and (aa <= 12 and bb <= 12 and cc <= 12) : # on regarde 2 points autour si c'est noir ou non 
                        
                        
                        try : 
                            (n1,q1,r1) = pix[g_1+83,i-45] # pixel pour lettre pseudo 
                            (n2,q2,r2) = pix[g_1+83,i-36] # pixel pour lettre pseudo 
                            (n3,q3,r3) = pix[g_1+83,i-54] # pixel pour lettre pseudo 
                            (n4,q4,r4) = pix[g_1+83,i-63] # pixel pour lettre pseudo 
                            (n5,q5,r5) = pix[g_1+83,i-30] # pixel pour lettre pseudo 
                            (t_1,u_1,v_1) = pix[g_1+1081,i-49] # pixel pour point blanc 1
                            (t_2,u_2,v_2) = pix[g_1+1097,i-49] # pixel pour point blanc 2
                            (t_3,u_3,v_3) = pix[g_1+1114,i-49] # pixel pour point blanc 3
                            (li1,lo1,lu1) = pix[g_1-50,i] # pixel pour ligne noire
                            (li2,lo2,lu2) = pix[g_1+100,i] # pixel pour ligne noire
                            (li3,lo3,lu3) = pix[g_1+200,i] # pixel pour ligne noire
                            
                        except : 
                            (n1,q1,r1,w) = pix[g_1+83,i-45] # pixel pour lettre pseudo 
                            (n2,q2,r2,w) = pix[g_1+83,i-36] # pixel pour lettre pseudo 
                            (n3,q3,r3,w) = pix[g_1+83,i-54] # pixel pour lettre pseudo 
                            (n4,q4,r4,w) = pix[g_1+83,i-63] # pixel pour lettre pseudo
                            (n5,q5,r5,w) = pix[g_1+83,i-30] # pixel pour lettre pseudo 
                            (t_1,u_1,v_1,w) = pix[g_1+1081,i-49] # pixel pour point blanc 1
                            (t_2,u_2,v_2,w) = pix[g_1+1097,i-49] # pixel pour point blanc 2
                            (t_3,u_3,v_3,w) = pix[g_1+1114,i-49] # pixel pour point blanc 3
                            (li1,lo1,lu1,w) = pix[g_1-50,i] # pixel pour ligne noire
                            (li2,lo2,lu2,w) = pix[g_1+100,i] # pixel pour ligne noire
                            (li3,lo3,lu3,w) = pix[g_1+200,i] # pixel pour ligne noire
                            
                        #print(i,g_1-50,pix[g_1-50,i],g_1+50,pix[g_1+50,i],g_1+200,pix[g_1+200,i])
                        #print("pqr : ",g_1+83,i-30,n1,q1,r1,n2,q2,r2,n3,q3,r3,n4,q4,r4,n5,q5,r5)
                        
                        if (li1 <= 5 and lo1 <= 5 and lu1 <= 5) and (li2 <= 5 and lo2 <= 5 and lu2 <= 5) and(li3 <= 5 and lo3 <= 5 and lu3 <= 5) : # on vérifie si la longueur est noire
                            

                            #print("tuv 1 : ",g_1+1081,i-49,t_1,u_1,v_1)
                            #print("tuv 2 : ",g_1+1097,i-49,t_2,u_2,v_2)
                            #print("tuv 3 : ",g_1+1114,i-49,t_3,u_3,v_3)
                            
                            if (n1 >= 245 and q1 >= 245 and r1 >= 245) or (n2 >= 245 and q2 >= 245 and r2 >= 245)  or (n3 >= 245 and q3 >= 245 and r3 >= 245)  or (n4 >= 245 and q4 >= 245 and r4 >= 245)  or (n5 >= 245 and q5 >= 245 and r5 >= 245)  : # on regarde si y'a bien des points blanc pour le pseudo 
                                
                                if t_1 >= 225 and t_2 >= 225 and t_3 >= 225 and u_1 >= 225 and u_2 >= 225 and u_3 >= 225 and v_1 >= 225 and v_2 >= 225 and v_3 >= 225 : # on regarde si y'a les 3 points blanc 
                        
                                    lim_haute = i + 32 # on place la limite 
                                    break # on a trouvé la limite donc on s'en va 
            #print(nb_noir)
        #print("haut done, limite : ",lim_haute)
        
        # =============================================================================
        # Remise de certaine variables à 0
        # =============================================================================
        
        g_1 = 57 # on met la largeur a 57 pixel en partant de la gauche
        nb_blanc = 0 # on initialise le nombre de pixel blanc à 0 
        nb_noir = 0 # on intialise le nombre de pixel noir à 0 
        
        # =============================================================================
        # On détermine à quel endroit couper en bas 
        # =============================================================================
        
        for i in range(h_1) : # on parcoure la moitié de l'image 
        
            i = h_1 + i # on commence au milieu vers le bas 
        
            try : 
                (r,g,b) = pix[g_1,i] # on chope le code rgb 

            except : 
                (r,g,b,k) = pix[g_1,i] # on chope le code rgb 

        
            if fond_blanc : # si c'est fond blanc 
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
            #print(nb_noir)
            
            else : # si c'est fond noir 
                #if i >= 1915 and i <= 1955: 
                    #print(i,r,g,b)
                   
                if (r,g,b) == (0,0,0) or (r<=12 and g<=12 and b<=12) or (r<= 30 and g<=0 and b<=0): # on regarde si le pixel préent est blanc 
                    nb_noir = nb_noir + 1 # le pixel est blanc donc on augmente le nombre de pixel blanc 
                else : 
                     nb_noir = 0 # si le pixel du moment est différent de blanc on remet à 0 
                if nb_noir >= 40 : # si le nombre de pixel blanc d'affilé est de 35 
                    

                    try : 
                        (xx, yy ,zz) = pix[g_1,i+30]
                    except : 
                        (xx, yy ,zz,ww) = pix[g_1,i+30]
                        
                    try : 
                        (x,y,z) = pix[g_1,i+3] 
                    except : 
                        (x,y,z,w) = pix[g_1,i+3]
                        
                    #print(i,x,y,z,xx,yy,zz)
                    if (x >= 245 and y >= 245 and z >= 245 and xx <= 5 and yy <= 5 and zz <= 5) or (x >= 200 and xx >= 200 and y>=80 and y<=100 and yy>=80 and yy<=100 and z>=80 and z<=100 and zz>=80 and zz<=100  )  : # si pixel bordure blanc et int noir ou tout rouge 
                        lim_basse = i - 40 # on place la limite 
                        break # on a trouvé la limite donc on s'en va 

      
        #print("bas done, limite : ", lim_basse)
        
        
        # =============================================================================
        # On peut découper
        # =============================================================================
        
        ima = ima.crop((0,lim_haute,largeur-1,lim_basse)) # on découpe la photo 
    

    # =============================================================================
    # On redimensionne et on enregistre
    # =============================================================================
    
    largeur, hauteur = ima.size  # on prend ses dimensions 
    # avant de les enregistrer, il faut les mettre a la bonne hauteur pour la suite 
    coef = 440 / hauteur # on calcule le coef avec lequel on va changer la taille de l'image 
    new_h = int(hauteur * coef) # on calcule la nouvelle hauteur ( qui doit être égale a 440 normalement )
    new_l = int(largeur * coef) # on calcule la nouvelle largeur 
    ima = ima.resize((new_l,new_h), Image.ANTIALIAS) # on redimensionne l'image avec les nouvelles dimensions que l'on vient de calculer 
    # maintenant on peut les enregistrer
    ima.save(str(chemin)+'\\done\\photo_'+str(p)+'.png') # on la ré-enregistre sous un autre nom  
    #os.remove(str(name_image[p])) # on supprime l'ancienne image 

print("over")