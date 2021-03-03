
# CORRECTION REQUISE : cette classe doit etre comlpetemnent revue 
# La classe IA herite des attributs et methodes mais redefinit les methodes... 
class IA(Joueur):
    def __init__(self,parent,nom,id, x,y):
        Joueur.__init__(self,parent,nom,id,x,y)
        self.delaiaction=20
        self.actions={"creerouvrier":self.creerouvrier,
                      "ouvrierciblermaison":self.ouvrierciblermaison,
                      "colorierouvrier":self.colorierouvrier,
                      "ciblerbalise":self.ciblerbalise}
        
    def colorierouvrier(self):
        if self.ouvriers.keys():
            idouvrier=random.choice(list(self.ouvriers.keys()))
            h=self.ouvriers[idouvrier]
            h.couleur=h.maison.couleur
        
    def ouvrierciblermaison(self):
        if self.ouvriers:
            idouvrier=random.choice(list(self.ouvriers.keys()))
            self.ouvriers[idouvrier].trouvercible(self.parent.joueurs)
        
    def creerouvrier(self):
        idmaison=random.choice(list(self.maisons.keys()))
        idouvrier=getprochainid()
        maison=self.maisons[idmaison]
        x=maison.x+40+(random.randrange(30)-15)
        y=maison.y +(random.randrange(30)-15)
        self.ouvriers[idouvrier]=Ouvrier(self,idouvrier,maison,x,y)
        
        
    def jouerprochaincoup(self):
        self.decideraction()
        
        for i in self.ouvriers.keys():
            self.ouvriers[i].deplacer()
    
    def decideraction(self):
        if self.delaiaction==0:
            action=random.choice(list(self.actions.keys()))
            self.actions[action]()
            self.delaiaction=random.randrange(30,60)
        else:
            self.delaiaction-=1
            
    def ciblerbalise(self):
        pass
            