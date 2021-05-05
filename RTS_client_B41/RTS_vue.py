## -*- Encoding: UTF-8 -*-

from tkinter import *
from tkinter import ttk
from helper import Helper
from RTS_divers import *
from chargeurdimages import *

class Vue():
    def __init__(self,parent,urlserveur,nomDuJoueur,testdispo):
        self.parent=parent
        self.root=Tk()
        self.root.title("Je suis "+nomDuJoueur)
        self.nomDuJoueur=nomDuJoueur
        self.cadrechaton=0
        self.textchat=""
        self.infohud={}
        # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele=None
        # variable pour suivre le trave du multiselect
        self.debutselect=[]
        self.selecteuractif=None
        # minicarte
        self.tailleminicarte=220
        # images des assets, definies dans le modue loadeurimages
        self.images=chargerimages()
        self.gifs = loadGif()
        # objet pour cumuler les manipulations du joueur pour generer une action de jeu
        self.action=Action(self)
        # cadre principal de l'application
        self.cadreapp=Frame(self.root)  
        self.cadreapp.pack(expand=1,fill=BOTH)
        self.cadreactif=None
        # un dictionnaire pour conserver les divers cadres du jeu, creer plus bas
        self.cadres={}                  
        self.creercadres(urlserveur,nomDuJoueur,testdispo)
    
    # Appeler apres l'initialisation de la partie
    def initialiseravecmodele(self):
        # on reassigne le nom final localement pour eviter
        # de toujours le requerir du parent
        self.nomDuJoueur= self.parent.nomDuJoueur
        # on ajuste la taille du canevas de jeu
        self.canevas.config(scrollregion=(0,0,self.modele.aireX,self.modele.aireY))
        self.canevasaction.delete("nom")
        self.canevasaction.create_text(100,30,text=self.nomDuJoueur,font=("arial",18,"bold"),anchor=S,tags=("nom"))
        
        # on cree les cadres affichant les items d'actions du joueur
        # cadre apparaissant si on selectionne un ouvrier
        coul=self.modele.joueurs[self.parent.nomDuJoueur].couleur
        self.cadrejeuinfo.config(bg=coul[1])
        self.creeraide()
        self.creercadreouvrier(coul[0]+"_",["maison","caserne","chickenCoop","pigPen"])
        self.creerchatter()
        # on affiche les maisons, point de depart des divers joueurs
        self.afficherdepart()
        self.root.update()
        self.centrermaison()
    
    def centrermaison(self): 
        cle=list(self.modele.joueurs[self.nomDuJoueur].batiments["maison"].keys())[0]
        x=self.modele.joueurs[self.nomDuJoueur].batiments["maison"][cle].x
        y=self.modele.joueurs[self.nomDuJoueur].batiments["maison"][cle].y
        
        x1=self.canevas.winfo_width()/2
        y1=self.canevas.winfo_height()/2
        
        pctx=(x-x1)/self.modele.aireX
        pcty=(y-y1)/self.modele.aireY
        
        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)
    
    def creercadreouvrier(self,coul,artefact):
        self.cadreouvrier=Frame(self.cadreaction)
        for i in artefact:
            btn=Button(self.cadreouvrier,text=i,image=self.images[coul+i])
            btn.bind("<Button>",self.batirartefact)
            btn.pack()    
             
