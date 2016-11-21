import sqlite3
connection = sqlite3.connect('../database.db3')
cursor = connection.cursor()
cursor.execute('SELECT SQLITE_VERSION()')
data = cursor.fetchone()    
print "SQLite version: %s" % data
cursor.execute("SELECT * FROM temperatures")
cursor.execute("SELECT * FROM modules")
rows = cursor.fetchall()
for row in rows:
        print row
