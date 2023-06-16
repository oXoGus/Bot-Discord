import sqlite3

conn = sqlite3.connect('CocPlayer.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 


cursor.execute('DELET * FROM Player')
resultat = cursor.fetchall()
for line in resultat:
    print(line[1])