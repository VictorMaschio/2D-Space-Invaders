# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 08:17:56 2022

@author: g.paulet-duprat
"""
import tkinter as tk
import Classe as cl
import Fonctions as f
import random as r
from PIL import Image, ImageTk

class jeu():
    def __init__(self):
        """
        Lance l'Initialisation de:
            - des tires alliés et enemies
            - de l'interface du jeu
            - d'une variable contenant la vie joueur
            - d'une variable contenant le score
        """
        self.pressed={}
        self.tiresG=[]
        self.tiresM=[]
        self.vie=3
        self.score=0
        self.mort=0
        self.creatInterface()
        self.root.mainloop()
        
    def start(self):
        """
        Initialisation / Réinitialisation du jeu:
            - set la vie a 3
            - on bloque le bouton nouvelle partie
            - on crée les enemies, les ilots, les déplacement des objets sur le canvas
        """
        if self.mort==1:
            self.canvas.delete(self.yditem)
        self.mort=0
        self.canvas.delete(self.backitem)
        self.backitem=self.canvas.create_image(800,470,image=self.backPhoto)
        v1item=self.canvas.create_image(self.v1.x,self.v1.y,image=self.v1Photo)
        self.v1.addItem(v1item)
        self.newGame['state'] = 'disabled'
        self.vie=3
        self.score=0
        self.allEnemmies=Allenemy(self.v2Photo)
        self.allEnemmies.move(self.canvas,self.root)
        self.createIlot()
        self._animatemove()
        self._animatetire()
        self.animateInterface()
        self.boom()
        
    def creatInterface(self):
        """
        Initialisation de l'interface avec:
            - la fenêtre
            - les boutons et labels
            - le canvas
            - chacun des objets du canvas soit lest tirs, les vaisseaux, les ilots
            - des controls en lancant la fonction setBinding
        """
        # Initialisation de la fenêtre
        self.root =tk.Tk()
        self.root.geometry("1920x1080")
        self.root.title("Space invader")
        self.root.overrideredirect(True)
        self.root.configure(bg='black')
        self.cadreG= tk.Frame(self.root)
        self.cadreG.configure(bg='black')
        self.cadreG.pack(side='left')
        self.cadreTop= tk.Frame(self.cadreG)
        self.cadreTop.configure(bg='black')
        self.cadreTop.pack(side='top')
        
        # Initialisation du score et de la vie du joueur
        self.scoreLabel= tk.Label(self.cadreTop,text='Score : '+str(self.score))
        self.scoreLabel.configure(bg='black',fg='white',font=("Courier", 20))
        self.scoreLabel.pack(side='left' ,padx=300,pady=30)
        self.vieLabel=tk.Label(self.cadreTop, text='Vies : '+str(self.vie))
        self.vieLabel.configure(bg='black',fg='white',font=("Courier", 20))
        self.vieLabel.pack(side='right' ,padx=300,pady=30)
        
        # Initialisation de l'image de fond
        backImg=Image.open("images/earth.jpeg")
        backimg=backImg.resize((1800, 1100))
        self.backPhoto=ImageTk.PhotoImage(backimg,master=self.cadreG)
        
        # Initialisation de l'image de fond
        backImg2=Image.open("images/brokenEarth.jpeg")
        backimg2=backImg2.resize((1800, 1100))
        self.backPhoto2=ImageTk.PhotoImage(backimg2,master=self.cadreG)
        
        #Initialisation de l'image des tires du joueur
        t1Image=Image.open("images/piou.png")
        t1img=t1Image.resize((15, 40))
        self.t1Photo=ImageTk.PhotoImage(t1img,master=self.cadreG)
        
        #Initialisation de l'image des tires des ennemies
        t2Image=Image.open("images/piou2.png")
        t2img=t2Image.resize((15, 40))
        self.t2Photo=ImageTk.PhotoImage(t2img,master=self.cadreG)
        
        #Initialisation de l'image des ennemies
        v2Image=Image.open("images/vaisseau2.png")
        v2img=v2Image.resize((100, 70))
        self.v2Photo=ImageTk.PhotoImage(v2img,master=self.cadreG)
        
        #initialisation de l'image du vaisseau du joueur
        self.v1=cl.entity(850,940,100,70,"images/vaisseau1.png",3,'G')
        v1Image=Image.open(self.v1.image)
        v1img=v1Image.resize((self.v1.lenght, self.v1.height))
        self.v1Photo=ImageTk.PhotoImage(v1img,master=self.cadreG)
        
        #Initialisation des images des Ilots (Liste d'images)
        self.IPhoto=[]
        for nb in [0,1,2,3]:
            nbString=str(nb)
            I1Image=Image.open("images/Débris%s.png" % nbString)
            I1img=I1Image.resize((150, 200))
            self.IPhoto.append(ImageTk.PhotoImage(I1img,master=self.cadreG))
        
        #Initialisation de l'écran de défaite.
        ydImage=Image.open("images/YD.png")
        ydimg=ydImage.resize((600,300))
        self.ydPhoto=ImageTk.PhotoImage(ydimg,master=self.cadreG)
        
        #Création du canvas 
        self.canvas=tk.Canvas(self.cadreG,bg='grey',height=1000,width=1700)
        self.backitem=self.canvas.create_image(800,470,image=self.backPhoto)
        
        
        self.canvas.pack()
        
        self.setBindings()
        
        # Initialisation des boutons de nouvelle partie et de fin
        self.newGame= tk.Button(self.root,text='Nouvelle Partie',state='normal',command=self.start)
        self.newGame.configure(bg='black',fg='white',font=("Courier", 10))
        self.newGame.pack(pady=300)
        self.quitbtn= tk.Button(self.root,text='Quitter',command=self.root.destroy)
        self.quitbtn.configure(bg='black',fg='white',font=("Courier", 10))
        self.quitbtn.pack()
        
    def setBindings(self):
        """
        Initialisation des controls 'q','d','espace', sous forme d'un dictionnaire contenant les caractères actuellement enfoncés
        """
        for char in ["q","d"," "]:
            self.root.bind("<KeyPress-%s>" % char, self._pressed)
            self.root.bind("<KeyRelease-%s>" % char, self._released)
            self.pressed[char] = False
            
    def _animatemove(self):
        """
        Déplacement du joueurs si une touche est enfoncé
        """
        if self.pressed["q"]: self.v1.move(-15,0,self.canvas)
        if self.pressed["d"]: self.v1.move(15,0,self.canvas)
        if self.mort==0:
            self.root.after(20, self._animatemove)
        
    def _animatetire(self):
        """
        Crée les tires du joueur si "espace" est enfoncé, et des tire ennemis aléatoirement
        """
        if self.pressed[" "]: 
            self.tiresG.append(self.creatTire(self.v1))
        
        for ennemie in self.allEnemmies.enemyListe:
            chance=r.randint(0,100)
            if chance<=25 and ennemie.y<950 and ennemie.y>140:
                self.tiresM.append(self.creatTire(ennemie))
        if self.mort==0:
            self.root.after(200, self._animatetire)
        
    def animateInterface(self):
        """
        Fonction d'actualisation du score et de la vie à partir des variable contenant la vie et le score.
        La fonction déclanche aussi la défaite si les ennemis descendent trop bas
        """
        self.vieLabel.configure(text='Vies : '+str(self.vie))
        self.scoreLabel.configure(text='Score : '+str(self.score))
        for enemy in self.allEnemmies.enemyListe:
            if enemy.y>870:
                self.youDied()
        if self.mort==0:
            self.root.after(100, self.animateInterface)
        
        
        
    def _pressed(self, event):
        """
        Fonction qui passe en True la valeur associée à la touche enfoncée dans le dictionaire.
        """
        self.pressed[event.char] = True

    def _released(self, event):
        """
        Fonction qui passe en False la valeur associée à la touche enfoncée dans le dictionaire.
        """
        self.pressed[event.char] = False
        
    def collision(self,entite1, entite2):
        """
        Fonction qui gère les collisions entre deux entités
        """
        if self.canvas.bbox(entite1) != None and self.canvas.bbox(entite2) != None:

            #On récupère les coordonées de l'objet 1
            x_1 = self.canvas.bbox(entite1)[0] 
            x_2 = self.canvas.bbox(entite1)[2] 
            y_1 = self.canvas.bbox(entite1)[1] 
            y_2 = self.canvas.bbox(entite1)[3] 
    
            # les coordonnées de la deuxième entité
            coords = self.canvas.bbox(entite2)
    
            #On vérifie s'i y a une collison par la gauche de l'entité 2 sur l'entité 1
            if (x_2 > coords[0]> x_1) and (y_1 < coords[1]< y_2):
                return True
    
            #On vérifie s'i y a une collison par la droite de l'entité 2 sur l'entité 1
            elif (x_2 > coords[2]> x_1) and (y_1 < coords[3]< y_2):
                return True
        
    def creatTire(self,v):
        """
        Créer un objet du canvas type tir alliée ou enemie en fonction de qui tir
        """
        if v.camp=="G":
            vitesse=-20
            t1=cl.entity(0,0,15,40,"images/piou.png",1,"G")
            imagePiou=self.t1Photo
        else:
            vitesse=20
            t1=cl.entity(0,0,15,40,"images/piou2.png",1,"M")
            imagePiou=self.t2Photo
        if vitesse<0:
            posy=-60
        else:
            posy=60
        t1.x=v.x
        t1.y=v.y +posy
        t1item=self.canvas.create_image(t1.x,t1.y,image=imagePiou)
        t1.addItem(t1item)
        self.automove(vitesse,t1)
        return t1
        
    def automove(self,vitesse,t1):
        """
        Déplacement automatique des tirs
        """
        if t1.y>50 and t1.y<950:
            t1.move(0,vitesse,self.canvas)
            self.root.after(10,self.automove,vitesse,t1)
        elif t1 in self.tiresG or t1 in self.tiresM:
            self.suprTire(t1)
        
    def suprTire(self,t1):
        """
        Supprime un tir de la liste des tirs de supprime l'objet canvas associé
        """
        if t1.camp=="G":
            self.tiresG.remove(t1)
            self.canvas.delete(t1.item)
        else:
            self.tiresM.remove(t1)
            self.canvas.delete(t1.item)
    
    def boom(self):
        """
        Détruit un objet de sa liste et son objet canvas suite à une collision 
        """
        for tire in self.tiresG:
            for enemy in self.allEnemmies.enemyListe:
                colli=self.collision(enemy.item, tire.item)
                if colli:
                    self.suprTire(tire)
                    self.allEnemmies.removeEnemy(enemy)
                    self.canvas.delete(enemy.item)
                    self.score+=50
                self.collisionIlotTire(tire)
            
        for tire in self.tiresM:
            colli2=self.collision(self.v1.item,tire.item)
            if colli2:
                self.suprTire(tire)
                self.vie-=1
                if self.vie<1:
                    self.youDied()
            self.collisionIlotTire(tire)
        if self.mort==0:  
            self.root.after(20, self.boom)
            
        for enemy in self.allEnemmies.enemyListe:
            for ilot in self.ilotListe:
                colli3=self.collision(ilot.item,enemy.item)
                if colli3:
                    self.allEnemmies.removeEnemy(enemy)
                    self.canvas.delete(enemy.item)
                    if ilot.vie<2:
                        self.canvas.delete(ilot.item)
                        nbImage=self.IPhoto.index(ilot.image)
                        if nbImage>0:
                            nbImage-=1
                            ilot.image=self.IPhoto[nbImage]
                            ilotItem = self.canvas.create_image(ilot.x,ilot.y,image=ilot.image)
                            ilot.addItem(ilotItem)
                            ilot.vie=4
                    else:
                        ilot.vie-=1
                  
    def collisionIlotTire(self,entity2):
        """
        Actualise l'état de l'ilot ou le détruit en fonction de sa vie et supprime le tir de la liste et de son objet 
        canvas. L'ilot commence à l'image Débrit3. Il a alors 4 vie. Lorsqu'il perd ses 4 vie il passe à l'image Débrit 2 et ainsi de suite
        jusqu'a arrivé à la dernière vie de Débrit0 ou l'ilot se suprime.
        """
        for ilot in self.ilotListe:
            colli3=self.collision(ilot.item,entity2.item)
            if colli3:
                self.suprTire(entity2)
                if ilot.vie<2:
                    self.canvas.delete(ilot.item)
                    nbImage=self.IPhoto.index(ilot.image)
                    if nbImage>0:
                        nbImage-=1
                        ilot.image=self.IPhoto[nbImage]
                        ilotItem = self.canvas.create_image(ilot.x,ilot.y,image=ilot.image)
                        ilot.addItem(ilotItem)
                        ilot.vie=4
                else:
                    ilot.vie-=1
               
    def youDied(self):
        """
        Lorsque la partie est perdue, affiche un écriteau marquand you died, réinitialise les variables du jeu, et passe self.mort à 1
        ce qui bloque les différentes fonctions récursives.
        """
        self.newGame['state'] = 'normal'
        self.allEnemmies._stop()
        for enemy in self.allEnemmies.enemyListe:
            self.canvas.delete(enemy.item)
        for ilot in self.ilotListe:
            self.canvas.delete(ilot.item)
        self.ilotListe=[]
        self.allEnemmies.enemyListe=[]
        self.canvas.delete(self.backitem)
        self.backitem=self.canvas.create_image(800,470,image=self.backPhoto2)
        self.ydCreate()
        self.canvas.delete(self.v1.item)
        self.v1.x=850
        self.mort=1
        
    def ydCreate(self):
        """
        Crée l'objet canvas de l'image you died
        """
        self.yditem=self.canvas.create_image(850,500,image=self.ydPhoto)
    
    def createIlot(self):
        """
        Crée 3 objet entity représentant les ilots à partir de l'objet canvas de l'ilot et les ajoutent à la liste
        """
        self.ilotListe=[]
        for nbIlot in range(3):
            ilot=cl.entity(250+nbIlot*600,700,150,200,self.IPhoto[3],4,"I")
            ilotItem = self.canvas.create_image(ilot.x,ilot.y,image=ilot.image)
            ilot.addItem(ilotItem)
            self.ilotListe.append(ilot)
            
        
        

class entity():
    """
    Objet définissant chacun des entité (vaisseaux, tirs, ilots)
    """
    def __init__(self,x,y,lenght,height,image,vie,camp):
        #x et y : coordonnées , lenght et height: dimmensions de l'image , image: liens de l'image.
        self.x=x
        self.y=y
        self.lenght=lenght
        self.height=height
        self.image=image
        self.vie=vie
        self.camp=camp
    
    def move(self,dx,dy,canvas):
        #dx et dy : variation des coordonnées, vitem: item du canvas a déplacer, canvas: zone de dessin.
        #change les coordonnées du vaisseau en leur ajoutant dx et dy.
        if self.x+dx>55 and self.x+dx<1645:    
            self.x+=dx
        self.y+=dy
        canvas.coords(self.item,self.x,self.y)
        
    def addItem(self,item):
        self.item=item
        
class Allenemy():
    """
    Objet contenant chacun des enemies apparus sur le champs de bataille ainsi que le déplacement 
    en cours et le déplacement précédent
    """
    def __init__(self,V2Photo):
        self.level=f.OuvrirFichier("enemy.txt")
        self.enemyListe=[]
        self.deplacement=['B','D']
        self.v2Photo=V2Photo
        self.stop=0
        
    def _stop(self):
        """
        Permet d'arréter les fonction récursives de déplacement.
        """
        self.stop=1

    def add(self,enemy):
        #Ajoute un enemy à la liste des enemy
        self.enemyListe.append(enemy)
    
    def removeEnemy (self,enemy):
        #Enlève un enemy à la liste des enemy
        self.enemyListe.remove(enemy)
    
    def move(self,canvas,root):
        """
        Effectue un déplacement globale des enemies vers la droite, le bas ou la gauche en fonction 
        du déplacement actuel. Lorsque l'ennemi le plus a droite atteint la droite lors d'un déplacement à droite,
        tout les ennemis décendent un peu, puis se déplace à gauche et ainsi de suite.
        """
        dx=15
        if self.enemyListe ==[]:
            self.spawnEnemy(canvas)
        if self.deplacement[1]=='D':
            maxx=0
            for i in range(0,len(self.enemyListe)):
                if self.enemyListe[i].x>maxx:
                    maxx=self.enemyListe[i].x
            if maxx+dx<1600:
                for i in range(0,len(self.enemyListe)):
                    self.enemyListe[i].move(dx,0,canvas)
            else:
                self.deplacement[0] =self.deplacement[1]
                self.deplacement[1] ='B'
        elif self.deplacement[1] =='G':
            dx=-dx
            minx=1600
            for i in range(0,len(self.enemyListe)):
                if self.enemyListe[i].x<=minx:
                    minx=self.enemyListe[i].x
            if minx+dx>=80:
                for i in range(0,len(self.enemyListe)):
                    self.enemyListe[i].move(dx,0,canvas)
            else:
                self.deplacement[0] =self.deplacement[1]
                self.deplacement[1] ='B'
        elif self.deplacement[1] =='B':
            self.spawnEnemy(canvas)
            maxy=0
            for i in range(0,len(self.enemyListe)):
                if self.enemyListe[i].y>maxy:
                    maxy=self.enemyListe[i].y
            posyenemymax = maxy + 80
            self.descente(posyenemymax,canvas,root)
            if self.deplacement[0] == 'D':
                self.deplacement[1] = 'G'
            elif self.deplacement[0] == 'G':
                self.deplacement[1] = 'D'
            self.deplacement[0] = 'B'
        if self.stop==0:
            root.after(30, self.move,canvas,root)

    def descente(self,posyenemymax,canvas,root):
        """
        Effectue un déplacement globale des enemies vers le bas dès qu'elle est appellée
        """
        maxy=0
        for i in range(0,len(self.enemyListe)):
            if self.enemyListe[i].y>maxy:
                maxy=self.enemyListe[i].y
        if posyenemymax>maxy+100:
            posyenemymax=maxy+100
        if maxy <=880:
            if maxy <= posyenemymax:
                for i in range(0,len(self.enemyListe)):
                    self.enemyListe[i].move(0,15,canvas)
                if self.stop==0:
                    root.after(20,self.descente,posyenemymax,canvas,root)
    
    def spawnEnemy(self,canvas):
        """
        Fonction qui gère l'apparition des enemies de sorte à ce qu'ils apparaissent aligné avec le plus à gauche ou
        le plus à droite. Les emplacement des ennemis sont récupérés depuis le fichier text enemy.txt.
        """
        if self.level==[]:
            self.level=f.OuvrirFichier("enemy.txt")
        if self.deplacement[0] == 'D':
            value = 600
        elif self.deplacement[0] == 'G':
            value = 85
        elif self.deplacement[0] == 'B':
                value = 100
        for i in range (0,len(self.level[0])):
            if self.level[0][i] == '1' :
                v2=f.creatEnemies(value +150*i,-30,self.v2Photo,canvas)
                self.add(v2)
        self.level.pop(0)
            
        

        
        
        