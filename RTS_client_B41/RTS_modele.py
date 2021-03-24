## - Encoding: UTF-8 -*-

import ast
import random
from helper import Helper
from RTS_divers import *
import math


class ARMOR_TYPES():
    LIGHT = 'LIGHT'
    HEAVY = 'HEAVY'
    SUPRA_HARD = 'SUPRA_HARD'

class Batiment():
    def __init__(self,parent,id,x,y):
        self.parent=parent
        self.id=id
        self.x=x
        self.y=y
        self.image=None
        self.montype=None
        self.maxperso=0
        self.perso=0
        self.cartebatiment=[]

        # Stats de defenses des bâtiments, doivent être spécifié dans les sous-classes
        self.health = 0
        self.defense = 2

        self.armorType = ARMOR_TYPES.HEAVY
        
class Maison(Batiment):
    def __init__(self,parent,id,couleur,x,y,montype):
        Batiment.__init__(self,parent,id,x,y)
        self.image=couleur[0]+"_"+montype
        self.montype=montype
        self.maxperso=10
        self.perso=0

        # Stats de defenses 
        self.health = 300
        self.defense = 2

class Abri():
    def __init__(self,parent,id,couleur,x,y,montype):
        Batiment.__init__(self,parent,id,x,y)
        self.image=couleur[0]+"_"+montype
        self.montype=montype
        self.maxperso=20
        self.perso=0
        
        # Stats de defenses 
        self.health = 300
        self.defense = 2
        
class Caserne():
    def __init__(self,parent,id,couleur,x,y,montype):
        Batiment.__init__(self,parent,id,x,y)
        self.image=couleur[0]+"_"+montype
        self.montype=montype
        self.maxperso=20
        self.perso=0

        # Stats de defenses 
        self.health = 500
        self.defense = 2
        
class Daim():
    def __init__(self,parent,id,x,y):
        self.parent=parent
        self.id=id
        self.etat="vivant"
        self.x=x
        self.y=y
        self.valeur=300
        self.cible=None
        self.angle=None
        self.dir="GB"
        self.vitesse=random.randrange(3)+3
        
    def mourir(self):
        self.etat="mort"
        self.cible=None
        
        
    def deplacer(self):
        if self.cible:
            x=self.cible[0]
            y=self.cible[1]  
            x1,y1=Helper.getAngledPoint(self.angle,self.vitesse,self.x,self.y)
            case=self.parent.trouvercase(x1,y1)
            if case[0]>self.parent.taillecarte or case[0]<0:
                self.cible=None
            elif case[1]>self.parent.taillecarte or case[1]<0:
                self.cible=None
            else:
                if self.parent.cartecase[case[1]][case[0]]>0:
                    pass
                    #print("marche dans ",self.parent.regionstypes[self.parent.cartecase[case[1]][case[0]]])
                # changer la vitesse tant qu'il est sur un terrain irregulier
                # FIN DE TEST POUR SURFACE MARCHEE
                self.x,self.y=x1,y1 
                dist=Helper.calcDistance(self.x,self.y,x,y)
                if dist <=self.vitesse:
                    self.cible=None
        else:
            if self.etat=="vivant":
                self.trouvercible()

    def trouvercible(self):
        n=1
        while n:
            x=(random.randrange(100)-50)+self.x
            y=(random.randrange(100)-50)+self.y
            case=self.parent.trouvercase(x,y)
            if case[0]>self.parent.taillecarte or case[0]<0:
                continue
            if case[1]>self.parent.taillecarte or case[1]<0:
                continue
            
            if self.parent.cartecase[case[1]][case[0]]==0:
                self.cible=[x,y]
                n=0
        self.angle=Helper.calcAngle(self.x,self.y,self.cible[0],self.cible[1])
        if self.x<self.cible[0]:
            self.dir="D"
        else:
            self.dir="G"
        if self.y<self.cible[1]:
            self.dir=self.dir+"B"
        else:
            self.dir=self.dir+"H"


class Biotope():
    def __init__(self,parent,id,monimg,x,y,montype):
        self.parent=parent
        self.id=id 
        self.img=monimg
        self.x=x
        self.y=y  
        self.montype=montype 
        self.sprite = None
        self.spriteNum = 0

