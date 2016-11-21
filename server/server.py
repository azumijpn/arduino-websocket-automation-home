from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import sqlite3
import time
import config

# ============================================================================
# DataBase Structure
# ============================================================================

SQL_CREATE_MODULES = """
CREATE TABLE IF NOT EXISTS modules (
	ID		integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	address  	varchar(30) NOT NULL UNIQUE,
	type		varchar(30) UNIQUE DEFAULT UNKNOWN,
	location	varchar(30) UNIQUE DEFAULT UNKNOWN
)
"""

SQL_CREATE_TEMPERATURES = """
CREATE TABLE IF NOT EXISTS temperatures (
	ID         	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	ID_Module  	integer NOT NULL,
	temperature     float(50) NOT NULL,
	time     	datetime NOT NULL
)
"""

SQL_CREATE_HYGROMETRIE = """
CREATE TABLE IF NOT EXISTS hygrometrie (
	ID         	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	ID_Module  	integer NOT NULL,
	hygrometrie     integer NOT NULL,
	time     	datetime NOT NULL
)
"""

# ============================================================================
class DashboardDatabase(object) :

    def __init__(self, dbname) :
        self.db = sqlite3.connect(dbname)
        cursor = self.db.cursor()
        cursor.execute(SQL_CREATE_MODULES)
        cursor.execute(SQL_CREATE_TEMPERATURES)
        cursor.execute(SQL_CREATE_HYGROMETRIE)
        self.db.commit()

    def addTemperature(self, address, time, temperature):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO temperatures(time, temperature) VALUES (?, ?)", (time, temperature))
        self.db.commit()

    def addModule(self, address):
        cursor = self.db.cursor()
	cursor.execute("INSERT OR IGNORE INTO modules(address) VALUES (?)", [address])
        self.db.commit()

DB = DashboardDatabase("database.db3")

# ============================================================================
class DashboardWebSocketHandler(WebSocket):

    def handleConnected(self):
	DB.addModule(self.address[0])
	print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

	# Example Json OBJ ==> { 'msg': 'setTemperature', 'temperature': '18.13' }
    def handleMessage(self):
        print('message :', self.data)
        obj = json.loads(self.data)
        if not obj: return
        msg = obj['msg']
        print('msg :', msg)
        if not msg: return
        methodName = "handle_" + msg
        if hasattr(self, methodName) :
            getattr(self, methodName)(obj)

    def handle_setTemperature(self, obj):
        temperature = float(obj['temperature'])
        print('temperature', temperature)
        now = int(time.time())
        print('time', now)
        DB.addTemperature(self.address, now, temperature)
        self.sendTemperature(now, temperature)

    def sendTemperature(self, time, temperature):
        print('sendTemperature :', temperature)
        obj = {'msg': 'temperature', 'temperature': temperature, 'time': time}
        msg = json.dumps(obj)
        for fileno, connection in self.server.connections.items() :
            connection.sendMessage(msg)

# ============================================================================
if __name__ == "__main__" : 
    server = SimpleWebSocketServer(config.socketBind, config.socketPort, DashboardWebSocketHandler)
    server.serveforever()
