
# Classe mère de tout les upgrades
# --------------------------------
class UpgradeTest():
    def __init__(self, param):
        name, description, productionTime, cost, prerequisites, img = param    # Les arguments doivent être passé dans cet ordre là

        self.name = name
        self.description = description
        self.productionTime = productionTime    # Temps que ça prend pour le faire
        self.cost = cost                        
        self.prerequisites = prerequisites      # La liste des upgrades qui doivent être fait pour débloquer celui-ci
        self.img = img                          # Icone sur le bouton de l'upgrade

    def effect(self, player):   # Définis dans les sous-classes
        return

# -------------------------------------------------------------------------------------------------------------------------------------



# Liste de tout les upgrades qui existent dans le jeu + un tit registre
# ---------------------------------------------------------------------

class ProteinShake():
    def __init__(self):
        UpgradeTest.__init__(self, # Parent constructor
        ["Protein shakes",
         "Le pouvoir des protéines : Augmente la quantité de ressources que peut transporter tout les slaves de 50%", # Une description        
        None,   # Time
        None,   # Cost
        None,   # Prerequesite
        None])   # Icon    

    def effect(self, player): # Effet de l'upgrade sur le joueur/partie
        slaveList = player.persos['ouvrier']
        for slave in slaveList: 
            slaveList[slave].quota += slaveList[slave].quota / 2
        

# Registre qui contient une instance de chaque upgrade
class UpgradeRegistry():
    UPGRADES = {
        "Protein shakes":ProteinShake(),
    }