class Baie(Biotope):
    typeressource=['baiegrand',
                   'baiepetit',
                   'baievert'] 
    def __init__(self,parent,id,monimg,x,y,montype):
        Biotope.__init__(self,parent,id,monimg,x,y,montype)
        self.valeur=100 
                   
class Marais(Biotope):
    typeressource=['marais1',
                   'marais2',
                   'marais3'] 
    def __init__(self,parent,id,monimg,x,y,montype):
        Biotope.__init__(self,parent,id,monimg,x,y,montype)
        self.valeur=100 
          
class Eau(Biotope):
    typeressource=['eaugrand1',
                   'eaugrand2',
                   'eaugrand3',
                   'eaujoncD',
                   'eaujoncG',
                   'eauquenouillesD',
                   'eauquenouillesG',
                   'eauquenouillesgrand',
                   'eautourbillon',
                   'eautroncs']

    def __init__(self,parent,id,monimg,x,y,montype):
        Biotope.__init__(self,parent,id,monimg,x,y,montype)
        n = random.randrange(100)
        
        if n == 10:
            self.spriteLength = len(self.parent.parent.vue.gifs["poissons"])
            self.sprite = "poissons"
            self.spriteNum = random.randrange(self.spriteLength)
            self.valeur=100 
        else:
            self.valeur = 10

    def nextSprite(self):
        if self.sprite:
            self.spriteNum+=1
            if self.spriteNum > self.spriteLength - 1:
                self.spriteNum = 0
                       
class Aureus(Biotope):
    typeressource=['aureusbrillant',
                   'aureusD_',
                   'aureusG',
                   'aureusrocgrand',
                   'aureusrocmoyen',
                   'aureusrocpetit']
    def __init__(self,parent,id,monimg,x,y,montype):
        Biotope.__init__(self,parent,id,monimg,x,y,montype)
        self.valeur=100 
                 
class Roche(Biotope):
    typeressource=['roches1 grand',
                   'roches1petit',
                   'roches2grand',
                   'roches2petit',
                   'roches3grand',
                   'roches3petit',
                   'roches4grand',
                   'roches4petit',
                   'roches5grand']
    def __init__(self,parent,id,monimg,x,y,montype):
        Biotope.__init__(self,parent,id,monimg,x,y,montype)
        self.valeur=100 
                    
class Arbre(Biotope):
    typeressource=['arbre0grand',
                   'arbre0petit',
                   'arbre1grand',
                   'arbre2grand',
                   'arbresapin0grand',
                   'arbresapin0petit']
    def __init__(self,parent,id,monimg,x,y,montype):
        Biotope.__init__(self,parent,id,monimg,x,y,montype)
        self.valeur=100 
        
class Javelot():
    def __init__(self,parent,id,proie):
        self.parent=parent
        self.id=id
        self.vitesse=18
        self.distance=150
        self.taille=20
        self.demitaille=10
        self.proie=proie
        self.proiex=self.proie.x
        self.proiey=self.proie.y
        self.x=self.parent.x
        self.y=self.parent.y
        self.ang=Helper.calcAngle(self.x,self.y,self.proiex,self.proiey)
        angquad=math.degrees(self.ang)
        dir="DB" 
        if 0 <= angquad <= 89 :
            dir="DB" 
        elif -90 <= angquad <= -1 :
            dir="DH" 
        if 90 <= angquad <= 179 :
            dir="GB" 
        elif -180 <= angquad <= -91 :
            dir="GH" 
        self.image="javelot"+dir
            
    def bouger(self): 
        self.x,self.y,=Helper.getAngledPoint(self.ang,self.vitesse,self.x,self.y)
        dist=Helper.calcDistance(self.x,self.y,self.proie.x,self.proie.y)
        if dist<=self.demitaille:  # 1 shot kill
            # tue daim
            self.parent.actioncourante="ciblerressource"
            self.parent.javelots.remove(self)
            self.proie.mourir()
        else:
            dist=Helper.calcDistance(self.x,self.y,self.proiex,self.proiey)
            if dist<self.vitesse:
                self.parent.javelots.remove(self)
                self.parent.actioncourante="ciblerproie"
                
                
            
        
                  
