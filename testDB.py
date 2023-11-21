import sqlite3
from trpData import clanMembersDB 
import time
import requests, json, traceback, random
from trpData import betterTroops, trpRoseFR, enginDeSiegeAPI, trpRoseAPI, clanMembersDB, emojiTrpRoseFR, superToopsAPI, trpNoirFR, emojiTrpNoirFR , trpNoirAPI, hdvPNG, sortAPI, sortDataFR , emojiSortFR, laboPNG, herosAPI, hérosFR, emojiHero, ligueAPI, emojiFamillier, famillierAPI, herosthumbnail, emojiLabo, herostemoji, labelsEmoji, clanType, ligueLDC
from config import TOKEN, GDCBotheader, laboHeader, clanHeader, infoGeneraleHeader

conn = sqlite3.connect('test.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 


def innitUpdateDB():
    i = random.random() 
    try:
        resp = requests.get(url=f"https://api.clashofclans.com/v1/clans/%232Q8G0LPU0", headers=clanHeader)
        resp.raise_for_status()
        resp = resp.json()
        clan = json.dumps(resp)
        clanJSON = json.loads(clan)
        member = clanJSON['memberList'] # on recupere la liste des membre
        try:
            cursor.execute(f"SELECT * FROM clanMembers_2Q8G0LPU3") #on cherche si la table existe deja (exeption si la table n'existe pas)
            for stat in member: # pour chaque membre
                try:
                    playerTag = stat['tag'] # on recupere le tag des membre
                    playerID = playerTag[1:] # on retire le hastag
                    responsePlayer = requests.get(url=f'https://api.clashofclans.com/v1/players/%23{playerID}', headers=clanHeader) #on recupere les info des joueurs
                    time.sleep(1) # pour depasser la limite de requete 
                    responsePlayer.raise_for_status() # exeption si il y a une erreur 
                    # on recupere les donnée pour la database
                    player_json = responsePlayer.json()
                    playerJSON = json.dumps(player_json) # convertit en chaine de caractere pour la DB 
                    playerData = json.loads(playerJSON) # conv en JSON
                    cursor.execute(f"SELECT * FROM clanMembers_2Q8G0LPU3 WHERE playerID = ?", (playerTag, )) # si le joueur etait deja dans le clan 
                    if cursor.fetchone() is not None:
                        cursor.execute(f"UPDATE clanMembers_2Q8G0LPU3 SET playerJSON = ?, iteration = ? WHERE playerID = ?", (playerJSON, i, playerTag)) # on update ses data  
                        conn.commit() # on enregiste les modification
                    else: #si le joueur n'etait pas dans le clan 
                        cursor.execute(f"INSERT INTO clanMembers_2Q8G0LPU3 (playerID, playerJSON, iteration) VALUES (?, ?, ?)", (playerTag, playerJSON, i )) # on entre les données dans le base de bonnée
                        conn.commit()
                        print(f"{playerData['name']} a rejoint {playerData['clan']['name']} !")
                except Exception as e:
                    traceback.print_exc()
            cursor.execute(f"SELECT * FROM clanMembers_2Q8G0LPU3 WHERE iteration != ?", (i, ))
            for row in cursor.fetchall():
                playerData = row[1] # on recupere le playerJSON du joueur
                print(f"{playerData['name']} a quitter le clan {playerData['clan']['name']} !")
                cursor.execute(f"DELETE FROM clanMembers_2Q8G0LPU3 WHERE playerID = ?", (playerData['tag'], )) # on retire le joueur de la db 
        except: 
            cursor.execute(f"CREATE TABLE clanMembers_2Q8G0LPU3 (playerID TEXT, playerJSON TEXT, iteration INTEGER)")
            conn.commit()
            for stat in member: # pour chaque membre
                try:
                    playerTag = stat['tag'] # on recupere le tag des membre
                    playerID = playerTag[1:] # on retire le hastag
                    responsePlayer = requests.get(url=f'https://api.clashofclans.com/v1/players/%23{playerID}', headers=clanHeader) #on recupere les info des joueurs
                    time.sleep(1)
                    # on recupere les donnée pour la database
                    player_json = responsePlayer.json()
                    playerJSON = json.dumps(player_json)
                    playerData = json.loads(playerJSON)
                    cursor.execute(f"INSERT INTO clanMembers_2Q8G0LPU3 (playerID, playerJSON, iteration) VALUES (?, ?, ?)", (playerTag, playerJSON, i ))
                    conn.commit()
                except Exception as e:
                    traceback.print_exc()

    except Exception as e:
        traceback.print_exc()
        



def syncroClan():
    innitUpdateDB()
    cursor.execute("SELECT * FROM clanMembers_2Q8G0LPU3")
    for player in cursor.fetchall():
        playerData = json.loads(player[1])
