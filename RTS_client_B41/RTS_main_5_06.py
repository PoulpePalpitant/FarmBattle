## -*- Encoding: UTF-8 -*-

import urllib.request
import urllib.parse 
import json 
import random
from helper import Helper
from RTS_divers import *
from RTS_vue import *
from RTS_modele import *
from RTS_upgrades import *

"""
Application client RTS, base sur le modele approximatif d'Age of Empire I

module principal (main), essentiellement le controleur, dans l'architecture M-V-C
"""

class Controleur():
    def __init__(self):
        # indique si on 'cree' la partie, c'est alors nous qui pourront Demarre la pertie
        self.egoserveur=0 
        # le no de cadre pour assurer la syncronisation avec les autres participants
        # cette variable est gerer par la boucle de jeu (bouclersurjeu)
        self.cadrejeu=0    
        # la liste de mes actions a envoyer au serveur, rempli par les actions du joueur AFFECTANT le jeu                 
        self.actionsrequises=[] 
        
        # cette variable INDENTIFIE les joueurs dans le jeu IMPORTANT            
        # createur automatique d'un nom de joueur, pour faciliter les tests (pas besoin d'inscrire un chaque fois)
        # NOTE la fonction ne garantie pas l'unicite des noms - probleme en cas de conflit - non traite pour l'instant
        self.nomDuJoueur=self.generernom()     
        # la variable donnant acces au jeu pour le controleur, cree lorsque la partie est initialise (initialiserpartie)
        self.modele=None
        # liste des noms de joueurs pour le lobby
        self.joueurs=[]
        
        # requis pour sortir de cette boucle et passer au lobby du jeu
        self.prochainsplash=None    
                
        # delai en ms de la boucle de jeu
        self.maindelai=100 
        # frequence des appel au serveur, evite de passer son temps a communiquer avec le serveur
        self.moduloappelserveur=5  
        
        # adresses du URL du serveur de jeu, adresse 127.0.0.1 est pour des tests avec un serveur local... utile pour tester
        #self.urlserveur = "http://dodo1bododo.pythonanywhere.com"
        self.urlserveur = "http://127.0.0.1:5000"
        
        # test la connexion au serveur et retourne son etat pour l'afficher dans le splash
        testdispo=self.testetatserveur()
        # creation de la l'objet vue pour l'affichage et les controles du jeu
        self.vue=Vue(self,self.urlserveur,self.nomDuJoueur,testdispo[0])
        # requiert l'affichage initiale du splash screen (fenetre initiale de l'application)
        self.vue.changercadre("splash") 
        # lancement de la communication avec les serveur
        self.bouclersplash()
        # demarrage de la boucle evenementielle du logiciel
        # cette boucle gere les evenements (souris, click, clavier)
        self.vue.root.mainloop()
        
    # methode speciale pour remettre les parametres du serveur a leurs valeurs par defaut (jeu disponible, pas de joueur)
    # indique le resultat dans le splash
    def resetpartie(self):
        leurl=self.urlserveur+"/resetjeu"
        r=urllib.request.urlopen(leurl)
        rep=r.read()
        self.vue.updatesplash("Dispo")
        return rep.decode('utf-8')
        
    # methode pour connaitre l'etat du serveur au lancement de l'application seulement
    # dispo=on peur creer une partie
    # attente=on peut se connecter a la partie
    # courante= la partie est en cours, on ne peut plus se connecter
    def testetatserveur(self):
        leurl=self.urlserveur+"/testjeu"
        r=urllib.request.urlopen(leurl)
        rep=r.read()
        repdecode=rep.decode('utf-8')
        if "dispo" in repdecode:
            return ["dispo",repdecode]
        elif "attente" in repdecode:
            return ["attente",repdecode]
        elif "courante" in repdecode:
            return ["courante",repdecode]
        else:
            return "impossible"
    
    # a partir du splash, permet de creer une partie (lance le lobby pour permettre a d'autres joueurs de se connecter)
    # l'argument valciv n'est pas utilise pour l'INSTANT, elle sert de recette pour envoyer d
    # es parameters lors de la demande de creation d'une partie
    # on pourrait ainsi deja fournir des options de jeu
    def creerpartie(self,nom,urljeu,valciv):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash=None
        if nom:
            self.nomDuJoueur=nom
        url = self.urlserveur+"/creerpartie"
        params = {"nom": self.nomDuJoueur,
                  "valoptions":[valciv]}
        reptext=self.appelserveur(url,params)
        mondict=reptext.decode('utf-8')
        maliste=ast.literal_eval(mondict)
        maciv=ast.literal_eval(mondict)
        macivint=ast.literal_eval(maciv[1])
        self.egoserveur=1
        self.vue.root.title("je suis "+self.nomDuJoueur)
        self.vue.changercadre("lobby")
        self.bouclersurlobby()
            
    # permettre a un joueur de s'inscrire a une partie creer (mais non lancer...)
    # transporter alors dans le lobby, en attente du lancement de la partie
    # le joueur peut aussi choisir une option 
    def inscrirejoueur(self,nom,urljeu,valciv):
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash=None
        if nom:
            self.nomDuJoueur=nom
        url = self.urlserveur+"/inscrirejoueur"
        params = {"nom": self.nomDuJoueur,
                  "valoptions":[valciv] }
        reptext=self.appelserveur(url,params)
        
        mondict=json.loads(reptext)
        self.vue.root.title("je suis "+self.nomDuJoueur)
        self.vue.changercadre("lobby")
        self.bouclersurlobby()
    
    # e partir du lobby, le createur de la partie peut lancer la partie
    # fournissant des options (ici nbrIA) uniquement accessible au createur
    # lors que le createur voit tous ses joueurs esperes insrit il peut (seul d'ailleurs) lancer la partie
    # cette methode ne fait que changer l'etat de la partie sur le serveur pour le mettre a courant
    # lorsque chaque joueur recevra cet etat la partie sera initialiser et demarrer localement pour chacun
    def lancerpartie(self,nbrIA = 0):
        
        if DebugSettings.generateAi:    # debug settings debug settingsdebug settingsdebug settingsdebug settingsdebug settingsdebug settingsdebug settingsdebug settings
            nbrIA = 3

        ## au lancement le champ 'champnbtIA' du lobby est lu...
        url = self.urlserveur+"/lancerpartie"
        params = {"nom": self.nomDuJoueur,
                  "nbrIA":nbrIA}
        reptext=self.appelserveur(url,params)
        
    # methode de demarrage local de la boucle de jeu (partie demarre ainsi)
    def initialiserpartie(self,mondict):
        # on recoit les divers parametres d'initialisation du serveur
        initaleatoire=mondict[1][0][0]
        #ment, decommenter un ligne et commenter l'autre
        # mais pour tester c'est bien de toujous avoir les memes suite de random
        # random ALEATOIRE fourni par le serveur
        random.seed(int(initaleatoire))
        # random FIXE pour test
        #random.seed(124993)
        
        # on recoit la derniere liste des joueurs pour la partie
        listejoueurs=[]
        for i in self.joueurs:
            listejoueurs.append(i[0])
        
        # le  nombre d'IA desires est envoye au modele
        nbrIA=mondict[2][0][0]
        # on cree le modele (la partie)
        self.modele=Partie(self,listejoueurs,nbrIA)
        
        # on passe le modele a la vue puisqu'elle trouvera toutes le sinfos a dessiner
        self.vue.modele=self.modele
        # on met la vue a jour avec les infos de partie
        
        #self.vue.initialiseravecmodele()
        # on change le cadre la fenetre pour passer dans l'interface de jeu
        self.vue.changercadre("jeu")
        
        self.vue.initialiseravecmodele()
        # on lance la boucle de jeu
        self.bouclersurjeu()    
          
    # boucle de comunication intiale avec le serveur pour creer ou s'inscrire a la partie
    def bouclersplash(self):
        url = self.urlserveur+"/testjeu"
        params = {"nom": self.nomDuJoueur }
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        if "attente" in mondict[0]:
            self.vue.updatesplash(mondict[0][0])
        self.prochainsplash=self.vue.root.after(500,self.bouclersplash)
    
    # on boucle sur le lobby en attendant l'inscription de tous les joueurs attendus
    def bouclersurlobby(self):
        url = self.urlserveur+"/lobbyjoueur"
        params = {"nom": self.nomDuJoueur }
        reptext=self.appelserveur(url,params)
        mondict=json.loads(reptext)
        # si l'etat est courant, c'est que la partie vient d'etre lancer
        if "courante" in mondict[0]:
            self.initialiserpartie(mondict)
        else:
            self.joueurs=mondict
            self.vue.updatelobby(mondict)
            self.vue.root.after(500,self.bouclersurlobby)
         
    def bouclersurjeu(self):
        # increment du compteur de boucle de jeu
        self.cadrejeu+=1
        # test pour communiquer avec le serveur periodiquement
        if self.cadrejeu%self.moduloappelserveur==0:
            if self.actionsrequises:
                actions=self.actionsrequises
            else:
                actions=None
            self.actionsrequises=[]
            
            url = self.urlserveur+"/bouclersurjeu"
            params = {"nom": self.nomDuJoueur,
                      "cadrejeu":self.cadrejeu,
                      "actionsrequises":actions}
            
            reptext=self.appelserveur(url,params)
            mondict=json.loads(reptext)
            self.modele.ajouteractionsafaire(mondict)
        
        # encoyer les messages au modele et a la vue de faire leur job
        self.modele.jouerprochaincoup(self.cadrejeu)
        self.vue.afficherjeu()
        # appel ulterieur de la meme fonction jusqu'a l'arret de la partie
        self.vue.root.after(self.maindelai,self.bouclersurjeu)
    
    # generateur de nouveau nom, 
    # peut generer UN NOM EXISTANT mais c'est rare, NON GERER PAR LE SERVEUR        
    
    def generernom(self): 
        nomDuJoueur="JAJA_"+str(random.randrange(100,1000))
        return nomDuJoueur
    
    # fonction d'appel normalisee, utiliser par les methodes du controleur qui communiquent avec le serveur
    def appelserveur(self,url,params):
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        url = url + "?" + query_string 
        rep=urllib.request.urlopen( url , data, timeout=20) # pour probleme de connection A SUIVRE
        reptext=rep.read()
        return reptext
    
    ###############################################################################
    ### Placez vos fonctions 
    def afficherbatiment(self,nom,batiment):
        self.vue.afficherbatiment(nom,batiment)
        
    def afficherbio(self,bio):
        self.vue.afficherbio(bio)

if __name__ == '__main__':
    c=Controleur()
    #print("FIN DE PROGRAMME")