###### LES CADRES ############################################################################################        
    # Appel de la création des divers cadre   
    def creercadres(self,urlserveur,nomDuJoueur,testdispo):
        self.cadres["splash"]=self.creercadresplash(urlserveur,nomDuJoueur,testdispo)
        self.cadres["lobby"]=self.creercadrelobby()
        self.cadres["jeu"]=self.creercadrejeu()
    
    # le splash (ce qui 'splash' à l'écran lors du démarrage) 
    # sera le cadre visuel initial lors du lancement de l'application
    def creercadresplash(self,urlserveur,nom,testdispo):
        self.cadresplash=Frame(self.cadreapp)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas
        self.canevassplash=Canvas(self.cadresplash,width=640,height=480,bg="wheat1")
        self.canevassplash.pack()
        
        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        # les champs et 
        self.etatdujeu=Label(text="Jeu",font=("Arial",18),borderwidth=2,relief=RIDGE)
        self.nomsplash=Entry(font=("Arial",14))
        self.urlsplash=Entry(font=("Arial",14))
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, nom)
        self.urlsplash.insert(0, urlserveur)
        # on les place sur le canevassplash
        self.canevassplash.create_window(320,100,window=self.etatdujeu,width=400,height=30)
        self.canevassplash.create_window(320,200,window=self.nomsplash,width=400,height=30)
        self.canevassplash.create_window(320,250,window=self.urlsplash,width=400,height=30)
        
        # les boutons d'actions
        self.btncreerpartie=Button(text="Creer partie",font=("Arial",12),command=self.creerpartie)
        self.btnconnecterpartie=Button(text="Connecter partie",font=("Arial",12),command=self.inscrirejoueur)
        self.btnreset=Button(text="reset partie",font=("Arial",9),command=self.resetpartie)
        # on place les boutons
        self.canevassplash.create_window(420,350,window=self.btncreerpartie,width=200,height=30)
        self.canevassplash.create_window(420,400,window=self.btnconnecterpartie,width=200,height=30)
        self.canevassplash.create_window(420,450,window=self.btnreset,width=200,height=30)
        
        ## NOTES : ceci est un exemple pour ajouter des options au cadresplash
        ## POUR CHOIX CIVILISATION, 4 OPTIONS
        # LA VARIABLE DONT LA VALEUR CHANGERA AU FIL DES CLICK
        self.valciv = StringVar(self.cadresplash, "1") 
        # LES 4 BTN RADIO
        radciv1=Radiobutton(text="Civilisation 1",variable=self.valciv,value="1")
        radciv2=Radiobutton(text="Civilisation 2",variable=self.valciv,value="2")
        radciv3=Radiobutton(text="Civilisation 3",variable=self.valciv,value="3")
        radciv4=Radiobutton(text="Civilisation 4",variable=self.valciv,value="4")
        # LE PLACEMENTS DES BTN RADIOS
        self.canevassplash.create_window(220,350,window=radciv1,width=180,height=30)
        self.canevassplash.create_window(220,380,window=radciv2,width=180,height=30)
        self.canevassplash.create_window(220,410,window=radciv3,width=180,height=30)
        self.canevassplash.create_window(220,440,window=radciv4,width=180,height=30)
        ## FIN de l'exemple des choix de civilisations
        
        # on met à jour les champs et widgets
        self.updatesplash(testdispo)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadresplash
                    
    def creercadrelobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby=Frame(self.cadreapp)
        self.canevaslobby=Canvas(self.cadrelobby,width=640,height=480,bg="lightblue")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby=Listbox(borderwidth=2,relief=GROOVE)
        # et un widget pour inscrire le nombre d'IA à créer - EN ATTENTE DE L'IA ACTUELLEMENT INCOMPLÈTE
        self.labnbrIA=Label(text="IAs",font=("Arial",18),bg="lightblue")
        self.champnbrIA=Entry(width=16)
        self.champnbrIA.insert(END,0)
        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie=Button(text="Lancer partie",state=DISABLED,command=self.lancerpartie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440,240,window=self.listelobby,width=200,height=400)
        self.canevaslobby.create_window(170,300,window=self.labnbrIA,width=50,height=30)
        self.canevaslobby.create_window(230,300,window=self.champnbrIA,width=50,height=30)
        self.canevaslobby.create_window(200,400,window=self.btnlancerpartie,width=100,height=30) 
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres  
        return self.cadrelobby
    
    def creercadrejeu(self):
        # le cadre principal du jeu, remplace le Lobby
        self.cadrepartie=Frame(self.cadreapp,bg="green",width=400,height=400)
        # cadre du jeu et ses scrollbars
        self.creerairedejeu()
        # cadre pour info sur les ressources du joueur en haut de l'aire de jeu
        self.creerHUD()
        # cadre pour commandes et infos des objets de jeu, situe a droite
        self.creercadrejeuaction()
        # configuration de la section qui s'etire lorsque la fenetre change de taille
        self.cadrepartie.rowconfigure(0, weight=1)
        self.cadrepartie.columnconfigure( 0, weight=1)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrepartie
        
    def creerairedejeu(self):
        # definition du cadre avec le canvas de jeu et les scrollbars
        self.cadrecanevas=Frame(self.cadrepartie)
        # on crée les scrollbar AVANT le canevas de jeu car le canevas est dépendant de leur 
        self.scrollV=Scrollbar(self.cadrecanevas,orient=VERTICAL)
        self.scrollH=Scrollbar(self.cadrecanevas,orient=HORIZONTAL)
        self.canevas=Canvas(self.cadrecanevas,width=500,height=400,bg="DarkOliveGreen2",
                            yscrollcommand = self.scrollV.set,
                            xscrollcommand = self.scrollH.set )
        self.scrollV.config( command = self.canevas.yview)
        self.scrollH.config( command = self.canevas.xview)
        # on visualise utilisant grid (grille) 
        # le grid avec 'sticky' indique que l'objet doit s'acroitre pour coller aux 'points cardinaux' (anglais)
        
        self.canevas.grid(row=1,column=0,sticky=N+S+E+W)
        self.scrollV.grid(row=1,column=1,sticky=N+S)
        self.scrollH.grid(row=2,column=0,sticky=E+W)
        
        # visualise le cadre qui contient le canevas de jeu
        self.cadrecanevas.grid(column=0,row=0,sticky=N+S+E+W)
        # on doit preciser quelle partie de la grille (grid) va s'accroitre, colonne et rangée
        # ici on precise que c'est le canevas et non les scrollbar qui doit s'agrandir
        self.cadrecanevas.rowconfigure(1, weight=1)
        self.cadrecanevas.columnconfigure( 0, weight=1)
        self.connecterevent()
    
    def creerHUD(self):
        self.cadrejeuinfo=Frame(self.cadrecanevas,bg="blue")
        #des etiquettes d'info
        self.infohud={"Nourriture":None,
                      "Bois":None,
                      "Roche":None,
                      "Aureus":None}
        # fonction interne uniquement pour reproduire chaque item d'info
        def creerchampinterne(listechamp):
            titre=Champ(self.cadrejeuinfo, text=i,bg="red",fg="white")
            varstr=StringVar()
            varstr.set(0)
            donnee=Champ(self.cadrejeuinfo,bg="red",fg="white", textvariable=varstr)
            titre.pack(side=LEFT)
            donnee.pack(side=LEFT)
            self.infohud[i]=[varstr,donnee]
            
        for i in self.infohud.keys():
            creerchampinterne(i)
        
        self.btnchat=Button(self.cadrejeuinfo,text="Chat",command=self.action.chatter)
        self.btnaide=Button(self.cadrejeuinfo,text="Aide",command=self.action.aider)
        
        self.btnaide.pack(side=RIGHT)
        self.btnchat.pack(side=RIGHT)
        self.cadrejeuinfo.grid(row=0,column=0,sticky=E+W,columnspan=2)  
            
    def creercadrejeuaction(self):
        # Ajout du cadre d'action a droite pour identifier les objets permettant les commandes du joueur 
        self.cadreaction=Frame(self.cadrepartie)
        self.cadreaction.grid(row=0,column=1,sticky=N+S)
        self.scrollVaction=Scrollbar(self.cadreaction,orient=VERTICAL)
        self.canevasaction=Canvas(self.cadreaction,width=200,height=300,bg="lightblue",
                            yscrollcommand = self.scrollVaction.set)
        
        self.scrollVaction.config( command = self.canevasaction.yview)
        self.canevasaction.grid(row=0,column=0,sticky=N+S)
        self.scrollVaction.grid(row=0,column=1,sticky=N+S)
        # les widgets 
        self.canevasaction.create_text(100,30,text=self.parent.nomDuJoueur,font=("arial",18,"bold"),anchor=S,tags=("nom"))
        
        
        # minicarte
        self.minicarte=Canvas(self.cadreaction,width=self.tailleminicarte,height=self.tailleminicarte,bg="tan1",highlightthickness=0)
        self.minicarte.grid(row=2,column=0,columnspan=2)
        self.minicarte.bind("<Button-1>",self.deplacercarte)
        
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres  
        self.canevasaction.rowconfigure(0, weight=1)
        self.cadreaction.rowconfigure(0, weight=1)
    
    def creeraide(self):
        self.cadreaide=Frame(self.canevas)
        self.scrollVaide=Scrollbar(self.cadreaide,orient=VERTICAL)
        self.textaide=Text(self.cadreaide,width=50,height=10,
                            yscrollcommand = self.scrollVaide.set )
        self.scrollVaide.config(command = self.textaide.yview)
        self.textaide.pack(side=LEFT)
        self.scrollVaide.pack(side=LEFT,expand=1, fill=Y)
        fichieraide=open("aide.txt")
        monaide=fichieraide.read()
        fichieraide.close()
        self.textaide.insert(END, monaide)
        self.textaide.config(state=DISABLED)
    
    def creerchatter(self):
        self.cadrechat=Frame(self.canevas,bd=2,bg="orange")
        self.cadrechatlist=Frame(self.cadrechat)
        # Make topLevelWindow remain on top until destroyed, or attribute changes.
        self.scrollVchat=Scrollbar(self.cadrechatlist,orient=VERTICAL)
        self.textchat=Listbox(self.cadrechatlist,width=30,height=6,
                            yscrollcommand = self.scrollVchat.set )
        self.scrollVchat.config(command = self.textchat.yview)
        self.textchat.pack(side=LEFT)
        self.scrollVchat.pack(side=LEFT,expand=1, fill=Y)
        self.textchat.delete(0, END)
        self.cadrechatlist.pack()
        # inscrire texte et choisir destinataire
        self.cadreparler=Frame(self.cadrechat,bd=2)
        self.joueurs=ttk.Combobox(self.cadreparler,
                                  values=list(self.modele.joueurs.keys()))
        self.entreechat=Entry(self.cadreparler,width=20)
        self.entreechat.bind("<Return>",self.action.envoyerchat)
        self.joueurs.pack(expand=1,fill=X)
        self.entreechat.pack(expand=1,fill=X)
        self.cadreparler.pack(expand=1,fill=X)
                
    def connecterevent(self):
        # on attache (bind) desF événements soit aux objets eux même
        self.canevas.bind("<Button-1>",self.annuleraction)
        self.canevas.bind("<Button-2>",self.construirebatiment)
        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>",self.selectdebuter)
        self.canevas.bind("<Shift-B1-Motion>",self.selectafficher)
        self.canevas.bind("<Shift-ButtonRelease-1>",self.selectfinir)
        
        self.canevas.bind("<Button-3>",self.indiquerposition)
        # soit aux dessins, en vertu de leur tag (propriétés des objets dessinés)
        # ALL va réagir à n'importe quel dessin
        # sinon on spécifie un tag particulier, exemple avec divers tag, attaché par divers événements
        self.canevas.tag_bind("batiment","<Button-1>",self.creerentite)
        self.canevas.tag_bind("perso","<Button-1>",self.ajoutselection)

        self.canevas.tag_bind("perso","<Button-3>",self.setAttackTarget)
        self.canevas.tag_bind("batiment","<Button-3>",self.setAttackTarget)

        self.canevas.tag_bind("arbre","<Button-3>",self.ramasserressource)
        self.canevas.tag_bind("aureus","<Button-3>",self.ramasserressource)
        self.canevas.tag_bind("roche","<Button-3>",self.ramasserressource)
        self.canevas.tag_bind("baie","<Button-3>",self.ramasserressource)
        self.canevas.tag_bind("daim","<Button-3>",self.chasserressource)
    
    # cette méthode sert à changer le cadre (Frame) actif de la fenêtre, on n'a qu'à fournir le cadre requis
    def changercadre(self,nomcadre):
        cadre=self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack(expand=1,fill=BOTH)
        
