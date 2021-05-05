## - Encoding: UTF-8 -*-

import ast
import random
import math
from helper import Helper
from RTS_divers import *
from _overlapped import NULL
from RTS_upgrades import *

class DebugSettings(): # Va permettre de dbug bien des affaires
    debugMode = True            
    showAttackRange = True      # Indicateur du range d'attack des unités
    
    # Settings de lancement de partie
    spawnPlayersNearby = True   # Spawn tout les joueurs très proche
    generateAi = True           # Start une game avec des ai (pour l'instant ce sont des joueurs inactifs)
    createAllUnitsAndBuildings = False   # Créer tout les bâtiments et unités qui existent lors du lancement du jeu
    quickStart = True           # Reset create et launch une partie, immédiatement

class ARMOR_TYPES():
    LIGHT = 'LIGHT'
    HEAVY = 'HEAVY'
    SUPRA_HARD = 'SUPRA_HARD'

class SimpleTimer():
    def __init__(self, parent, interval):
        self.parent = parent
        self.interval = interval
        self.counter = 0
        self.running = True
    # Une alternative serait de juste setté un point future, et de checker si on est rendu
    # AddDelay(time + duration)
    # tick -> if time >= pointfuture: 
    #             timer est finit


    def set(self, interval):
        try :
            if interval > 0:  # Pas de counter négatif
                self.counter = 0
                self.interval = interval
                self.running = True
        except ValueError :
                print("Timer null ou négatif is no bueno")
    
    def isRunning(self): 
        return self.running 

    def tick(self):
        self.counter += 1 

        if self.counter >= self.interval: 
            self.running = False
            return True # Counter finis
        else:
            return False

    def start(self):  
        self.counter = 0
        self.running = True

    def stop(self): 
        self.counter = self.interval = 0



class Batiment():
    def __init__(self,parent,id, couleur,x,y,montype, cloningPrototype = True):
        if cloningPrototype:
            self.parent=parent
            self.id=id
            self.x=x
            self.y=y

            # S'ajoute sur la map
            casex2,casey2 = self.parent.parent.trouvercase(x, y)           
            self.parent.parent.hashmap[casex2][casey2]["batiments"].append(self)    

            self.montype=montype
            self.image=couleur[0]+"_"+montype

            self.cartebatiment=[]
            self.alive = True
        else:
            # Le prototype de base va avoir ces stats. Tout les clones vont copier les attributs du prototype de bases
            self.health = self.maxHealth = 0
            self.defense = 2
            self.maxperso = 0
            self.perso = 0
            self.armorType = ARMOR_TYPES.HEAVY

    def copyAttributes(self, prototype):  
        self.health = prototype.health
        self.maxHealth = prototype.health
        self.defense = prototype.defense
        self.armorType = prototype.armorType
        self.maxperso = prototype.maxperso
        self.perso = prototype.perso


    def clone():     # Abstract
        return

    def die(self):
        self.alive = False
        self.health = 0
        self.parent.addToListOfDeadStuff(False, self.montype, self.id) # S'ajoute à la liste des choses qui sont dead
        #self.parent.avertirressourcemort(self.typeressource,self.cibleressource)              
        
        # Retire de la tile map
        tile = self.parent.parent.trouvercase(self.x, self.y) 
        if self in self.parent.parent.hashmap[tile[0]][tile[1]]["batiments"]:    # safety measures
                    self.parent.parent.hashmap[tile[0]][tile[1]]["batiments"].remove(self)    

        
class Maison(Batiment):
    def __init__(self,parent,id,couleur,x,y,montype, prototype = None):
        Batiment.__init__(self,parent,id, couleur,x, y, montype, prototype)

        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de defenses 
            self.health = self.maxHealth = 300
            self.defense = 2
            self.maxperso=10    # useless for now
            self.perso=0        # useless for now

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,couleur,x,y,montype, prototype):       
        return Maison(parent,id,couleur,x,y,montype, prototype)


class Abri(Batiment):
    def __init__(self,parent,id,couleur,x,y,montype, prototype = None):
        Batiment.__init__(self,parent,id, couleur, x, y, montype, prototype)

        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de defenses 
            self.health = self.maxHealth = 300
            self.defense = 2
            self.maxperso=20
            self.perso=0

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,couleur,x,y,montype, prototype):       
        return Abri(parent,id,couleur,x,y,montype, prototype)
        