class Perso():    
    def __init__(self,parent,id,batiment,couleur,x,y,montype):
        self.parent=parent
        self.id=id
        self.actioncourante="deplacer"
        self.batimentmere=batiment
        self.dir="D"
        self.image=couleur[0]+"_"+montype+self.dir
        self.x=x
        self.y=y
        self.cible=[]
        self.champvision=100
        self.vitesse=5
        self.angle=None

        # Stats de combats, doivent être spécifié dans les sous-classes
        self.health = 0
        self.defense = 0
        self.atkDmg = 0
        self.atkRange = 3   # Default pour melee unit
        self.atkSpeed = 0
        self.armorType = ARMOR_TYPES.LIGHT
        self.mana=0



        
    def jouerprochaincoup(self):
        if self.actioncourante=="deplacer":
            self.deplacer()
            
    def deplacer(self):
        if self.cible:
            x=self.cible[0]
            y=self.cible[1]
            ang=Helper.calcAngle(self.x,self.y,x,y)  
            x1,y1=Helper.getAngledPoint(ang,self.vitesse,self.x,self.y)
            ####### ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER 
            ####### SINON RTOUVER VOIE DE CONTOURNEMENT
            casex=x1/self.parent.parent.taillecase
            if casex!=int(casex):
                casex=int(casex)+1
            casey=y1/self.parent.parent.taillecase
            if casey!=int(casey):
                casey=int(casey)+1
            if self.parent.parent.cartecase[int(casey)][int(casex)]>0:
                print("marche dans ",self.parent.parent.regionstypes[self.parent.parent.cartecase[int(casey)][int(casex)]])
            
            ####### FIN DE TEST POUR SURFACE MARCHEE
            self.x,self.y=x1,y1 
            dist=Helper.calcDistance(self.x,self.y,x,y)
            if dist <=self.vitesse:
                self.cible=None
                
    def cibler(self,pos):
        self.cible=pos
        if self.x<self.cible[0]:
            self.dir="D"
        else:
            self.dir="G"
        self.image=self.image[:-1]+self.dir
        
class Soldat(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype)
        
        # Stats de combats
        self.health = 100
        self.defense = 0
        self.atkDmg = 6
        self.atkSpeed = 5


class Archer(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype)
        
        # Stats de combats
        self.health = 60
        self.defense = 0
        self.atkDmg = 8
        self.atkRange = 30   
        self.atkSpeed = 7


class Chevalier(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype)
        
        # Stats de combats
        self.health = 200
        self.defense = 1
        self.armorType = ARMOR_TYPES.HEAVY
        self.atkDmg = 15
        self.atkRange = 5   
        self.atkSpeed = 2


class Druide(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype)
               