##### FIN DES CADRES##########################################################################################################        
    
    def annuleraction(self,evt):
        mestags=self.canevas.gettags(CURRENT)
        if not mestags:
            self.canevasaction.delete(self.action.widgetsactifs)
            if self.action.btnactif:
                self.action.btnactif.config(bg="SystemButtonFace")
            self.action=Action(self)

    
    def fermechat(self):
        self.textchat=None 
        self.fenchat.destroy()
        
    def ajoutselection(self,evt):
        mestags=self.canevas.gettags(CURRENT)
        if self.parent.nomDuJoueur in mestags:
            if "perso" in mestags:
                self.action.persochoisi.append(mestags[1])
                self.action.affichercommandeperso()    
                  
    # Methodes pour multiselect    
    def selectdebuter(self,evt):
        self.debutselect=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
        x1,y1=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
        self.selecteuractif=self.canevas.create_rectangle(x1,y1,x1+1,y1+1,outline="red",width=2,
                                                          dash=(2,2),tags=("","selecteur","","artefact"))
        
        
    def selectafficher(self,evt):
        if self.debutselect:
            x1,y1=self.debutselect
            x2,y2=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
            self.canevas.coords(self.selecteuractif,x1,y1,x2,y2)
            
    def selectfinir(self,evt):
        if self.debutselect:
            x1,y1=self.debutselect
            x2,y2=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
            self.debutselect=[]
            objchoisi=(list(self.canevas.find_enclosed(x1,y1,x2,y2)))
            for i in objchoisi:
                if self.parent.nomDuJoueur not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.action.persochoisi.append(self.canevas.gettags(i)[1])
                    
            if self.action.persochoisi:
                self.action.affichercommandeperso()   
            self.canevas.delete("selecteur")
    ### FIN du multiselect
                
    def ramasserressource(self,evt):
        tag=self.canevas.gettags(CURRENT)
        if tag[0]=="" and self.action.persochoisi:
            self.action.ramasserressource(tag)
        else:
            print(tag[3])
    
    def chasserressource(self,evt):
        tag=self.canevas.gettags(CURRENT)
        if tag[0]=="" and self.action.persochoisi and tag[3]=="daim":
            self.action.chasserressource(tag)
        else:
            print(tag[3])
                                    
    def indiquerposition(self,evt):
        tag=self.canevas.gettags(CURRENT)
        if not tag:
            x,y=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
            self.action.position=[x,y]
            self.action.deplacer()

    def setAttackTarget(self,evt):
        tag=self.canevas.gettags(CURRENT)

        if not tag:
            print(tag[3])
        else:
            if self.nomDuJoueur != tag[0]:  # Si Ennemie
                self.action.setAttackTarget(tag)
            
    # Cette fonction permet se se deplacer via un click sur la minicarte
    def deplacercarte(self,evt):
        x=evt.x
        y=evt.y
        
        pctx=x/self.tailleminicarte
        pcty=y/self.tailleminicarte 
        
        xl=(self.canevas.winfo_width()/2)/self.modele.aireX
        yl=(self.canevas.winfo_height()/2)/self.modele.aireY
        
        self.canevas.xview_moveto(pctx-xl)
        self.canevas.yview_moveto(pcty-yl)
        xl=self.canevas.winfo_width()
        yl=self.canevas.winfo_height()
        
    def batirartefact(self,evt):
        obj=evt.widget
        if self.action.btnactif:
            if self.action.btnactif != obj:
                self.action.btnactif.config(bg="SystemButtonFace")
                
        self.action.btnactif=obj
        self.action.prochaineaction=obj.cget("text")
        obj.config(bg="lightgreen")
        
    def construirebatiment(self,evt):
        mestags=self.canevas.gettags(CURRENT)
        if not mestags:
            pos=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
            self.action.construirebatiment(pos)
              
    def creerentite(self,evt):
        x,y=evt.x,evt.y
        mestags=self.canevas.gettags(CURRENT)
        if self.parent.nomDuJoueur in mestags and "batiment" in mestags:
            if "maison" in mestags:
                pos=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
                action=[self.parent.nomDuJoueur,"creerperso",["ouvrier",mestags[4],mestags[1],pos]]
            if "caserne" in mestags:
                pos=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
                action=[self.parent.nomDuJoueur,"creerperso",["soldat",mestags[4],mestags[1],pos]]
            if "chickenCoop" in mestags:
                pos=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
                action=[self.parent.nomDuJoueur,"creerperso",["chicken",mestags[4],mestags[1],pos]]
            if "pigPen" in mestags:
                pos=(self.canevas.canvasx(evt.x),self.canevas.canvasy(evt.y))
                action=[self.parent.nomDuJoueur,"creerperso",["pig",mestags[4],mestags[1],pos]]
                
            self.parent.actionsrequises=action
           
    ##FONCTIONS D'AFFICHAGES##################################        
    def afficherdepart(self):
        self.modele.listebiotopes.sort(key = lambda c: c.y)
        for i in self.modele.listebiotopes:
            monitem=self.canevas.create_image(i.x,i.y,image=self.images[i.img],anchor=S,
                                              tags=("",i.id,"bio",i.montype))
        
        minitaillecase=int(self.tailleminicarte/self.modele.taillecarte)
        couleurs={0:"",
                  1:"light green",
                  2:"light blue",
                  3:"tan",
                  4:"gray30",
                  5:"orange"}
        for i,t in enumerate(self.modele.regions):
            if t!="plaine":
                for j,c in enumerate(self.modele.regions[t]):
                    for k in c:
                        y1=k[1]*minitaillecase
                        y2=y1+minitaillecase
                        x1=k[0]*minitaillecase
                        x2=x1+minitaillecase
                        self.minicarte.create_rectangle(x1,y1,x2,y2,outline="",
                                                        fill=couleurs[self.modele.cartecase[k[1]][k[0]]])
        
        # Affichage des batiments intiaux sur l'aire de jeu et sur la minicarte      
        px=int(self.tailleminicarte/self.modele.aireX)
        py=int(self.tailleminicarte/self.modele.aireY)
        
        for j in self.modele.joueurs.keys():
            for i in self.modele.joueurs[j].batiments["maison"].keys():
                m=self.modele.joueurs[j].batiments["maison"][i]
                coul=self.modele.joueurs[j].couleur[0]
                self.canevas.create_image(m.x,m.y,image=self.images[coul+"_maison"],
                                          tags=(j,m.id,"artefact","batiment","maison")) 
                # afficher sur minicarte
                coul=self.modele.joueurs[j].couleur[1]
                x1=int((m.x/self.modele.aireX)*self.tailleminicarte)
                y1=int((m.y/self.modele.aireY)*self.tailleminicarte)
                self.minicarte.create_rectangle(x1-2,y1-2,x1+2,y1+2,fill=coul,tags=(j,m.id,"artefact","maison"))
    
    def afficherbio(self,bio):
        self.canevas.create_image(bio.x,bio.y,image=self.images[bio.img],
                                    tags=("",bio.id,"bio",bio.montype))        
            
    def afficherbatiment(self,joueur,batiment):
        coul=self.modele.joueurs[joueur].couleur[0]
        self.canevas.create_image(batiment.x,batiment.y,image=self.images[batiment.image],
                                    tags=(self.parent.nomDuJoueur,batiment.id,"artefact","batiment",batiment.montype))        
        couleurs={0:"",
                  1:"light green",
                  2:"light blue",
                  3:"tan",
                  4:"gray30",
                  5:"orange"}
        coul=self.modele.joueurs[joueur].couleur[1]
        x1=int((batiment.x/self.modele.aireX)*self.tailleminicarte)
        y1=int((batiment.y/self.modele.aireY)*self.tailleminicarte)
        self.minicarte.create_rectangle(x1-2,y1-2,x1+2,y1+2,fill=coul,tags=(self.parent.nomDuJoueur,batiment.id,"artefact",batiment.montype))
    
    def afficherjeu(self):
        # On efface tout ce qui est 'mobile' (un tag)
        self.canevas.delete("mobile")
        
        # on se debarrasse des choses mortes (disparues), le id est dans le tag du dessin
        for i in self.modele.ressourcemorte:
            self.canevas.delete(i.id)
            
        # commencer par les choses des joueurs             
        for j in self.modele.joueurs.keys():
            # ajuster les infos du HUD 
            if j==self.parent.nomDuJoueur:
                self.infohud["Nourriture"][0].set(self.modele.joueurs[j].ressources["nourriture"])
                self.infohud["Bois"][0].set(self.modele.joueurs[j].ressources["arbre"])
                self.infohud["Roche"][0].set(self.modele.joueurs[j].ressources["roche"])
                self.infohud["Aureus"][0].set(self.modele.joueurs[j].ressources["aureus"])
        
            # ajuster les persos de chaque joueur et leur dépendance (ici javelots des ouvriers)
            for p in self.modele.joueurs[j].persos.keys():    
                for k in self.modele.joueurs[j].persos[p].keys():
                    i=self.modele.joueurs[j].persos[p][k]
                    coul=self.modele.joueurs[j].couleur[0]
                    self.canevas.create_image(i.x,i.y,anchor=S,image=self.images[i.image],
                                              tags=(j,k,"artefact","mobile","perso",p))
                    
                    # Ceci est l'endroit ou l'affichage des healthbar à lieu
                    if k in self.action.persochoisi:
                        self.canevas.create_rectangle(i.x-10,i.y+5,i.x+10,i.y+10,fill="black",tags=(j,k,"artefact","mobile","persochoisi"))
                        self.canevas.create_rectangle(i.x-10,i.y+5,i.x + (i.health / i.maxHealth) * 20 - 10, i.y + 10  ,fill="green",tags=(j,k,"artefact","mobile","persochoisi"))
                    else:
                        self.canevas.create_rectangle(i.x-10,i.y+5,i.x + 10,i.y+10,fill="black",tags=(j,k,"artefact","mobile","persochoisi"))
                        self.canevas.create_rectangle(i.x-10,i.y+5,i.x + (i.health / i.maxHealth) * 20 - 10, i.y + 10 ,fill="yellow",tags=(j,k,"artefact","mobile","persochoisi"))
                        
                    # dessiner javelot de l'ouvrier
                    if p=="ouvrier":
                        for b in self.modele.joueurs[j].persos[p][k].javelots:
                            self.canevas.create_image(b.x,b.y,image=self.images[b.image],tags=(j,b.id,"artefact","mobile","javelot"))

            # Barre de vie des bâtiments                            
            for k in self.modele.joueurs[j].batiments.keys():    
                for l in self.modele.joueurs[j].batiments[k].keys():
                    i = self.modele.joueurs[j].batiments[k][l]
                    if i in self.action.persochoisi:
                        self.canevas.create_rectangle(i.x-10,i.y+25,i.x+10,i.y+30,fill="black",tags=(j,k,"artefact","mobile"))
                        self.canevas.create_rectangle(i.x-10,i.y+25,i.x + (i.health / i.maxHealth) * 20 - 10, i.y +30  ,fill="green",tags=(j,k,"artefact","mobile"))
                    else:
                        self.canevas.create_rectangle(i.x-10,i.y+25,i.x+10,i.y + 30,fill="black",tags=(j,k,"artefact","mobile"))
                        self.canevas.create_rectangle(i.x-10,i.y+25,i.x + (i.health / i.maxHealth) * 20 - 10, i.y +30 ,fill="yellow",tags=(j,k,"artefact","mobile"))

        # ajuster les choses vivantes dependantes de la partie (mais pas des joueurs) 
        for j in self.modele.biotopes["daim"].keys():
            i=self.modele.biotopes["daim"][j]
            if i.etat=="mort":
                self.canevas.create_image(i.x,i.y,image=self.images["daimMORT"],tags=("",i.id,"artefact","daim","mobile"))

            else:
                nomimg="daim"+i.dir
                self.canevas.create_image(i.x,i.y,image=self.images[nomimg],tags=("",i.id,"artefact","daim","mobile"))
        
        for j in self.modele.biotopes["eau"].keys():
            i = self.modele.biotopes["eau"][j]
            if i.sprite:
                self.canevas.create_image(i.x,i.y,image = self.gifs[i.sprite][i.spriteNum], tags=("",i.id,"artefact","poissons","mobile"))
                i.nextSprite()


        # mettre les chat a jour si de nouveaux messages sont arrives
        if self.textchat and self.modele.joueurs[self.parent.nomDuJoueur].chatneuf:
            self.textchat.delete(0, END)
            self.textchat.insert(END, *self.modele.joueurs[self.parent.nomDuJoueur].monchat)
            if self.modele.joueurs[self.parent.nomDuJoueur].chatneuf and self.action.chaton==0:
                self.btnchat.config(bg="orange")
            self.modele.joueurs[self.parent.nomDuJoueur].chatneuf=0
                
    ###  METHODES POUR SPLASH ET LOBBY INSCRIPTION pour participer a une partie
    def updatesplash(self,etat):
        if etat=="attente" or etat=="courante":
            self.btncreerpartie.config(state=DISABLED)
        if etat=="courante":
            self.etatdujeu.config(text="Desole - partie encours !")
            self.btnconnecterpartie.config(state=DISABLED)
        elif etat=="attente":
            self.etatdujeu.config(text="Partie en attente de joueurs !")
            self.btnconnecterpartie.config(state=NORMAL)
        else:
            self.etatdujeu.config(text="Bienvenue ! Serveur disponible")
            self.btnconnecterpartie.config(state=DISABLED)
            self.btncreerpartie.config(state=NORMAL)

    def updatelobby(self,dico):
        self.listelobby.delete(0,END)
        for i in dico:
            self.listelobby.insert(END,i[0])
        if self.parent.egoserveur:
            self.btnlancerpartie.config(state=NORMAL)
               
    def creerpartie(self):
        nom=self.nomsplash.get()
        ## ON VA LIRE LA VALEUR DE LA VARIABLE ASSOCIEE AU BTN RADION CHOISI
        valciv=self.valciv.get()
        urljeu=self.urlsplash.get()
        self.parent.creerpartie(nom,urljeu,valciv)
        
    def inscrirejoueur(self):
        nom=self.nomsplash.get()
        ## ON VA LIRE LA VALEUR DE LA VARIABLE ASSOCIEE AU BTN RADION CHOISI
        valciv=self.valciv.get()
        urljeu=self.urlsplash.get()
        self.parent.inscrirejoueur(nom,urljeu,valciv)
        
    def lancerpartie(self):
        nbrIA=self.champnbrIA.get()
        self.parent.lancerpartie(nbrIA)
        
    def resetpartie(self):
        rep=self.parent.resetpartie()
    ### FIN des methodes pour lancer la partie
    
    