class Caserne(Batiment):
    def __init__(self,parent,id,couleur,x,y,montype, prototype = None):
        Batiment.__init__(self,parent,id, couleur, x, y, montype, prototype)


        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de defenses 
            self.health = self.maxHealth = 300
            self.defense = 2
            self.maxperso=20
            self.perso=0

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,couleur,x,y,montype, prototype):       
        return Caserne(parent,id,couleur,x,y,montype, prototype)

class ChickenCoop(Batiment):
    def __init__(self,parent,id,couleur,x,y,montype, prototype = None):
        Batiment.__init__(self,parent,id, couleur,x, y, montype, prototype)

        if prototype:
            self.copyAttributes(prototype)

            self.maxperso=20
            self.perso=0
        else:
            # Stats de defenses 
            self.health = self.maxHealth = 500
            self.defense = 2

    def copyAttributes(self, prototype):
        print(super())
        print(super)

        super().copyAttributes(prototype)

    def clone(parent,id,couleur,x,y,montype, prototype):       
        return ChickenCoop(parent,id,couleur,x,y,montype, prototype)

class PigPen(Batiment):
    def __init__(self,parent,id,couleur,x,y,montype, prototype = None):
        Batiment.__init__(self,parent,id, couleur,x, y, montype, prototype)
        
        if prototype:
            self.copyAttributes(prototype)

        else:
            # Stats de defenses 
            self.health = self.maxHealth = 500
            self.defense = 2
            self.maxperso=20
            self.perso=0

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,couleur,x,y,montype, prototype):       
        return PigPen(parent,id,couleur,x,y,montype, prototype)
        
class Daim():
    def __init__(self,parent,id,x,y):
        self.parent=parent
        self.id=id
        self.etat="vivant"
        self.x=x
        self.y=y
        self.valeur=random.randrange(20, 100)
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
        self.valeur=random.randrange(20, 100)
                    
class Arbre(Biotope):
    typeressource=['arbre0grand',
                   'arbre0petit',
                   'arbre1grand',
                   'arbre2grand',
                   'arbresapin0grand',
                   'arbresapin0petit']
    def __init__(self,parent,id,monimg,x,y,montype):
        Biotope.__init__(self,parent,id,monimg,x,y,montype)
        self.valeur=random.randrange(20, 100) 
        
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
    def __init__(self,parent,id,batiment,couleur,x,y,montype, cloningPrototype = True):
        if cloningPrototype:   # Si on clone pas, on créer un prototype. Le prototype n'existeras pas dans le jeu, il n'aura donc pas besoins de ces attributs
            self.parent=parent
            self.id=id
            self.type = montype
            self.actioncourante = None
            self.batimentmere=batiment
            self.dir="D"
            self.image=couleur[0]+"_"+montype+self.dir
            self.x=x
            self.y=y
            
            self.movingIn = False
            
            # S'ajoute sur la map
            caseX,caseY = self.parent.parent.trouvercase(x, y)           
            self.parent.parent.hashmap[caseX][caseY]["persos"].append(self)    

            self.alive = True
            self.cible=[]
            self.canAttack = True
            self.attackTarget=[]
            self.angle=None

            self.actions = {
                "deplacer":self.deplacer,
                "setAttackTarget":self.setAttackTarget,
                "attack": self.attack,
                }

        else: # Le prototype de base va avoir ces stats. Tout les clones vont copier les attributs du prototype
            self.health = 0
            self.maxHealth = 0
            self.defense = 0
            self.vitesse = 5
            self.champvision = 200
            self.atkDmg = 0
            self.atkRange = 10   # Default pour melee unit
            self.atkSpeed = 0    # Nombre de ticks par attaque
            self.attackTimer = None
            self.armorType = ARMOR_TYPES.LIGHT
            self.mana=0
            
    def clone():     # Abstract
        return

    def copyAttributes(self, prototype):  # MUST BE TESTED
        self.health = prototype.health
        self.maxHealth = prototype.health
        self.defense = prototype.defense
        self.vitesse = prototype.vitesse
        self.champvision = prototype.champvision
        self.atkDmg = prototype.atkDmg
        self.atkRange = prototype.atkRange
        self.atkSpeed = prototype.atkSpeed
        self.attackTimer = SimpleTimer(self, self.atkSpeed)
        self.armorType = prototype.armorType
        self.mana = prototype.mana