class Ouvrier(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype)
        self.actioncourante=None
        self.cibleressource=None
        self.typeressource=None
        self.quota=20
        self.ramassage=0
        self.cibletemp=None
        self.dejavisite=[]
        self.champvision=random.randrange(50)+150
        self.champchasse=120
        self.javelots=[]
        self.vitesse=random.randrange(5)+5

        # Combat stats
        self.health = 50
        self.defense = 0
        self.atkDmg = 2
        self.atkRange = 0   
        self.atkSpeed = 5

        
    def jouerprochaincoup(self):
        if self.actioncourante=="deplacer":
            self.deplacer()
        elif self.actioncourante=="ciblerressource":
            if self.cibleressource not in self.parent.parent.ressourcemorte:
                self.deplacer()
            else:
                self.actioncourante="retourbatimentmere"
                self.cibleressource=None
                self.typeressource=None
        elif self.actioncourante=="ramasserressource":
            if self.cibleressource not in self.parent.parent.ressourcemorte:
                self.ramasser()
            else:
                self.actioncourante="retourbatimentmere"
                self.cibleressource=None
            
        elif self.actioncourante=="retourbatimentmere":
            self.deplacer()
        elif self.actioncourante=="ciblerproie":
            if self.cibleressource.etat=="vivant":
                dist=Helper.calcDistance(self.x,self.y,self.cibleressource.x,self.cibleressource.y)
                if dist <=self.champchasse:
                    self.lancerjavelot(self.cibleressource)
                    self.actioncourante="attendrejavelot"
                else:
                    self.deplacer()
            else:
                self.actioncourante=="ciblerressource"
                self.deplacer()
        elif self.actioncourante=="attendrejavelot":
            for i in self.javelots:
                i.bouger()
            
    def lancerjavelot(self,proie):
        if self.javelots==[]:
            id=getprochainid()
            self.javelots.append(Javelot(self,id,proie))
             
    def ramasser(self):
        if not self.cibleressource:
            self.actioncourante="retourbatimentmere"
            self.cibler([self.batimentmere.x,self.batimentmere.y])
        else:
            self.ramassage+=1
            self.cibleressource.valeur-=1
            if self.cibleressource.valeur==0:
                self.actioncourante="retourbatimentmere"
                self.cibler([self.batimentmere.x,self.batimentmere.y])
                self.parent.avertirressourcemort(self.typeressource,self.cibleressource)              
            if self.ramassage==self.quota:
                self.actioncourante="retourbatimentmere"
                self.cibler([self.batimentmere.x,self.batimentmere.y])
            self.x=self.x+random.randrange(4)-2
            self.y=self.y+random.randrange(4)-2
                    
    def deplacer(self):
        if self.cible:
            if self.actioncourante=="ciblerressource" and not self.cibleressource:
                self.actioncourante="retourbatimentmere"
                return
            x=self.cible[0]
            y=self.cible[1]
            ang=Helper.calcAngle(self.x,self.y,x,y)  
            x1,y1=Helper.getAngledPoint(ang,self.vitesse,self.x,self.y)
            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER 
            ######## SINON TROUVER VOIE DE CONTOURNEMENT
            # ici oncalcule sur quelle case on circule
            casex=x1/self.parent.parent.taillecase
            if casex!=int(casex):
                casex=int(casex)+1
            casey=y1/self.parent.parent.taillecase
            if casey!=int(casey):
                casey=int(casey)+1
            # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
            if self.parent.parent.cartecase[int(casey)][int(casex)]>0:
                # test pour être sur que de n'est 9 (9=batiment)
                if self.parent.parent.cartecase[int(casey)][int(casex)]<9:
                    print("marche dans ",self.parent.parent.regionstypes[self.parent.parent.cartecase[int(casey)][int(casex)]])
                else:
                    print("marche dans batiment")
            ######## FIN DE TEST POUR SURFACE MARCHEE
            # si tout ba bien on continue avec la nouvelle valeur
            self.x,self.y=x1,y1 
            # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
            dist=Helper.calcDistance(self.x,self.y,x,y)
            if dist <=self.vitesse:
                if self.actioncourante=="deplacer":
                    self.actioncourante=None
                    self.cible=None
                # si on est rendu on change notre actioncourante
                if self.actioncourante=="ciblerressource":
                    self.actioncourante="ramasserressource"
                    self.cible=None
                elif self.actioncourante=="retourbatimentmere":
                    if self.typeressource=="baie" or self.typeressource=="daim":
                        self.parent.ressources["nourriture"]+=self.ramassage
                    else:
                        self.parent.ressources[self.typeressource]+=self.ramassage
                    self.ramassage=0
                    if self.cibleressource:
                        self.cibler([self.cibleressource.x,self.cibleressource.y])
                        self.actioncourante="ciblerressource"
                    else:
                        self.typeressource=None
                        self.cible=None
                        
    def chasserressource(self,typeress,id,proie):
        if proie.etat=="vivant":
            self.actioncourante="ciblerproie"
        else:
            self.actioncourante="ciblerressource"
            
        self.cibler([proie.x,proie.y])
        self.cibleressource=proie
        self.typeressource=typeress
                
    def ramasserressource(self,typeress,id):
        ress=self.parent.parent.biotopes[typeress][id]
        self.actioncourante="ciblerressource"
        self.cibler([ress.x,ress.y])
        self.cibleressource=ress
        self.typeressource=ress.montype
        
    def abandonnerressource(self,ressource):
        if ressource==self.cibleressource:
            if self.actioncourante=="ciblerressource" or self.actioncourante=="ramasserresource":
                self.actioncourante="retourbatimentmere"
                self.cibler([self.batimentmere.x,self.batimentmere.y])
            self.cibleressource=None
    
    ## PAS UTILISER POUR LE MOMENT          
    def scanneralentour(self):
        dicojoueurs=self.parent.parent.joueurs
        for i in dicojoueurs.values():
            for j in i.ouvriers.values():
                if j!=self:
                    if Helper.calcDistance(self.x,self.y,j.x,j.y) <=self.champvision:
                        pass
        return 0
                    
    def trouvercible(self,joueurs):
        c=None 
        while c== None:
            listeclesj=list(joueurs.keys())
            c=random.choice(listeclesj)
            if joueurs[c].nom != self.parent.nom:
                listeclesm=list(joueurs[c].maisons.keys())
                maisoncible=random.choice(listeclesm)
                self.cible=joueurs[c].maisons[maisoncible]
            else:
                c=None
        self.angle=Helper.calcAngle(self.x,self.y,self.cible.x,self.cible.y)
                
        
