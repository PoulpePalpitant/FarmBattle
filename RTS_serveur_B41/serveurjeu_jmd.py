# -*- coding: utf-8 -*-

from flask import Flask,request,json
from werkzeug.wrappers import Response
import random
import sqlite3

app=Flask(__name__)

app.secret_key="qwerasdf1234"
class Dbman():
    def __init__(self):
        self.conn = sqlite3.connect("baseRTS.db")
        self.curs = self.conn.cursor()

    def setpartiecourante(self,chose):
        self.vidertable("partiecourante")
        self.curs.execute("Insert into partiecourante (etat) VALUES(?);",(chose,))
        self.conn.commit()

    def setinitaleatoire(self,chose):
        self.vidertable("initaleatoire")
        self.curs.execute("Insert into initaleatoire (initaleatoire) VALUES(?);",(chose,))
        self.conn.commit()

    def setnbrIA(self,chose):
        self.vidertable("nbrIA")
        self.curs.execute("Insert into nbrIA (nbrIA) VALUES(?);",(chose,))
        self.conn.commit()

    def setcadrecourant(self,chose):
        self.vidertable("cadrecourant")
        self.curs.execute("Insert into cadrecourant (cadrecourant) VALUES(?);",(chose,))
        self.conn.commit()

    def ajouterjoueur(self,nom):
        self.curs.execute("Insert into joueurs (nom) VALUES(?);",(nom,))
        self.conn.commit()

    def ajouteractionaujoueur(self,nom,cadrejeu,action):
        self.curs.execute("Insert into actionsenattente (nom,cadrejeu,action) VALUES(?,?,?);",(nom,cadrejeu,action))
        self.conn.commit()

    def getinfo(self,table):
        sqlnom="select * from '"+table+"'"
        self.curs.execute(sqlnom)
        info=self.curs.fetchall()
        return info

    def getinfoconditionel(self,table,champ,valeur):
        sqlnom="select * from '"+table+"' WHERE nom=?"
        self.curs.execute(sqlnom,(valeur))
        info=self.curs.fetchall()
        return info

    def resetdb(self):
        tables=["partiecourante","joueurs","cadrecourant","actionsenattente","initaleatoire","nbrIA"]
        for i in tables:
            self.vidertable(i)

        self.curs.execute("Insert into partiecourante (etat) VALUES(?);",("dispo",))
        self.curs.execute("Insert into cadrecourant (cadrecourant) VALUES(?);",(0,))
        self.curs.execute("Insert into initaleatoire (initaleatoire) VALUES(?);",(2020,))
        self.curs.execute("Insert into nbrIA (nbrIA) VALUES(?);",(0,))
        self.conn.commit()

    def effaceractionsjoueur(self,joueur):
        self.curs.execute("DELETE from actionsenattente WHERE  nom=?",(joueur,))
        self.conn.commit()

    def vidertable(self,table):
        self.curs.execute("DELETE from "+table)
        self.conn.commit()

    def fermerdb(self):
        self.conn.close()



@app.route("/testjeu", methods=["GET","POST"])
def testjeu():
    db=Dbman()
    info=db.getinfo("partiecourante")

    return Response(json.dumps(info), mimetype='application/json')
    #return repr(info)

@app.route("/resetjeu", methods=["GET","POST"])
def resetjeu():
    db=Dbman()
    db.resetdb()
    return "Reset fait"

@app.route("/creerpartie", methods=["GET","POST"])
def creerpartie():
    db=Dbman()
    info=db.getinfo("partiecourante")
    if "dispo" in info[0]:
        if request.method=="POST":
            nom=request.form["nom"]
            valoptions=request.form["valoptions"]
            db.ajouterjoueur(nom)
            db.setpartiecourante("attente")

            joueurs=db.getinfo("joueurs")
            reponse=[joueurs,valoptions]
            return Response(json.dumps(reponse), mimetype='application/json')
            #return repr([joueurs,valoptions])
    else:
        return str("banane")

@app.route("/inscrirejoueur", methods=["GET","POST"])
def inscrirejoueur():
    db=Dbman()
    info=db.getinfo("partiecourante")
    if "attente" in info[0]:
        if request.method=="POST":
            nom=request.form["nom"]
            valoptions=request.form["valoptions"]
            db.ajouterjoueur(nom)

            joueurs=db.getinfo("joueurs")
            reponse=[joueurs,valoptions]
            return Response(json.dumps(reponse), mimetype='application/json')
            #return repr([joueurs,valoptions])
    else:
        return "Erreur d'inscription"


@app.route("/lobbyjoueur", methods=["GET","POST"])
def lobbyjoueur():
    db=Dbman()
    info=db.getinfo("partiecourante")
    if "courante" in info[0]:
        nbrIA=db.getinfo("nbrIA")
        initaleatoire=db.getinfo("initaleatoire")
        reponse=["courante",initaleatoire,nbrIA]
        return Response(json.dumps(reponse), mimetype='application/json')
        #return str(["courante",initaleatoire,nbrIA])
    else:
        info=db.getinfo("joueurs")
        #maliste=[]
        #for i in info:
        #    maliste.append(i)

        return Response(json.dumps(info), mimetype='application/json')
        #return repr(info)

@app.route("/lancerpartie", methods=["GET","POST"])
def lancerpartie():
    db=Dbman()
    if request.method=="POST":
        nom=request.form["nom"]
        nbrIA=request.form["nbrIA"]

        initrand=random.randrange(1000,10000)
        db.setnbrIA(nbrIA)
        db.setinitaleatoire(initrand)
        db.setpartiecourante("courante")

        return "courante"

@app.route("/bouclersurjeu", methods=["POST"])
def bouclersurjeu():
    db=Dbman()
    cadreactuel=db.getinfo("cadrecourant")[0]
    if request.method=="POST":
        nom=request.form["nom"]
        cadrejeu=request.form["cadrejeu"]
        actionsrequises=request.form["actionsrequises"]
        cadrejeu=int(cadrejeu)
        cadreactuel=cadreactuel[0]
        # ON CALCULE LE CADRE DE L'ACTION REQUISE
        sautdecadre=10
        if cadreactuel<cadrejeu:
            db.setcadrecourant(cadrejeu)
            cadreajouer=cadrejeu+sautdecadre
        else:
            cadreajouer=cadreactuel+sautdecadre

        # ON AJOUTE LES ACTIONS À TOUS LES JOUEURS
        if actionsrequises!="None":
            info=db.getinfo("joueurs")
            for i in info:
                db.ajouteractionaujoueur(i[0],cadreajouer,actionsrequises)

        # ON CHERCHE S'IL Y A DES ACTIONS QUE NOUS AYONS À RECEPTIONNER
        info=db.getinfo("actionsenattente")

        maliste=[]
        for i in info:
            if i[0]==nom:
                maliste.append([i[1],i[2]])
        db.effaceractionsjoueur(nom)
        db.fermerdb()

        return Response(json.dumps(maliste), mimetype='application/json')
        #return repr(maliste)

if __name__ == '__main__':
    #dbman=Dbman()
    app.run(debug=True)



