#!/usr/bin/python

import time
import json
import sqlite3
import collections

from domoDatabase import *
from bluetoothServer import BluetoothServer

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


# Classe pour chaque websocket ouverte        
# ============================================================================

class WebSockClient(WebSocket):

    moduleClientID = 0
        
    def handleConnected(self):
        print(self.address, 'connected')
    
    def handleClose(self):
        print(self.address, 'closed')

    def handleMessage(self):
        try:
            obj = json.loads(self.data)
            if not obj: return
            
            typeRequete = obj['typeReq']
            if not typeRequete: return
            requete = obj['msg']
            if not requete: return
            params = obj['params']
            
            # En fonction du type de requete on renvoie ou non un resultat
            try:
                # Methode GET
                # ----------------------------------------------------------------------------------------------
                if typeRequete == 'GET' :
                    if hasattr(self, 'handle_' + requete) :
                        # Traitement specifiques avant envoi de la requete en DB
                        getattr(self, 'handle_' + requete)(requete, params)
                    else:
                        # Demande d'envoi direct en DB
                        self.sendReqToDB(requete, params)
                        
                # Methode SET - Ex : {"typeReq":"SET","msg":"setTemperature","params":[{"temperature":22.00}]}
                # ----------------------------------------------------------------------------------------------
                elif typeRequete == "SET"  and self.moduleClientID != 0:
                    if hasattr(self, 'handle_' + requete) :
                        # Traitement specifiques avant envoi de la requete en DB
                        getattr(self, 'handle_' + requete)(requete, params)
                    else:
                        # Demande d'envoi direct en DB
                        for param in params:
                            # On ajoute en parametres l'id du module qui fait le SET. Exemple : [{'idModule': 1, 'temperature': 22.0}, {...}]
                            param['idModule'] = self.moduleClientID
                            self.sendReqToDB(requete, param)
                            
            except Exception as e:
                print ('WEBSOCKET ERROR ! methode : ',  requete, ' - Erreur : ', repr(e))
        except Exception as e:
            print ('WEBSOCKET ERROR : ',  repr(e))
    
    # sendResponse - Repond via la socket a une demande recue
    def sendResponse(self, requete, response):
        # Puis on ajoute les dictionnaire de data
        dict = collections.OrderedDict()
        dict['typeReq'] = 'REP'
        dict['msg'] = requete
        dict['params'] = response
        j = json.dumps(dict)
        self.sendMessage(j)
    
    def sendReqToDB(self, requete, param):
        if hasattr(DB, requete) :
            getattr(DB, requete)(param)
        else:
            print ('WEBSOCKET WARNING ! Requete ', requete,' non geree par la database')
                             
    # GetModuleID - Recupere l'ID du module en fonction de son adresse
    # --------------------------------------------------------
    def handle_getModuleID(self, requete, param):
        adrModule = param['adrModule']
        if hasattr(DB, requete) :
            resultReq = getattr(DB, requete)(adrModule)
            self.moduleClientID = resultReq['ID']
    
    # GetListeModule - Recupere tous les modules connus
    # --------------------------------------------------------
    def handle_getListeModule(self, requete, param):
        if hasattr(DB, requete) :
            resultReq = getattr(DB, requete)()            
            jsonResponse = json.dumps(resultReq)
            self.sendResponse(requete, jsonResponse)
                    
    # SetModule - Set des donnees du module connecte
    # --------------------------------------------------------
    def handle_setModule(self, requete, param):
        adrModule = param['adrModule']
        nomModule = param['nomModule']
        if hasattr(DB, requete) :
            getattr(DB, requete)(adrModule, nomModule)
            
#    # SetTemperature - Set d'une nouvelle temperature recue
#    # --------------------------------------------------------                
#    def handle_setTemperature(self, requete, params):
#        for param in params:
#            self.sendReqToDB(requete, param)               
#
#    # SetHumidite - Set d'une nouvelle valeur d'humidite recue
#    # --------------------------------------------------------     
#    def handle_setHumidite(self, requete, param):
#        for param in params:
#            self.sendReqToDB(requete, param)
        
        
# Classe de serveur de Websocket      
# ============================================================================

class WebSockServer(SimpleWebSocketServer):

    # Initialisation du serveur
    # *****************************************
    def __init__(self, host, port, websocketclass):
        SimpleWebSocketServer.__init__(self, host, port, websocketclass)
        
        # Lancement du serveur bluetooth
        serverBT = BluetoothServer(self)
        serverBT.setDaemon(True)
        serverBT.start()
        
        self.serveforever()

# MAIN
# ============================================================================
if __name__ == "__main__" :
    
    # Creation de la database
    DB = DomoDatabase(dbName)
    print ('Opened database successfully')
    
    # Lancement du serveur websocket 
    server = WebSockServer('', 8000, WebSockClient)
    