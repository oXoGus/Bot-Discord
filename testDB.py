import sqlite3
from trpData import clanMembersDB 
import time
import requests, json
from trpData import betterTroops, trpRoseFR, enginDeSiegeAPI, trpRoseAPI, clanMembersDB, emojiTrpRoseFR, superToopsAPI, trpNoirFR, emojiTrpNoirFR , trpNoirAPI, hdvPNG, sortAPI, sortDataFR , emojiSortFR, laboPNG, herosAPI, hérosFR, emojiHero, ligueAPI, emojiFamillier, famillierAPI, herosthumbnail, emojiLabo, herostemoji, labelsEmoji, clanType, ligueLDC
from config import TOKEN, GDCBotheader, laboHeader, clanHeader, infoGeneraleHeader

conn = sqlite3.connect('test.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 


while True:
    try:
        cursor.execute(f"SELECT * FROM clanMembers_2Q8G0LPU2")
        resp = requests.get(url=f"https://api.clashofclans.com/v1/clans/%232Q8G0LPU0", headers=clanHeader)
        resp.raise_for_status() 
        print('A')
        resp = resp.json()
        clan = json.dumps(resp)
        clanJSON = json.loads(clan)
        member = clanJSON['memberList'] # on recupere la liste des membre
        for stat in member: # pour chaque membre
            try:
                playerTag = stat['tag'] # on recupere le tag des membre
                playerID = playerTag[1:] # on retire le hastag
                responsePlayer = requests.get(url=f'https://api.clashofclans.com/v1/players/%23{playerID}', headers=clanHeader) #on recupere les info des joueurs
                time.sleep(1)
                responsePlayer.raise_for_status()
                # on recupere les donnée pour la database
                player_json = responsePlayer.json()
                print(player_json)
                player_json = json.dumps(player_json)
                playerData= json.loads(player_json)
                playerJSON = json.dumps(playerData)
                cursor.execute(f"UPDATE clanMembers_2Q8G0LPU2 SET playerJSON = ? WHERE playerID = ?", (playerJSON, playerData['tag']))
                conn.commit()

            except Exception as e:
                print(e)
    except:
        cursor.execute(f"CREATE TABLE clanMembers_2Q8G0LPU2 (playerID TEXT, playerJSON TEXT)")
        conn.commit()
        resp = requests.get(url=f"https://api.clashofclans.com/v1/clans/%232Q8G0LPU0", headers=clanHeader)
        resp.raise_for_status() 

        resp = resp.json()
        clan = json.dumps(resp)
        clanJSON = json.loads(clan)
        member = clanJSON['memberList'] # on recupere la liste des membre
        for stat in member: # pour chaque membre
            try:
                playerTag = stat['tag'] # on recupere le tag des membre
                playerID = playerTag[1:] # on retire le hastag
                responsePlayer = requests.get(url=f'https://api.clashofclans.com/v1/players/%23{playerID}', headers=clanHeader) #on recupere les info des joueurs
                time.sleep(1)
                # on recupere les donnée pour la database
                player_json = responsePlayer.json()
                player_json = json.dumps(player_json)
                playerData = json.loads(player_json)
                playerJSON = json.dumps(playerData)
                cursor.execute(f"INSERT INTO clanMembers_2Q8G0LPU2 (playerID, playerJSON) VALUES (?, ?)", (playerData['tag'], playerJSON,))
                conn.commit()
            except Exception as e:
                print(e)