# Singleton (mais pas automatique) sert a conserver les manipulations du joueur pour demander une action
class Action():
    def __init__(self,parent):
        self.parent=parent
        self.persochoisi=[]
        self.position=[]
        self.btnactif=None
        self.prochaineaction=None
        self.widgetsactifs=[]
        self.chaton=0 
        self.aideon=0 
           

    # C'est ici qu'on liste tout les actions possibles?
    def deplacer(self):
        if self.persochoisi:
            action=[self.parent.parent.nomDuJoueur,"deplacer",[self.position,self.persochoisi]]
            self.parent.parent.actionsrequises=action

    def setAttackTarget(self,tag):
        # Pour target, voici les tags nécessaires:
        # targetId, isPerso, targetType, enemyPlayerName, self.persochoisi 

        if self.persochoisi:
            action=[self.parent.parent.nomDuJoueur,"setAttackTarget",[tag[1],tag[4], tag[5], tag[0], self.persochoisi]]
            self.parent.parent.actionsrequises=action
    
    def chasserressource(self,tag):
        if self.persochoisi:
            action=[self.parent.parent.nomDuJoueur,"chasserressource",[tag[3],tag[1],self.persochoisi]]
            self.parent.parent.actionsrequises=action
            
    def ramasserressource(self,tag):
        if self.persochoisi:
            action=[self.parent.parent.nomDuJoueur,"ramasserressource",[tag[3],tag[1],self.persochoisi]]
            self.parent.parent.actionsrequises=action
            
    def construirebatiment(self,pos):
        self.btnactif.config(bg="SystemButtonFace")
        self.btnactif=None
        action=[self.parent.nomDuJoueur,"construirebatiment",[self.prochaineaction,pos]]
        self.parent.parent.actionsrequises=action            
                
    def affichercommandeperso(self):
        self.widgetsactifs=self.parent.canevasaction.create_window(100,180,
                                                window=self.parent.cadreouvrier,
                                                anchor=CENTER)
    
    def envoyerchat(self,evt):
        txt=self.parent.entreechat.get()
        joueur=self.parent.joueurs.get()
        if joueur:
            action=[self.parent.nomDuJoueur,"chatter",[self.parent.nomDuJoueur+": "+txt,self.parent.nomDuJoueur,joueur]]
            self.parent.parent.actionsrequises=action
    
    def chatter(self):
        if self.chaton==0:
            x1,x2=self.parent.scrollH.get()
            x3=self.parent.modele.aireX*x1
            y1,y2=self.parent.scrollV.get()
            y3=self.parent.modele.aireY*y1
            self.parent.cadrechaton=self.parent.canevas.create_window(x3,y3,
                                                window=self.parent.cadrechat,
                                                anchor=N+W)
            self.parent.btnchat.config(bg="SystemButtonFace")
            self.chaton=1
        else:
            self.parent.canevas.delete(self.parent.cadrechaton)
            self.parent.cadrechaton=0
            self.chaton=0
            
    def aider(self):
        if self.aideon==0:
            x1,x2=self.parent.scrollH.get()
            x3=self.parent.modele.aireX*x2
            y1,y2=self.parent.scrollV.get()
            y3=self.parent.modele.aireY*y1
            self.aideon=self.parent.canevas.create_window(x3,y3,
                                                window=self.parent.cadreaide,
                                                anchor=N+E)
        else:
            self.parent.canevas.delete(self.aideon)
            self.aideon=0
            
        
class Champ(Label):
    def __init__(self,master,*args, **kwargs):
        Label.__init__(self,master,*args, **kwargs)
        self.config(font=("arial",13,"bold"))
        self.config(bg="goldenrod3")