class Joueur():
    classespersos={"ouvrier":Ouvrier,
                   "soldat":Soldat,
                   "archer":Archer,
                   "chevalier":Chevalier,
                   "druide":Druide}
    def __init__(self,parent,id,nom,couleur, x,y):
        self.parent=parent
        self.nom=nom
        self.id=id
        self.x=x 
        self.y=y 
        self.couleur=couleur
        self.monchat=[]
        self.chatneuf=0
        self.ressourcemorte=[]
        self.ressources={"nourriture":200,
                         "arbre":200,
                         "roche":200,
                         "aureus":200}
        
        self.persos={"ouvrier":{},
                    "soldat":{},
                    "archer":{},
                    "chevalier":{},
                    "druide":{}}
        
        self.batiments={"maison":{},
                       "abri":{},
                       "caserne":{}}
        
        self.actions={"creerperso":self.creerperso,
                      "ouvrierciblermaison":self.ouvrierciblermaison,
                      "deplacer":self.deplacer,
                      "ramasserressource":self.ramasserressource,
                      "chasserressource":self.chasserressource,
                      "construirebatiment":self.construirebatiment,
                      "chatter":self.chatter}
        # on va creer une maison comme centre pour le joueur
        self.creerpointdorigine(x,y)
        
    def chatter(self,param):
        txt,envoyeur,receveur=param
        self.parent.joueurs[envoyeur].monchat.append(txt)
        self.parent.joueurs[receveur].monchat.append(txt)
        self.parent.joueurs[envoyeur].chatneuf=1
        self.parent.joueurs[receveur].chatneuf=1
            
    def avertirressourcemort(self,type,ress):
        for i in self.persos["ouvrier"]:
            self.persos["ouvrier"][i].abandonnerressource(ress) # ajouer libereressource
        self.parent.eliminerressource(type,ress)

    def chasserressource(self,param):
        typeress,idress,troupe=param
        for i in troupe:
            for j in self.persos.keys():
                if j=="ouvrier":
                    if i in self.persos[j]:
                        proie=self.parent.biotopes[typeress][idress]
                        self.persos[j][i].chasserressource(typeress,idress,proie)
        
    def ramasserressource(self,param):
        typeress,id,troupe=param
        for i in troupe:
            for j in self.persos.keys():
                if j=="ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].ramasserressource(typeress,id)
              
    def deplacer(self,param):
        pos,troupe=param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].cibler(pos)
                    self.persos[j][i].actioncourante="deplacer"
           
    def creerpointdorigine(self,x,y):
        idmaison=getprochainid()
        self.batiments["maison"][idmaison]=Maison(self,idmaison,self.couleur,x,y,"maison")
    
    def construirebatiment(self,param):
        sorte,pos=param
        id=getprochainid()
        self.batiments[sorte][id]=self.parent.classesbatiments[sorte](self,id,self.couleur,pos[0],pos[1],sorte)
        batiment=self.batiments[sorte][id]
        
        
        self.parent.parent.afficherbatiment(self.nom,batiment)
        self.parent.parent.vue.root.update()
        litem=self.parent.parent.vue.canevas.find_withtag(id)
        x1,y1,x2,y2=self.parent.parent.vue.canevas.bbox(litem)
        cartebatiment=self.parent.getcartebbox(x1,y1,x2,y2)
        for i in cartebatiment:
            self.parent.cartecase[i[1]][i[0]]=9
        batiment.cartebatiment=cartebatiment