#---- Si on revampe tout l'AI, on passe par ici

    def updateAction(self):
        # méthode d'action à faire
        return 
        
    def update(self):
        self.deplacer() 
        self.updateAction()
        
        # Update other stuff
        
#---- Si on revampe tout l'AI, on passe par ici


    def jouerprochaincoup(self):
        if self.attackTimer.isRunning():
            if self.attackTimer.tick():
                self.canAttack = True

        self.deplacer()
        if self.actioncourante == "attack":
            self.attack()
        else:
            if self.actioncourante == None:
                self.targetNearestEnnemy()
            
    def deplacer(self):
        if self.cible and self.movingIn:
            ang=Helper.calcAngle(self.x,self.y,self.cible[0],self.cible[1])  
            x,y=Helper.getAngledPoint(ang,self.vitesse,self.x,self.y)
            
            casex1,casey1 = self.parent.parent.trouvercase(self.x, self.y) # Case départ
            casex2,casey2 = self.parent.parent.trouvercase(x, y)           # Case d'arrivé
            self.x,self.y=x,y # Avance le tit bonhomme. Pourrait sortir de la map je suppose
            
            if casex1 != casex2 or casey1 != casey2: 
                if self in self.parent.parent.hashmap[casex1][casey1]["persos"]:    # safety measures
                    self.parent.parent.hashmap[casex1][casey1]["persos"].remove(self)    
                
                self.parent.parent.hashmap[casex2][casey2]["persos"].append(self)    # Ajout de la map

                # if self.parent.parent.cartecase[casex2][casey2]>0:  # Test pour un semblant d'hitbox
                #     print("marche dans ",self.parent.parent.regionstypes[self.parent.parent.cartecase[casex2][casey2]])
                
            if Helper.withinDistance(self.x, self.y, self.cible[0], self.cible[1], self.vitesse):    
                if self.actioncourante == "deplacer":
                    self.actioncourante = None
                self.cible=None 

    # Vérifie si la cible est valide pour une attaque. 
    def setAttackTarget(self, cible):        
        if cible.parent != self.parent: # SAFETY: Si ennemie    
            if isinstance(cible, Perso) or isinstance(cible, Batiment): # Si bâtiment || person
                self.attackTarget = cible
                self.actioncourante ="attack"
                return True
        return False
                
        
    def attack(self):        
        if self.attackTarget and self.attackTarget.alive:    # Cible pas dead
            if Helper.withinDistance(self.x, self.y, self.attackTarget.x, self.attackTarget.y, self.atkRange):    # Range d'attack
                self.movingIn = False   # Arrêt du mouvement si peut attaquer à distance
                if self.canAttack:  # Si le cooldown de l'attaque est terminé
                    self.attackTarget.health = self.dealDamage(self.attackTarget)
                    self.attackTimer.set(self.atkSpeed) # Start cooldown pour prochaine attaque quand même. Tuer une cible ne reset pas le cooldown d'attaque
                    self.canAttack = False
                    #self.startNewAttack()# Ici la spécificité de l'attaque peut être déterminé, ex: lance un projectile, swing son arme etc...
                    
                if self.attackTarget.health <= 0: # Si la cible meurt ici, faut arrêter de la target
                    self.attackTarget.die() # et la buter
                    self.resetAction()
                    
                return
            else:
                if self.movingIn == False:
                    self.movingIn = True
                        
            if self.cible == None:
                self.cibler([self.attackTarget.x, self.attackTarget.y])
        else:
            self.resetAction()

        
    
    def dealDamage(self, target):
        # Check si ya boost de dmg selon le type d'armor et de dmg
        # ex: if dmgtype = FEU and armor = BOIS
        # bonusDmg = 0.15
        # dmg = self.atkDmg + self.atkDmg * bonusDmg
        dmg = self.atkDmg - target.defense

        if dmg < 1: # Comme dans les autres jeux du genre, le dmg minimum est toujours 1
            dmg = 1

        return target.health - dmg

    def resetAction(self):
        self.movingIn = False
        self.cible = self.attackTarget = self.actioncourante = None


    def die(self):
        self.alive = False
        self.cible = None
        self.attackTarget = None
        self.health = 0
        self.parent.addToListOfDeadStuff(True, self.type, self.id) # S'ajoute à la liste des choses qui sont dead

        # Retire de la tile map
        tile = self.parent.parent.trouvercase(self.x, self.y) 
        if self in self.parent.parent.hashmap[tile[0]][tile[1]]["persos"]:    # safety measures
                    self.parent.parent.hashmap[tile[0]][tile[1]]["persos"].remove(self)    


    def cibler(self,pos):
        self.cible=pos
        if self.x<self.cible[0]:
            self.dir="D"
        else:
            self.dir="G"
        self.image=self.image[:-1]+self.dir

        self.movingIn = True


    # Une autre méthodes pourrait être intégré pour prioriser les ennemies les plus 'dangereux', au besoin
    def targetNearestEnnemy(self):
        ennemyUnits = []
        ennemyBuildings = []
        nearestEnnemy = None

        # Consulte hashmap
        tilesAround = self.parent.parent.getOccupiedTilesAround(self.x,self.y,self.champvision)
        
        for t in tilesAround:
            for p in t["persos"]: # Ajout de tout les unités ennemies
                if p.parent != self.parent: # Si ennemie !   
                    ennemyUnits.append(p)
            for b in t["batiments"]:  # Ajout de tout les batiments ennemis
                if b.parent != self.parent: # Si ennemie !   
                    ennemyBuildings.append(b)

        if ennemyUnits:
            nearestEnnemy = Helper.findNearest(self.x, self.y, ennemyUnits) # Priorise toujours les unités sur les batiments
        else: 
            nearestEnnemy = Helper.findNearest(self.x, self.y, ennemyBuildings)

        # AH-TTACK
        if nearestEnnemy:
            self.setAttackTarget(nearestEnnemy)
            self.cibler([nearestEnnemy.x,nearestEnnemy.y])
            return True
        else:
            return False



