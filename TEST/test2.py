import sqlite3

conn = sqlite3.connect('CocPlayer.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 

clan_tag = '#2QGJGJ'
cursor.execute('SELECT clanID FROM Player WHERE clanID = ?', (clan_tag,))
clanResult = cursor.fetchone()
print(clanResult)