# CORRECTION REQUISE : la fonction devrait en faire la demande a l'ouvrier concerne 
# trouvercible ne veut rien dire ici... à changer       
    def ouvrierciblermaison(self,listparam):
        idouvrier=listparam[0]
        self.ouvriers[idouvrier].trouvercible(self.parent.joueurs)

# transmet à tous ses persos de jouer         
    def jouerprochaincoup(self):
        for j in self.persos.keys():
            for i in self.persos[j].keys():
                self.persos[j][i].jouerprochaincoup()   
                
    def creerperso(self,param):
        sorteperso,batimentsource,idbatiment,pos=param
        id=getprochainid()
        batiment=self.batiments[batimentsource][idbatiment]
        
        x=batiment.x+100+(random.randrange(50)-15)
        y=batiment.y +(random.randrange(50)-15)
            
        self.persos[sorteperso][id]=Joueur.classespersos[sorteperso](self,id,batiment,self.couleur,x,y,sorteperso)

#######################  LE MODELE est la partie #######################
class Partie():
    def __init__(self,parent,mondict,nbrIA):
        self.parent=parent
        self.actionsafaire={}
        self.aireX=4000
        self.aireY=4000
        self.taillecase=20
        self.taillecarte=int(self.aireX/self.taillecase)
        self.cartecase=0
        self.makecartecase(self.taillecarte)
        self.delaiprochaineaction=20
        self.joueurs={}
        self.classesbatiments={"maison":Maison,
                        "caserne":Caserne,
                        "abri":Abri}
        self.classespersos={"ouvrier":Ouvrier,
                    "soldat":Soldat,
                    "archer":Archer,
                    "chevalier":Chevalier,
                    "druide":Druide}
        self.ressourcemorte=[]
        self.listebiotopes=[]
        #self.
        self.biotopes={"daim":{},
                         "arbre":{},
                         "roche":{},
                         "aureus":{},
                         "eau":{},
                         "marais":{},
                         "baie":{}}
        self.regions={}
        self.regionstypes={0:["plaine",0,0,0,"pale green"],
                           1:["arbre",10,10,10,"forest green"],
                           2:["eau",3,10,10,"light blue"],
                           3:["marais",3,8,8,"DarkSeaGreen3"],
                           4:["roche",16,6,3,"gray60"],
                           5:["aureus",12,4,3,"gold2"],}
        self.creerregions()
        self.creerbiotopes()
        self.creerpopulation(mondict,nbrIA)
    
    def creerbiotopes(self):
        # creer des daims éparpillés
        n=40
        while n:
            x=random.randrange(self.aireX)
            y=random.randrange(self.aireY)
            case=self.trouvercase(x,y)
            if self.cartecase[case[1]][case[0]]==0:
                id=getprochainid()
                daim=Daim(self,id,x,y)
                self.biotopes["daim"][id]=daim
                n-=1
        self.creerbiotope("arbre","arbre",Arbre)
        self.creerbiotope("roche","roche",Roche)
        self.creerbiotope("eau","eau",Eau)
        self.creerbiotope("marais","marais",Marais)
        self.creerbiotope("aureus","aureus",Aureus)
    
    def creerbiotope(self,region,ressource,typeclasse):# creation des forets
        typeressource=typeclasse.typeressource
        
        for listecase in self.regions[region]:
            nressource=random.randrange(int(len(listecase)/3))+int((len(listecase)/3))
            while nressource:
                pos=random.choice(listecase)
                x=random.randrange(self.taillecase)
                y=random.randrange(self.taillecase)
                xa=(pos[0]*self.taillecase)+x
                ya=(pos[1]*self.taillecase)+y
                
                styleress=random.choice(typeressource)
                id=getprochainid()
                objet=typeclasse(self,id,styleress,xa,ya,ressource)
                self.biotopes[ressource][id]=(objet)
                self.listebiotopes.append(objet)
                nressource-=1
                          
    def creerregions(self):
        for k,reg in self.regionstypes.items():
            self.regions[reg[0]]=[]     # la clé de région
            for i in range(reg[1]):
                listecasereg=[]
                x=random.randrange(self.taillecarte)
                y=random.randrange(self.taillecarte)
                taillex=random.randrange(reg[2])+reg[3]
                tailley=random.randrange(reg[2])+reg[3]
                x=x-int(taillex/2)
                if x<0:
                    taillex-=x
                    x=0
                y=y-int(tailley/2)
                if y<0:
                    tailley-=y
                    y=0
                x0=x
                y0=y
                listereg=[]
                for i in range(tailley):
                    for j in range(taillex):
                        self.cartecase[y][x]
                        self.cartecase[y][x]=k
                        listereg.append([x,y])
                        x+=1
                        if x>=self.taillecarte:
                            x=self.taillecarte-1
                            break
                    y+=1
                    x=x0
                    if y>=self.taillecarte:
                        y=self.taillecarte-1
                        break
                self.regions[reg[0]].append(listereg)   # Assignation de région pour chaque case
                
        
    def creerpopulation(self,mondict,nbrIA):
        couleurs=[["R","red"],["B","blue"],["J","yellow"],["V","lightgreen"]]
        quadrants=[[[0,0],[int(self.aireX/2),int(self.aireY/2)]],
                   [[int(self.aireX/2),0],[self.aireX,int(self.aireY/2)]],
                   [[0,int(self.aireY/2)],[int(self.aireX/2),self.aireY]],
                   [[int(self.aireX/2),int(self.aireY/2)],[self.aireX,self.aireY]]]
        nquad=4
        bord=50
        for i in mondict:
            id=getprochainid()
            coul=couleurs.pop()
            # placer les joueurs dans des quandrants differents
            choixquad=random.choice(range(nquad))
            nquad-=1
            quad=quadrants.pop(choixquad)
            
            n=1
            while n:
                x=random.randrange(quad[0][0]+bord,quad[1][0]-bord)
                y=random.randrange(quad[0][1]+bord,quad[1][1]-bord)
                case=self.trouvercase(x,y)
                if self.cartecase[case[1]][case[0]]==0:
                    self.joueurs[i]=Joueur(self,id,i,coul,x,y)
                    n=0
            
    # Cette methode est une amorce non-fonctionnel a l'IA       
    #def creerIA(self):    
    #    #AJOUTS IA dans la methode partie.creerpopulation
    #    lesIAs=[]
    #    for i in range(int(nbrIA)):
    #        lesIAs.append("IA_"+str(i))
    #          
    #    for i in lesIAs:
    #        id=getprochainid()
    #        x=random.randrange(self.aireX)
    #        y=random.randrange(self.aireY)
    #        self.joueurs[i]=IA(self,id,i,x,y)
            
    def deplacer(self):
        for i in self.joueurs:
            self.joueurs[i].deplacer()
            
    def jouerprochaincoup(self,cadrecourant):
        self.ressourcemorte=[]
        ##################################################################
        # faire nouvelle action recu du serveur si on est au bon cadrecourant
        # ATTENTION : NE PAS TOUCHER 
        if cadrecourant in self.actionsafaire:
            for i in self.actionsafaire[cadrecourant]:
                self.joueurs[i[0]].actions[i[1]](i[2])
        ##################################################################
        
        # demander aux objets de s'activer
        for i in self.biotopes["daim"].keys():
            self.biotopes["daim"][i].deplacer()
            
        # demander aux objets de s'activer
        for i in self.joueurs.keys():
            self.joueurs[i].jouerprochaincoup()
            
        self.faireactionpartie()
        
    def faireactionpartie(self):
        if self.delaiprochaineaction==0:
            self.produireaction()
            self.delaiprochaineaction=random.randrange(20,30)
        else:
            self.delaiprochaineaction-=1
            
    def produireaction(self):
        typeressource=Baie.typeressource
        n=1
        while n:
            x=random.randrange(self.aireX)
            y=random.randrange(self.aireY)
            case=self.trouvercase(x,y)
            if self.cartecase[case[1]][case[0]]==0:
                id=getprochainid()
                img=random.choice(typeressource)
                baie=Baie(self,id,img,x,y,"baie")
                self.biotopes["baie"][id]=baie
                n-=1
                self.parent.afficherbio(baie)
        
            
