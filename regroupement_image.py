# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 20:37:51 2019

@author: pierr
"""

# code pour créer les images composées de plusieurs photos 

from PIL import ImageDraw, Image
import glob
import random 
import os 

def creation_bg(name) : # fonction pour créer le background 
    bg = Image.new("RGBA", (1920,1080), (255,255,255,255)) # on créer une image à la bonne taille et blanche 
    draw1 = ImageDraw.Draw(bg,"RGBA") # on permet le dessin sur celle ci 
    draw1.rectangle(((100, 100), (1820, 980)), fill="white") # on dessine un rectangle blanc pour try 
    bg.save(str(chemin)+"\\done\\background_"+name+".png") # on l'enregistre histoire de
    return(str(chemin)+"\\done\\background_"+name+".png") 
    
def superposer_2_img(front, background,x,y,bg_name) : # fonction pour superposer 2 images 
    #front = Image.open(front) # on ouvre l'image front 
    #background = Image.open(background) # on ouvre l'image background
    img = Image.new('RGBA', background.size,(0,0,0,0)) # on créer une image de la même taille que le background 
    img.paste(background,(0,0)) # on y met le background dessus
    img.paste(front,(x,y)) # on y met la photo dessus 
    img.save(bg_name)

chemin = input("veuillez rentrer le chemin de là où il y a les photos :\n ") # on demande à l'utilisateur de rentrer le chemin et le nom de la photo 
liste_photo = [] # on créer un tableau dans lequel on mettra la photo et une info sur elle 
nombre_photo = 0 # variable qui indique le nombre total de photo 
for photo in glob.glob(chemin+"\*.png") : # on parcoure toutes les photos 
    photo = [photo,False] # on donne deux arguments a la photo, la photo elle même, et un argument booléen qui dit si elle a été utilisée ou non 
    liste_photo.append(photo) # on ajoute cette photo a la liste des photos 
    nombre_photo = nombre_photo + 1 # le nombre de photo augmente a chaque fois qu'on en met une de plus dans le tableau 

photo_used = 0 # variable qui indique le nombre de photo utilisée 
b = 0 # variable pour les noms des backgrounds  
while photo_used < nombre_photo : # tant qu'on a pas utilisé toutes les photos au moins une fois on travaille 
    b = b + 1 # pour changer le nom du prochain background 
    bg = Image.open(creation_bg(str(b))) # on créer un background et on l'ouvre dans python
    Largeur_bg, Hauteur_bg = bg.size # on récupère la taille du background 
    page_done = False # on dit que ce background n'est pas encore remplie 

    while not page_done : # tant qu'on a pas rempli entièrement le background, on continue a essayer de le remplir
        i = 0 # variable qui va servir a compter le nombre d'essai pour le random 
        ligne_H = 0 # variable qui donne la largeur de la ligne du haut
        ligne_B = 0 # variable qui donne la largeur de la ligne du bas 
        haut_done = False # variable qui dit si on a fini de remplir la ligne du haut 
        bas_done = False # variable qui dit si on a fini de remplir la ligne du bas 
        while haut_done == False :  # tant que la ligne n'est pas remplie 
            photo_dispo = True # on initialise cette variable a true pour rentrer dans la première boucle  
            i = i + 1 # on incrémente la variable qui donne le nombre d'essai 
            if i < 20 : # on fera juste 10 essai en choisissant les photos de manière random 
                while photo_dispo == True : # tant qu'on ne trouve pas une photo non utilisé, on en cherche une 
                    selection = random.randint(0,nombre_photo-1) # on prend un chiffre aléatoire 
                    photo_dispo = liste_photo[selection][1] # on regarde si la photo prise aléatoirement a déjà été utilisée ou non 
                im = Image.open(liste_photo[selection][0]) # la on ouvre l'image qu'on vient de sélectionner 
                largeur, hauteur = im.size # la on choppe les dimensions de l'image 
                if largeur < Largeur_bg - ligne_H - 200 : # si la largeur de la photo est inférieure à la largeur disponible sur le bg alors 
                    bg = Image.open(str(chemin)+"\\done\\background_"+str(b)+".png") # on réouvre le bon bg 
                    superposer_2_img(im,bg,ligne_H+100,100,str(chemin)+"\\done\\background_"+str(b)+".png") # on les superpose à la bonne largeur 
                    liste_photo[selection][1] = True # on vient d'utiliser la photo donc on la note comme utilisée 
                    ligne_H = ligne_H + largeur # la on donne la nouvelle largeur utilisé 
                    photo_used = photo_used + 1 # on incrémente le nombre de photo utilisée
            else : # si on a fais plus de 20 essais sans trouver d'image a la bonne taille, on les parcoure linéairement  
                for p in range(len(liste_photo)) : # on parcoure toutes les photos 
                    photo_dispo = liste_photo[p][1] # on attribue la disponibilité de la photo a la variable pour voir si on sort du while ou non 
                    if photo_dispo == False : # si on a une photo dispo, alors on doit la tester
                        im = Image.open(liste_photo[p][0]) # la on ouvre la photo pour python
                        largeur, hauteur = im.size # on choppe les dimensions de la photo 
                        if largeur < Largeur_bg - ligne_H - 200 : # si la largeur de la photo est inférieure à la largeur disponible sur le bg alors 
                            bg = Image.open(str(chemin)+"\\done\\background_"+str(b)+".png") # on réouvre le bon bg 
                            superposer_2_img(im,bg,ligne_H+100,100,str(chemin)+"\\done\\background_"+str(b)+".png") # on les superpose à la bonne largeur
                            liste_photo[p][1] = True # on vient d'utiliser la photo donc on la note comme utilisée 
                            ligne_H = ligne_H + largeur # la on donne la nouvelle largeur utilisé 
                            photo_used = photo_used + 1 # on incrémente le nombre de photo utilisée
                            break # on sort de la boucle et on recommence pour voir si il y'a encore de la place
                    if p == len(liste_photo)-1 : # si on a tout essayé 
                        haut_done = True # alors beh on a fini de remplir la ligne du haut 
                        
        while bas_done == False :  # tant que la ligne n'est pas remplie 
            photo_dispo = True # on initialise cette variable a true pour rentrer dans la première boucle  
            i = i + 1 # on incrémente la variable qui donne le nombre d'essai 
            if i < 20 : # on fera juste 10 essai en choisissant les photos de manière random 
                while photo_dispo == True : # tant qu'on ne trouve pas une photo non utilisé, on en cherche une 
                    selection = random.randint(0,nombre_photo-1) # on prend un chiffre aléatoire 
                    photo_dispo = liste_photo[selection][1] # on regarde si la photo prise aléatoirement a déjà été utilisée ou non 
                im = Image.open(liste_photo[selection][0]) # la on ouvre l'image qu'on vient de sélectionner 
                largeur, hauteur = im.size # la on choppe les dimensions de l'image 
                if largeur < Largeur_bg - ligne_B - 200 : # si la largeur de la photo est inférieure à la largeur disponible sur le bg alors 
                    bg = Image.open(str(chemin)+"\\done\\background_"+str(b)+".png") # on réouvre le bon bg 
                    superposer_2_img(im,bg,ligne_B+100,540,str(chemin)+"\\done\\background_"+str(b)+".png") # on les superpose à la bonne largeur 
                    liste_photo[selection][1] = True # on vient d'utiliser la photo donc on la note comme utilisée 
                    ligne_B = ligne_B + largeur # la on donne la nouvelle largeur utilisé 
                    photo_used = photo_used + 1 # on incrémente le nombre de photo utilisée
            else : # si on a fais plus de 20 essais sans trouver d'image a la bonne taille, on les parcoure linéairement  
                for p in range(len(liste_photo)) : # on parcoure toutes les photos 
                    photo_dispo = liste_photo[p][1] # on attribue la disponibilité de la photo a la variable pour voir si on sort du while ou non 
                    if photo_dispo == False : # si on a une photo dispo, alors on doit la tester
                        im = Image.open(liste_photo[p][0]) # la on ouvre la photo pour python
                        largeur, hauteur = im.size # on choppe les dimensions de la photo 
                        if largeur < Largeur_bg - ligne_B - 200 : # si la largeur de la photo est inférieure à la largeur disponible sur le bg alors 
                            bg = Image.open(str(chemin)+"\\done\\background_"+str(b)+".png") # on réouvre le bon bg 
                            superposer_2_img(im,bg,ligne_B+100,540,str(chemin)+"\\done\\background_"+str(b)+".png") # on les superpose à la bonne largeur
                            liste_photo[p][1] = True # on vient d'utiliser la photo donc on la note comme utilisée 
                            ligne_B = ligne_B + largeur # la on donne la nouvelle largeur utilisé 
                            photo_used = photo_used + 1 # on incrémente le nombre de photo utilisée
                            break # on sort de la boucle et on recommence pour voir si il y'a encore de la place
                    if p == len(liste_photo)-1 : # si on a tout essayé 
                        bas_done = True # alors beh on a fini de remplir la ligne du bas 
                        
        if haut_done == True and bas_done == True : 
            page_done = True # quand on a rempli la ligne du haut et celle du bas, alors on peut passer a un prochain bg 
            print("background : ",b)
        
print("on a tout utilisé ! ")             


