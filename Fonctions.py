#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 10:20:49 2021

@author: g.paulet-duprat
"""
import tkinter as tk
import Classe as cl

def init_info():
    """
    Cette fonction lance la fenêtre d'instruction, lorsque le joueur appui sur le bouton commencer, le jeu est lancer
    """
    launch = tk.Tk()
    launch.geometry("600x600")
    launch.title("Space invader Instruction")
    launch.configure(bg='black')
    instruction="Bonjour,\n\nnous avons recréer le fameux space invaders:\n\nAider notre dernier vaisseau à affronter des\nhordes d'enemies surgissant à l'infini\nrespectant un pattern. Pour cela vous\ndisposer de tirs que vous lancez\navec la touche 'espace' et de déplacements gauche\net droite avec les touches 'q' et 'd'.\n\nSi un enemie s'approche trop de vous\nvous perdrez la partie !!! De même si vous perdez\nvos trois vies.\n\nPrenez votre courages camarade\nvous partez à la guerre !"
    info= tk.Label(launch,text=instruction)
    info.configure(bg='black',fg='white',font=("Courier", 15))
    info.pack(padx=30,pady=30)
    begin= tk.Button(launch,text='Commencer',command=launch.destroy)
    begin.configure(bg='black',fg='white',font=("Courier", 15))
    begin.pack(pady=40)
    launch.mainloop()
    cl.jeu()
  
def creatEnemies(x,y,v2Photo,canvas):
    """
    Cette fonction permet la création d'un objet sur le canvas à partir de ses coordonnées, de l'image et du canvas
    """
    v2=cl.entity(x,y,100,70,"vaisseau2.png",1,"M")
    v2item=canvas.create_image(x,y,image=v2Photo)
    v2.addItem(v2item)
    return v2
       
def OuvrirFichier(nom,car='/'):
    """
    Cette fonction ouvre un fichier text avec des caractère séparer par des '/' et en ressort un tableau
    """
    monFichier=open(nom, encoding='utf-8')
    Fichier=monFichier.readlines()
    monFichier.close()
    for i in range(len(Fichier)):
        a=Fichier[i].split(car)
        Fichier[i]=a[0:-1]
    return Fichier
        




#def destructionVaisseau(ligne,colonne):
    
    

    
    


        