# VERIFIER CES FONCTIONS SUR LA CARTECASE
    def makecartecase(self,taille):
        self.cartecase=[]
        for i in range(taille):
            t1=[]
            for j in range(taille):
                t1.append(0)
            self.cartecase.append(t1)  
    
    def trouvercase(self,x,y):
        cx=int(x/self.taillecase) 
        cy=int(y/self.taillecase)
        if cx!=0 and x%self.taillecase>0:
            cx+=1
            
        if cy!=0 and y%self.taillecase>0:
            cy+=1
            
        # possible d'etre dans une case trop loin
        if cx==self.taillecarte:
            cx-=1
        if cy==self.taillecarte:
            cy-=1
        return [cx,cy]
    
    def getcartebbox(self,x1,y1,x2,y2):# case d'origine en cx et cy,  pour position pixels x, y
         # case d'origine en cx et cy,  pour position pixels x, y
        if x1<0:
            x1=1
        if y1<0:
            y1=1
        if x2>=self.aireX:
            x2=self.aireX-1
        if y2>=self.aireY:
            y2=self.aireY-1
        
        cx1=int(x1/self.taillecase) 
        cy1=int(y1/self.taillecase) 
        
        cx2=int(x2/self.taillecase) 
        cy2=int(y2/self.taillecase)
        t1=[]
        for i in range(cy1,cy2):
            for j in range(cx1,cx2):
                case=self.cartecase[i][j]
                t1.append([j,i])
        return t1  
        
