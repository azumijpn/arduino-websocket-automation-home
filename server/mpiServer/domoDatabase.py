#!/usr/bin/python

import sqlite3
from datetime import date, datetime
import collections
import json

# Definition de requetes SQL
# ======================================================================
dbName = "domoDatabase.db3"

#SQL_CREATE_TABLE_HYGROMETRIE = """
#CREATE TABLE IF NOT EXISTS Hygrometrie (
#  ID         integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#  ID_Module  integer NOT NULL,
#  valeur     integer NOT NULL,
#  "date"     datetime NOT NULL)"""

  
SQL_CREATE_TABLE_HYGROMETRIE = """
CREATE TABLE IF NOT EXISTS [Hygrometrie] (
[id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
[id_lieu] INTEGER UNIQUE NULL,
[date] DATE DEFAULT CURRENT_DATE NOT NULL,
[hygro] FLOAT NOT NULL
)"""

SQL_CREATE_TABLE_LIEU = """
CREATE TABLE IF NOT EXISTS [Lieu] (
[id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
[libelle] VARCHAR(50) DEFAULT 'NR' NULL
)"""

SQL_CREATE_TABLE_TYPE_MODULE = """ 
CREATE TABLE IF NOT EXISTS [TypeModule] (
[id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
[type] VARCHAR(50) UNIQUE NOT NULL
) """ 

SQL_CREATE_TABLE_MODULE = """
CREATE TABLE IF NOT EXISTS [Module] (
[id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
[id_lieu] INTEGER NULL,
[id_typeModule] INTEGER NOT NULL,
[libelle] VARCHAR(50) NULL,
[adresse] VARCHAR(50) NULL,
[isConnected] BOOLEAN DEFAULT '0' NOT NULL,
[dateDernierContact] DATE NOT NULL
) """
  
SQL_CREATE_TABLE_TEMPERATURE = """ 
CREATE TABLE IF NOT EXISTS [Temperature] (
[id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
[id_lieu] INTEGER NOT NULL,
[id_module] INTEGER NOT NULL,
[date] DATE DEFAULT CURRENT_DATE NOT NULL,
[temp1] FLOAT NOT NULL,
[temp2] FLOAT NULL,
[temp3] FLOAT NULL
) """
  

  
SQL_UPDATE_LASTCONNECT	= """ UPDATE Module SET dateDernierContact = (datetime('now','localtime')) WHERE ID = ? """

SQL_GET_MODULE			= """ SELECT id, libelle, dateDernierContact FROM Module"""
SQL_GET_MODULE_ID 		= """ SELECT id FROM Module WHERE adresse = ? ORDER BY ROWID ASC LIMIT 1"""
SQL_INSERT_MODULE 		= """ INSERT INTO Module(libelle, adresse, dateDernierContact) VALUES (?,?,datetime('now','localtime')) """
SQL_UPDATE_MODULE 		= """ UPDATE Module SET libelle = ? WHERE adresse = ? """

SQL_GET_TEMPERATURE		= """ SELECT temp1, date FROM Temperature """
SQL_INSERT_TEMPERATURE	= """ INSERT INTO Temperature(id_module, temp1, date) VALUES (?,?,datetime('now','localtime')) """

SQL_INSERT_HUMIDITE		= """ INSERT INTO Hygrometrie(id_module, hygro, date) VALUES (?,?,datetime('now','localtime')) """

# Methode permettant de concstruire le dictionnaire de resultat d'une requete SQL
def dict_factory(cursor, row):
    resultDict = dict()
    for idx, col in enumerate(cursor.description):
        # create a new array in this slot
        resultDict[col[0]] = row[idx]   
    #print (resultDict)
    return resultDict
    
# Classe d accession a la DB
# ======================================================================
class DomoDatabase(object):
    
    def __init__(self, dbname):
        self.db = sqlite3.connect(dbname, check_same_thread = False)
        self.db.row_factory = dict_factory
        cursor = self.db.cursor()
        cursor.execute(SQL_CREATE_TABLE_HYGROMETRIE)
        cursor.execute(SQL_CREATE_TABLE_LIEU)
        cursor.execute(SQL_CREATE_TABLE_MODULE)
        cursor.execute(SQL_CREATE_TABLE_TEMPERATURE)
        cursor.execute(SQL_CREATE_TABLE_TYPE_MODULE)
        self.db.commit()
        
    # METHODES SET
    # ======================================================================
    
    # Permet de mettre a jour la date de derniere connexion a la base
    def setDateDernierContactModule(self, idModule):
        cursor = self.db.cursor()
        cursor.execute(SQL_UPDATE_LASTCONNECT, (idModule,))
        self.db.commit()
        
    # Insertion des donnees concernant le module
    def setModule(self, moduleAdresse, moduleNom):
        # Recuperation de l'ID du module concerne
        cursor = self.db.cursor()
        cursor.execute(SQL_GET_MODULE_ID, (moduleAdresse,))
        row = cursor.fetchone()
        # Insertion ou MAJ dans la base
        if row == None:
            cursor.execute(SQL_INSERT_MODULE, [moduleNom, moduleAdresse])
        else:
            cursor.execute(SQL_UPDATE_MODULE, [moduleNom, moduleAdresse])
        self.db.commit()
        print(row)
        self.setDateDernierContactModule(row['ID'])

    # Sauvegarde en base de la temperature
    def setTemperature(self, param):
        # Recuperation des parametres
        idModule         = param['idModule']
        temperature      = param['temperature']
        print ('Insertion de la temperature :', str(temperature), '°C du module ID n°', str(idModule))
        # Execution de la requete
        cursor = self.db.cursor()
        cursor.execute(SQL_INSERT_TEMPERATURE, (idModule, temperature))
        self.db.commit()
        self.setDateDernierContactModule(idModule)

    # Sauvegarde en base du taux d humidite
    def setHumidite(self, param):
        # Recuperation des parametres
        idModule         = param['idModule']
        humidite         = param['humidite']
        print ('Insertion de l hygrometrie :', str(humidite), '% du module ID n°', str(idModule))
        # Execution de la requete
        cursor = self.db.cursor()
        cursor.execute(SQL_INSERT_HUMIDITE, (idModule, humidite))
        self.db.commit()
        self.setDateDernierContactModule(idModule)
            
    # METHODES GET
    # ====================================================================== 
       
    # Permet de recuperer la liste des modules
    def getListeModule(self):
        cursor = self.db.cursor()
        rows = cursor.execute(SQL_GET_MODULE).fetchall()
        return rows

        
    # Permet de recuperer l ID d un module en fonction de l'adresse
    def getModuleID(self, moduleAdresse):
        cursor = self.db.cursor()
        rows = cursor.execute(SQL_GET_MODULE_ID, (moduleAdresse,)).fetchone()
        return rows
        
    # Permet de recuperer les temperature demandee
    def getTemperature(self, returnDict, param):
        try:
            cursor = self.db.cursor()
            cursor.execute(SQL_GET_TEMPERATURE)
            rows = cursor.fetchall()    
            objects_list = []
            # On commence par ajouter le dictionnaire permettant d'indentifier la demande
            objects_list.append(returnDict)
            for row in rows:
                # Puis on ajoute les dictionnaire de data
                dict = collections.OrderedDict()
                dict['valeur'] = row[0]
                dict['date'] = row[1]
                objects_list.append(dict)
            j = json.dumps(objects_list)
            print (j)
            return j
        except Exception as e:
            print ("ERROR: Caught exception: " + repr(e))
            raise e
            sys.exit(1)

