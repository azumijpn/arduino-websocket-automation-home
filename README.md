## Arduino Websocket Automation Home

### Description
L'objectif de ce github est de creer une application opensource de domotique très simple. Elle regroupe des fonctionnalités:
- Dashboard bootstrap: Permettra d'afficher les données avec une interface responsive design.
- Un serveur: Ecrit en python, ce serveur récupère les données provenant d'un client et les inserts dans une base de donnée.
- Une base de donnée: Stock les données des capteurs répartie sur les cartes arduinos.
- Un client collectant les données et les envoyants au serveur.

```Javascript
                                                |-----------|
                                                |    www    |
                                                |           |
                                                |-----------| 
                                                      ||
                                                      ||
                                                      ||(WebSocket)
                                                      ||
|-----------|                                   |-----------|        |-----------|
|  Arduino  |                                   |  Python   |        | Data Base |
|  sensors  |<=========Ethernet/Wireless=======>|  Server   |<======>|  SQLlite  |
| Websocket |            (WebSocket)            | Websocket |        |-----------|
|-----------|                                   |-----------|
```

### ROADMAP

- Client/sensors:
	- Ecriture du client (C/C++): Regroupe essentiellement des capteurs: Température, Pression, Niveau, UV, Hall
	- Gérer la possibilité d'envoyer des commandes au client: Pilotage relay, moteur

- Serveur:
	- Ecriture du serveur
	- Inscription des valeurs dans la base de données
	- fichier de configuration du serveur (config.py)

- Base de donnée:
	- Créer/trouver une organisation de la base de données

- www:
	- Page Web du dashboard
	- Exploiter la remonter des données de la base de données
	- Intégrer des graphiques style http://www.highcharts.com/demo/dynamic-update ou Charts.js.org

### Prerequis

#### Installation

You can install SimpleWebSocketServer by running the following command...
sudo pip install git+https://github.com/dpallot/simple-websocket-server.git

Or by downloading the repository and running sudo python setup.py install.
Installation via pip is suggested.

Compiler avec l'IDE arduino 1.6.2 ou superieur.


### Credit

- https://github.com/djsb/arduino-websocketclient
- https://github.com/adngdb/python-websocket-server/blob/master/websocketserver.py
- https://github.com/dpallot/simple-websocket-server

---------------------
The MIT License (MIT) https://opensource.org/licenses/MIT
