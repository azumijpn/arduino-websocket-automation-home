#!/usr/bin/python

import bluetooth
import threading
import time
import json
import collections
import time
import random
import websocket

listConnectedDevice = []

nomDeviceBTrecherche  = "HC-06"
nomServerWebSocket    = "ws://localhost:8000"


# Classe thread du serveur BT
# ======================================================================

class BluetoothServer(threading.Thread):
    
    # Classe thread de la socket ouverte pour le client BT
    # ======================================================================
    
    class ClientBTThread(websocket.WebSocketApp, threading.Thread):
    
        # Methode de reception de message sur la WebSocket
        def on_message(ws, message):
            print (message)
            
        # Methode de reception d'une erreur sur la WebSocket
        def on_error(ws, error):
            print (error)
            
        # Methode de reception d'une fermeture de la WebSocket
        def on_close(self, cr):
            print (self.adrBTclient, ": Serial connection is disconnected")
            self.sockBT.close()
            self.threadIsOK = False
                        
        # Methode de reception de message sur la liaison BT
        def run(ws):
            sautDeLigne = "\r\n"
            #buff = ""
            try:
                buff = ""
                while True and ws.threadIsOK == True:   
                    buff = buff + ws.sockBT.recv(1024).decode()
                    if len(buff) == 0: continue
                    try:
                        indexRetourCh = buff.index(sautDeLigne)
                    except ValueError:
                        continue
                    data = buff[:indexRetourCh]
                    ws.handleBTMessage(data)
                    buffDecoup = buff.split(data+sautDeLigne)
                    if len(buffDecoup) > 1 : 
                        buff = buffDecoup[1]
                    else:
                        buff = ""
            except Exception as e:
                print ("SERIAL ERROR: " + repr(e))
                
        # Methode de traitement de la trame JSON recue en BT pour l'envoyer directement au serveur via la websocket
        def handleBTMessage(self, data):
            #print (self.adrBTclient, "- Received %s" % data)
            self.ws.send(data)  
        
        # Methode generique d'envoi de trame JSON via la socket ouverte
        def send (self, typeReq, requete, params):
            # On envoie les donnees du modules au serveur
            dict = collections.OrderedDict()
            dict['typeReq'] = typeReq
            dict['msg'] = requete
            dict['params'] = params
            obj = json.dumps(dict)
            self.ws.send(obj)
        
        # Initialisation du thread client de la liaison BT                 
        def __init__ (self, sock, btClient_adresse, btClient_name):
            threading.Thread.__init__(self)  
            
            # Sauvegarde des parametres
            self.sockBT         = sock
            self.adrBTclient    = btClient_adresse
            self.nameBTclient   = btClient_name
            
            # Ouverture d'une WebSocket pour discuter avec le serveur
            self.ws = websocket.WebSocketApp(nomServerWebSocket, on_message = self.on_message, on_close = self.on_close)
            self.wst = threading.Thread(target=self.ws.run_forever)
            self.wst.daemon = True
            self.wst.start()
            self.threadIsOK = True
            time.sleep(2)
            
            # On envoie les donnees du modules au serveur
            params = collections.OrderedDict()
            params['adrModule'] = self.adrBTclient
            params['nomModule'] = self.nameBTclient
            self.send('SET', 'setModule', params)
    
            # On fait une demande au serveur au pour qu'il envoie l'ID du module
            params = collections.OrderedDict()
            params['adrModule'] = self.adrBTclient
            self.send('GET', 'getModuleID', params)
            
            # Apres l'initialisation, la methode Run est appele

         
    # Methodes globales
    # ======================================================================
    def deviceIsAlreadyConnected(btServ, addrDevice):
        
        for device in listConnectedDevice: 
            if device == addrDevice:
                print ("Module deja connecte :", addrDevice)
                return True
        return False
        
    
    # Initialisaiton + Boucle principale
    # ======================================================================
    def __init__ (btServ, serverWebSocket):    
        threading.Thread.__init__(btServ)   
        btServ.serverWS = serverWebSocket
        
    def run(btServ):
        print ('Lancement du seveur bluetooth...'     )               
        while True:
            # Recherche le device bluetooth non-connecte
            non_connected_devices = bluetooth.discover_devices()
            # Si on en trouve
            for device in non_connected_devices:
                # Si le nom du device est celui recherche
                #if nomDeviceBTrecherche == bluetooth.lookup_name(device) and btServ.deviceIsAlreadyConnected(device) == False :
                if nomDeviceBTrecherche == bluetooth.lookup_name(device) :
                    target_address = device
                    if target_address is not None:
                        # Connection avec le module et instanciation d'un thread dedie
                        print ("Module bluetooth trouve :", target_address)
                        try:
                            client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                            client_sock.connect((target_address, 1))
                            print (target_address, ": Serial connection is accepted")
                            echo = btServ.ClientBTThread(client_sock, target_address, bluetooth.lookup_name(device))
                            #echo = btServ.ClientBTThread()
                            echo.setDaemon(True)
                            echo.start()
                            listConnectedDevice.append(target_address)
                        except IOError as e:
                            print ("SERIAL ERROR: " + repr(e))
                            print ("Erreur bluetooth. Module ignore : ", target_address)
                break
    
        print ("all done")