# CORRECTION REQUISE : PAS SUR QUE CETTE FONCITON SOIT ENCORE REQUISE
# VA DEPENDRE DE L'IMPLANTATION S'IL Y A TROP D'OBJETS À VÉRIFIER
    def getsubcarte(self,x,y,d):
       
        cx=int(x/self.taillecase) 
        cy=int(y/self.taillecase) 
        # possible d'etre dans une case trop loin
        if cx==self.largeurcase:
            cx-=1
        if cy==self.hauteurcase:
            cy-=1
        
        # le centre en pixels de la case d'origine
        pxcentrex=(cx*self.taillecase)+self.demicase
        pxcentrey=(cy*self.taillecase)+self.demicase
        
        # la case superieur gauche de la case d'origine
        casecoinx1=cx-d
        casecoiny1=cy-d
        # assure qu'on deborde pas
        if casecoinx1<0:
            casecoinx1=0
        if casecoiny1<0:
            casecoiny1=0
        # la case inferieur droite
        casecoinx2=cx+d
        casecoiny2=cy+d
        # assure qu'on deborde pas
        if casecoinx2 >= self.largeurcase:
            casecoinx2=self.largeurcase-1
        if casecoiny2>=self.hauteurcase:
            casecoiny2=self.hauteurcase-1

        distmax=(d*self.taillecase)+self.demicase
        
        t1=[]
        for i in range(casecoiny1,casecoiny2):
            for j in range(casecoinx1,casecoinx2):
                case=self.carte[i][j]
                pxcentrecasex=(j*self.taillecase)+self.demicase
                pxcentrecasey=(i*self.taillecase)+self.demicase
                distcase=H.calcDistance(pxcentrex,pxcentrey,pxcentrecasex,pxcentrecasey)
                if distcase<=distmax:
                    t1.append(case)
        return t1  
    
    def eliminerressource(self,type,ress):
        self.biotopes[type].pop(ress.id)
        self.ressourcemorte.append(ress)
        
    #############################################################################    
    # ATTENTION : NE PAS TOUCHER                 
    def ajouteractionsafaire(self,actionsrecues):
        for i in actionsrecues:
            cadrecle=i[0]
            action=ast.literal_eval(i[1])

            if cadrecle not in self.actionsafaire.keys():
                self.actionsafaire[cadrecle]=[action] 
            else:
                self.actionsafaire[cadrecle].append(action)
    ##############################################################################