class Soldat(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype, prototype = None):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype, prototype)
        
        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de combats
            self.health = self.maxHealth = 100
            self.defense = 0
            self.atkDmg = 6
            self.atkSpeed = 5

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,batiment,couleur,x,y,montype, prototype):       
        return Soldat(parent,id,batiment,couleur,x,y,montype, prototype)

class Archer(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype,prototype = None):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype, prototype)
        
        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de combats
            self.health = self.maxHealth = 60
            self.defense = 0
            self.atkRange = 30   
            self.atkSpeed = 7

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,batiment,couleur,x,y,montype, prototype):       
        return Archer(parent,id,batiment,couleur,x,y,montype, prototype)


class Chevalier(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype, prototype = None):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype, prototype)
        
        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de combats
            self.health = self.maxHealth = 200
            self.defense = 1
            self.armorType = ARMOR_TYPES.HEAVY
            self.atkDmg = 15
            self.atkSpeed = 2

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,batiment,couleur,x,y,montype, prototype):       
        return Chevalier(parent,id,batiment,couleur,x,y,montype, prototype)

class Druide(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype,prototype = None):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype, prototype)

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,batiment,couleur,x,y,montype, prototype):       
        return Druide(parent,id,batiment,couleur,x,y,montype, prototype)

class Chicken(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype,prototype = None):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype, prototype)
       
        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de combats
            self.health = self.maxHealth = 200
            self.defense = 1
            self.armorType = ARMOR_TYPES.LIGHT
            self.atkDmg = 15
            self.atkRange = 200   
            self.atkSpeed = 10

    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

    def clone(parent,id,batiment,couleur,x,y,montype, prototype):       
        return Chicken(parent,id,batiment,couleur,x,y,montype, prototype)

class Pig(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype,prototype = None):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype, prototype)
        
        
        if prototype:
            self.copyAttributes(prototype)
        else:
            # Stats de combats
            self.health = self.maxHealth = 400
            self.defense = 1
            self.armorType = ARMOR_TYPES.HEAVY
            self.atkDmg = 30
            self.atkSpeed = 2


    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)


    def clone(parent,id,batiment,couleur,x,y,montype, prototype):       
        return Pig(parent,id,batiment,couleur,x,y,montype, prototype)

               
