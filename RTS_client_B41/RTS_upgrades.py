
# Classe mère de tout les upgrades
# --------------------------------
class UpgradeTest():
    def __init__(self, param):
        name, description, productionTime, cost, prerequisites, img = param    # Les arguments doivent être passés dans cet ordre là

        self.name = name
        self.description = description
        self.productionTime = productionTime    # Temps que ça prend pour le faire
        self.cost = cost                        
        self.prerequisites = prerequisites      # La liste des upgrades qui doivent être fait pour débloquer celui-ci
        self.img = img                          # Icone sur le bouton de l'upgrade
        
    def effect(self, player):   # Définis dans les sous-classes. Nécessaires, car python ne supporte pas les méthodes anonymes
        return

# -------------------------------------------------------------------------------------------------------------------------------------



# Liste de tout les upgrades qui existent dans le jeu + un tit registre
# ---------------------------------------------------------------------

class ProteinShake():
    def __init__(self):
        UpgradeTest.__init__(self, # Parent constructor
        ["Protein shakes",
         "Augmente la quantité de ressources que peut transporter tout les slaves de 50%", # Une description        
        None,   # Time
        None,   # Cost
        None,   # Prerequesite
        None])   # Icon    

    def effect(self, player): # Effet de l'upgrade sur le joueur/partie
        quota = player.prototypePersos['ouvrier'].quota
        quota += quota * 0.50  
        player.prototypePersos['ouvrier'].quota = quota  # Modifie le prototype des slaves
        
        slaveList = player.persos['ouvrier']
        for slave in slaveList: 
            slaveList[slave].quota = quota  # Augmente immédiatement tout les quotas des slaves en vie du joueur

class BetterShoes():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Better shoes",
         "Augmente la vitesse de déplacement des slaves de 50%",    
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        vitesse = player.prototypePersos['ouvrier'].vitesse
        vitesse += vitesse * 0.50  
        player.prototypePersos['ouvrier'].vitesse = vitesse  # Modifie le prototype des slaves
        
        slaveList = player.persos['ouvrier']
        for slave in slaveList: 
            slaveList[slave].vitesse = vitesse 

class Scope():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Scope",
         "Augmente la distance d'attaque des chickens de 100%",    
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        atkRange = player.prototypePersos['chicken'].atkRange
        atkRange += atkRange 
        player.prototypePersos['chicken'].atkRange = atkRange  
        
        chickenList = player.persos['chicken']
        for c in chickenList: 
            chickenList[c].atkRange = atkRange 

class SuperPigs():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Super pigs",
         "Améliore les pigs en super pigs, mieux armés et plus puissants. Peut maintenant produire des super pigs",    
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        return
        # Remplace le choix de production des pigs en super pigs, dans tout les pigpen du joueur
        
        # . . .

        # Copie les pigs et créer des super pigs identiques        
        # pigList = player.persos['pig']
        # superPigList = player.persos['superPigs']
        # for p in pigList: 
        #     superPigList.push(pigList[p])
        #     pigList[p].copyAttributes(player.prototypePersos['superPigs'])


class DefenseTier1():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Defense Tier 1",
         "Augmente la défense de tous les unités de +1",    
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        for p in player.prototypePersos:
            player.prototypePersos[p].defense += 1     # Modifie tout les prototypes

            for u in player.persos[p]:  # Modifie tout les unités actuelles
                u.defense += 1



class DefenseTier2():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Defense Tier 2",
         "Augmente la défense de tous les unités de + 1",    
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        for p in player.prototypePersos:
            player.prototypePersos[p].defense += 1     # Modifie tout les prototypes

            for u in player.persos[p]:  # Modifie tout les unités actuelles
                u.defense += 1


class DefenseTier3():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Defense Tier 3",
         "Augmente la défense de tous les unités de + 2",    # Augmente de +2. Ceci récompense le joueur pour commit dans ses upgrades
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        for p in player.prototypePersos:
            player.prototypePersos[p].defense += 2     # Modifie tout les prototypes

            for u in player.persos[p]:  # Modifie tout les unités actuelles
                player.persos[p][u].defense += 2


class AttackTier1():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Attack Tier 1",
         "Augmente les dégât infligés de tous les unités de +1",    
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        for p in player.prototypePersos:
            player.prototypePersos[p].atkDmg += 1     

            for u in player.persos[p]:  
                u.atkDmg += 1



class AttackTier2():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Attack Tier 2",
         "Augmente les dégât infligés de tous les unités de + 1",    
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        for p in player.prototypePersos:
            player.prototypePersos[p].atkDmg += 1     

            for u in player.persos[p]:  
                u.atkDmg += 1


class AttackTier3():
    def __init__(self):
        UpgradeTest.__init__(self, 
        ["Attack Tier 3",
         "Augmente les dégât infligés de tous les unités de + 2",   
        None,  
        None,   
        None,   
        None])     

    def effect(self, player): 
        for p in player.prototypePersos:
            player.prototypePersos[p].atkDmg += 2     
            for u in player.persos[p]: 
                player.persos[p][u].atkDmg += 2
        


# Registre qui contient une instance de chaque upgrade
class UpgradeRegistry():
    UPGRADES = {
        "Protein shakes":ProteinShake(),
        "Better shoes":BetterShoes(),
        "Scope":Scope(),
        "Defense Tier 1":DefenseTier1(),
        "Defense Tier 2":DefenseTier2(),
        "Defense Tier 3":DefenseTier3(),
        "Attack Tier 1":AttackTier1(),
        "Attack Tier 2":AttackTier2(),
        "Attack Tier 3":AttackTier3(),
    }