class Ouvrier(Perso):
    def __init__(self,parent,id,maison,couleur,x,y,montype, prototype = None):
        Perso.__init__(self,parent,id,maison,couleur,x,y,montype, prototype)

        if prototype:
            self.copyAttributes(prototype)
            
            self.cibleressource=None
            self.typeressource=None
            self.cibletemp=None
            self.javelots=[]
            self.ramassage=0

            # Actions supplémentaires
            self.actions["gather"] = self.ramasserressource
            self.actions["hunt"] = self.chasserressource
            self.tickInactive=0
            #self.actions["build"] = self.build

        else:
            # Stats du prototype de base
            self.vitesse=random.randrange(5)+5
            self.health = self.maxHealth = 50
            self.defense = 0
            self.atkDmg = 2
            self.atkSpeed = 5
            self.champvision=random.randrange(50)+150

            # Attributs uniques aux ouvriers
            self.quota=20 
            self.champchasse= 120
            self.dejavisite=[]
            

            
    def copyAttributes(self, prototype):
        super().copyAttributes(prototype)

        self.quota = prototype.quota 
        self.champchasse = prototype.champchasse


    def clone(parent,id,batiment,couleur,x,y,montype, prototype):        # Retourne une copie de soi-même
        return Ouvrier(parent,id,batiment,couleur,x,y,montype, prototype)

    def jouerprochaincoup(self):
        if not self.actioncourante:
            self.tickInactive+=1
            if self.tickInactive >= 100:
                self.automaticAction()
        elif self.tickInactive > 0:
            self.tickInactive=0
            
        if self.attackTimer.isRunning():
            if self.attackTimer.tick():
                self.canAttack = True

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
                nearTarget = self.findNearRessource()
                if not nearTarget:
                    self.actioncourante="retourbatimentmere"
                    self.cibleressource=None
                else:
                    self.ramasserressource(nearTarget[0], nearTarget[1])
            
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
        elif self.actioncourante=="attack":
            self.deplacer()
            self.attack()
                
    def automaticAction(self):
        for k, bio in self.parent.parent.biotopes.items():
            if k != "eau" or k != "marais":
                for k2, bio2 in bio.items():
                    if bio2.x < self.x + self.champvision and bio2.x > self.x - self.champvision and bio2.y < self.y + self.champvision and bio2.y > self.y - self.champvision:
                        if k == "daim":
                            self.chasserressource(k, k2, bio2)
                        else:
                            self.ramasserressource(k, k2)
                        return
                    
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
                self.parent.avertirressourcemort(self.typeressource,self.cibleressource)
                
            if self.ramassage >= self.quota:
                self.actioncourante="retourbatimentmere"
                self.cibler([self.batimentmere.x,self.batimentmere.y])
            self.x=self.x+random.randrange(4)-2
            self.y=self.y+random.randrange(4)-2
            
    def findNearRessource(self):
        for k, bio in self.parent.parent.biotopes.items():
            if k == self.typeressource and k != "daim":
                for k2, bio2 in bio.items():
                    if bio2.x < self.cibleressource.x + self.champvision and bio2.x > self.cibleressource.x - self.champvision and bio2.y < self.cibleressource.y + self.champvision and bio2.y > self.cibleressource.y - self.champvision and self.cibleressource != bio2:
                        nearTarget = [k, k2]
                        return nearTarget
            
    def deplacer(self):
        if self.cible:
            if self.actioncourante=="ciblerressource" and not self.cibleressource:
                self.actioncourante="retourbatimentmere"
                return

            ang=Helper.calcAngle(self.x,self.y,self.cible[0],self.cible[1])  
            x,y=Helper.getAngledPoint(ang,self.vitesse,self.x,self.y)
            
            casex1,casey1 = self.parent.parent.trouvercase(self.x, self.y) # Case départ
            casex2,casey2 = self.parent.parent.trouvercase(x, y)           # Case d'arrivé
            self.x,self.y=x,y # Avance le tit bonhomme. Pourrait sortir de la map je suppose
            
            if casex1 != casex2 or casey1 != casey2: 
                if self in self.parent.parent.hashmap[casex1][casey1]["persos"]:    # safety measures
                    self.parent.parent.hashmap[casex1][casey1]["persos"].remove(self)    
                
                self.parent.parent.hashmap[casex2][casey2]["persos"].append(self)    # Ajout sur la map

                # if self.parent.parent.cartecase[casex2][casey2]>0:  # Test pour un semblant d'hitbox
                #     print("marche dans ",self.parent.parent.regionstypes[self.parent.parent.cartecase[casex2][casey2]])
                
            if Helper.withinDistance(self.x, self.y, self.cible[0], self.cible[1], self.vitesse):    
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
                        self.actioncourante=None
                else:
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
            nearTarget = self.findNearRessource()
            if not nearTarget:
                if self.actioncourante=="ciblerressource" or self.actioncourante=="ramasserressource":  
                    self.actioncourante="retourbatimentmere"
                    self.cibler([self.batimentmere.x,self.batimentmere.y])  
                self.cibleressource=None
            else:
                if self.ramassage >= self.quota:
                    self.cibleressource = self.parent.parent.biotopes[nearTarget[0]][nearTarget[1]]
                else:
                    self.ramasserressource(nearTarget[0], nearTarget[1])
    
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
                   "druide":Druide,
                   "chicken":Chicken,
                   "pig":Pig}
    def __init__(self,parent,id,nom,couleur, x,y):

        self.parent=parent
        self.nom=nom
        self.id=id
        self.x=x 
        self.y=y 
        self.couleur=couleur
        self.monchat=[]
        self.chatneuf=0
        self.ressourcemorte=[]#
        self.ressources={"nourriture":200,
                         "arbre":200,
                         "roche":200,
                         "aureus":200}
        
        self.persos={"ouvrier":{},
                    "soldat":{},
                    "archer":{},
                    "chevalier":{},
                    "druide":{},
                    "chicken":{},
                    "pig":{}}
        
        self.prototypePersos={"ouvrier": self.classespersos["ouvrier"](None, None, None,None,None,None,None,None), #none! yep, overloading constructor would prevent that.
                    "soldat":self.classespersos["soldat"](None, None, None,None,None,None,None,None),
                    "archer":self.classespersos["archer"](None, None, None,None,None,None,None,None),
                    "chevalier":self.classespersos["chevalier"](None, None, None,None,None,None,None,None),
                    "druide":self.classespersos["druide"](None, None, None,None,None,None,None,None),
                    "chicken":self.classespersos["chicken"](None, None, None,None,None,None,None,None),
                    "pig":self.classespersos["pig"](None, None, None,None,None,None,None,None)}

        self.prototypeBatiments={"maison": self.parent.classesbatiments["maison"](None, None, None,None,None,None,None), 
                    "caserne":self.parent.classesbatiments["caserne"](None, None, None,None,None,None,None),
                    "abri":self.parent.classesbatiments["abri"](None, None, None,None,None,None,None),
                    "chickenCoop":self.parent.classesbatiments["chickenCoop"](None, None, None,None,None,None,None),
                    "pigPen":self.parent.classesbatiments["pigPen"](None, None, None,None,None,None,None)
                    }

        self.batiments={"maison":{},
                       "abri":{},
                       "caserne":{},
                       "chickenCoop":{},
                       "pigPen":{}}
        
        self.actions={"creerperso":self.creerperso,
                      "ouvrierciblermaison":self.ouvrierciblermaison,
                      "deplacer":self.deplacer,
                      "ramasserressource":self.ramasserressource,
                      "chasserressource":self.chasserressource,
                      "construirebatiment":self.construirebatiment,
                      "chatter":self.chatter,
                      "setAttackTarget":self.setAttackTarget,
                      }

        # on va creer une maison comme centre pour le joueur
        self.creerpointdorigine(x,y)
        self.completedUpgrades = {}     # ex : {"Protein shakes": ProteinShake}
        UpgradeRegistry.UPGRADES["Defense Tier 3"].effect(self)
        
    def addToListOfDeadStuff(self, isPerso, type, id):
        if isPerso:
            self.ressourcemorte.append(self.persos[type][id])
            del self.persos[type][id]
        else:
            self.ressourcemorte.append(self.batiments[type][id])
            del self.batiments[type][id]

    def sendListOfDeadStuff(self):
        for i in self.ressourcemorte:
            self.parent.ressourcemorte.append(i)
        self.ressourcemorte = []

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

    # Cible unité ennemie à attaquer
    def setAttackTarget(self,param):
        targetId, isPerso, targetType, enemyPlayerName, units = param
        target = None # Doit trouvé la cible selon l'id fournie

        # Doit chercher la target dans la liste des persos    
        if isPerso == 'perso':
            if targetId in self.parent.joueurs[enemyPlayerName].persos[targetType]:
                target = self.parent.joueurs[enemyPlayerName].persos[targetType][targetId]
        else:
            targetType = isPerso # le tag numero [1] devient le targetType dans ce contexte ci, beceause? "Spaghetti"
            if targetId in self.parent.joueurs[enemyPlayerName].batiments[targetType]: 
                target = self.parent.joueurs[enemyPlayerName].batiments[targetType][targetId]

        # L'action
        for u in units:
            for j in self.persos.keys():
                if u in self.persos[j]:
                    self.persos[j][u].setAttackTarget(target) 
                    self.persos[j][u].cibler([target.x,target.y])   #   Même si la target n'est pas valide pour une attaque, les perso vont se déplacer quand même
                    break

    # Ajouter les unités et bâtiments qu'on veut à l'initialisation ici   
    def creerpointdorigine(self,x,y):
        idmaison=getprochainid()
        self.batiments["maison"][idmaison]=Maison(self,idmaison,self.couleur,x,y,"maison",self.prototypeBatiments["maison"])
        self.creerperso(["ouvrier","maison",idmaison,[]])
        
        # Pour debug plus rapidement
        if DebugSettings.createAllUnitsAndBuildings:
            nextId = getprochainid()    # Le bâtiment est invisible, et source de bug 
            self.batiments["chickenCoop"][nextId]= ChickenCoop(self,nextId ,self.couleur, x + 25 , y - 100,"chickenCoop")    # Peut crash si spawn trop près d'une bordure, probablement
            self.creerperso(["chicken","chickenCoop",nextId,[]])

            
        
    
    def construirebatiment(self,param):
        sorte,pos=param
        id=getprochainid()
        
        self.batiments[sorte][id]=self.parent.classesbatiments[sorte](self,id,self.couleur,pos[0],pos[1],sorte, self.prototypeBatiments[sorte])
        # self.batiments[sorte][id]=self.parent.classesbatiments[sorte](self,id,self.couleur,pos[0],pos[1],sorte)
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

        if self.ressourcemorte:
            self.sendListOfDeadStuff()
                
    def creerperso(self,param):
        sorteperso,batimentsource,idbatiment,pos=param
        id=getprochainid()
        batiment=self.batiments[batimentsource][idbatiment]
        
        x=batiment.x+100+(random.randrange(50)-15)
        y=batiment.y +(random.randrange(50)-15)
            
        #if sorteperso == "ouvrier":
        self.persos[sorteperso][id]=Joueur.classespersos[sorteperso].clone(self,id,batiment,self.couleur,x,y,sorteperso, self.prototypePersos[sorteperso])
        #else:    
        #    self.persos[sorteperso][id]=Joueur.classespersos[sorteperso](self,id,batiment,self.couleur,x,y,sorteperso)

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
        self.hashmap = None     # contiendra tout les données sur l'emplacements des unités et batiments

        self.makecartecase(self.taillecarte)
        self.delaiprochaineaction=20
        self.joueurs={}
        self.classesbatiments={"maison":Maison,
                        "caserne":Caserne,
                        "abri":Abri,
                        "chickenCoop":ChickenCoop,
                        "pigPen":PigPen}
        self.classespersos={"ouvrier":Ouvrier,
                    "soldat":Soldat,
                    "archer":Archer,
                    "chevalier":Chevalier,
                    "druide":Druide,
                    "chicken":Chicken,
                    "pig":Pig}
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
        
        self.creerpopulation(mondict,nbrIA)
        self.creerregions()
        self.creerbiotopes()
    
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
            players = []
            for i in self.joueurs:
                players.append(i)
            self.regions[reg[0]]=[]     # la cl� de r�gion
            for i in range(reg[1]):
                listecasereg=[]
                if players.__len__() and (k==1 or k == 4):
                    playerX = math.floor(self.joueurs.get(players[0]).x/self.taillecase)
                    playerY = math.floor(self.joueurs.get(players[0]).y/self.taillecase)
                    x=random.randrange(playerX-20, playerX+20)
                    y=random.randrange(playerY-20, playerY+20)
                    players.pop(0)
                else:
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

        for i in range(nbrIA):
            mondict.append(self.parent.generernom())

        playersToCreate = len(mondict)

        for i in mondict:
            id=getprochainid()
            coul=couleurs.pop()
            # placer les joueurs dans des quandrants differents
            choixquad=random.choice(range(nquad))
            nquad-=1
            quad=quadrants.pop(choixquad)
            
            locationOccupied = False
            x = y = 0

            n=1
            while n:
                # DEBUG SETTINGS DEBUG SETTINGS DEBUG SETTINGS DEBUG SETTINGS DEBUG SETTINGS DEBUG SETTINGS DEBUG SETTINGS DEBUG SETTINGS  DEBUG SETTINGS DEBUG SETTINGS 
                if DebugSettings.spawnPlayersNearby:
                    if locationOccupied:    
                        x += 1  # On pousse vers la droite pour trouver une case non occupés
                    else:
                        if playersToCreate == 1: 
                            x = 1000 
                            y = 1000
                        elif playersToCreate == 2:
                            x = 1500 
                            y = 1000
                        elif playersToCreate == 3:
                            x = 1000 
                            y = 1300
                        elif playersToCreate == 4:
                            x = 1500 
                            y = 1300
                else:
                    # Génère les coordonnées de spawn aléatoire, mais dans un quadrant
                    x=random.randrange(quad[0][0]+bord,quad[1][0]-bord)
                    y=random.randrange(quad[0][1]+bord,quad[1][1]-bord)

                case=self.trouvercase(x,y)
                if self.cartecase[case[1]][case[0]]==0: # Check si la case est occupé par quek chose?
                    self.joueurs[i]=Joueur(self,id,i,coul,x,y)
                    n=0
                    playersToCreate-=1
                else:
                    locationOccupied = True
            
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

        t1=[]
        for i in range(taille):
            t2=[]
            for j in range(taille):
                t2.append({"persos":[],
                           "batiments":[]})
            t1.append(t2)

        self.hashmap = t1
    
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

    def findTileInHashMap(self,x,y):
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

        return self.hashmap[cx][cy]

    def getOccupiedTilesAround(self,x,y,distance):
        # Distance d serait en case et non en pixel, faut convert je crois
        distanceCase = int (distance / self.taillecase)
        if distanceCase < 1:
            distanceCase = 0

        cx=int(x/self.taillecase) 
        cy=int(y/self.taillecase) 

        demiCase = self.taillecase / 2

        # le centre en pixels de la case d'origine
        pxcentrex=(cx*self.taillecase) + demiCase
        pxcentrey=(cy*self.taillecase) + demiCase
        
        # la case superieur gauche de la case d'origine
        casecoinx1=cx-distanceCase
        casecoiny1=cy-distanceCase

        # assure qu'on deborde pas
        if casecoinx1<0:
            casecoinx1=0
        if casecoiny1<0:
            casecoiny1=0

        # la case inferieur droite
        casecoinx2=cx+distanceCase
        casecoiny2=cy+distanceCase

        # assure qu'on deborde pas
        if casecoinx2 >= self.taillecarte:
            casecoinx2 = self.taillecarte-1
        if casecoiny2 >= self.taillecarte:
            casecoiny2 = self.taillecarte-1

        distmax = (distanceCase * self.taillecase) + demiCase

        t1=[]
        for i in range(casecoinx1,casecoinx2):
            for j in range(casecoiny1,casecoiny2): 
                case = self.hashmap[i][j]

                pxcentrecasex=(i * self.taillecase) + demiCase
                pxcentrecasey=(j * self.taillecase) + demiCase
                
                if Helper.withinDistance(pxcentrex,pxcentrey,pxcentrecasex,pxcentrecasey, distmax):
                    if case["persos"] or case["batiments"]: # Non vide
                        t1.append(case)
        return t1  
    

    def getcartebbox(self,x1,y1,x2,y2):# case d'origine en cx et cy,  pour position pixels x, y
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
        

    # C'est ici qu'on reçoit une action.
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
