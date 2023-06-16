import requests
import json
import time
import random
import string
import sqlite3
import time
import datetime

searchClanHeader = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImVjNWVkODY2LWVmMzctNDZjYi1hOTM4LWUzMWFlMmE3YjhhMCIsImlhdCI6MTY4NjQxNDM2Nywic3ViIjoiZGV2ZWxvcGVyLzc4ZjdjMzM2LWM2NjUtYzdmYi0xYzhkLTE0YjlhZTY4NjEwMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgxLjY0LjI1NS4xMTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.J_1HMMjTeUzEndQ30VTCP582vqH6rpnQw01qdIsM6I9RZ0HWOiZw9wtvlhdePfvnUHvwAKGv8Ql3rCoBR80S2Q'
}

searchPlayerHeader = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijk5ZmU5NmUxLWRjODktNGM2Zi05Mjg0LTg2OTFmOGRhYjUyNCIsImlhdCI6MTY4NjQxNDM5MCwic3ViIjoiZGV2ZWxvcGVyLzc4ZjdjMzM2LWM2NjUtYzdmYi0xYzhkLTE0YjlhZTY4NjEwMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgxLjY0LjI1NS4xMTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.pDhhspnsGDlUY1I-xkNVVOmGznFgoL-rgTZQmHTzIN1GEMalK5MzAId3tlutSDwDsJqKmFjr54FOkenDaTgCCQ'
}

class Clan:
    def __init__(self) -> None:
        pass

    def GenerateClanId(self):
        # génération de des ID de clan 
        characters = string.ascii_letters + string.digits # Chiffres et lettres
        characters = characters.replace('O', '').replace('o', '')
        self.clan_id = ''.join(random.choice(characters) for i in range(9)) # genereation de l'ID
        self.clan_id = self.clan_id.upper() # on met toutes les lettres de l'ID en majuscule 

conn = sqlite3.connect('CocPlayer.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 

clanInfo = Clan() # inctanciation 


while 1:
    
    url = "https://api.clashofclans.com/v1/clans?locationId=32000087&limit=21" 
    response = requests.get(url, headers=searchClanHeader) # envoie de la requete a l'API
    clan_json = response.json() # on convertit la reponse au format JSON
    clan_json = json.dumps(clan_json) # convertit la reponse au format JSON
    clan_json = json.loads(clan_json) # convertit une chaîne de caractères JSON en une structure de données Python afin de pouvoir accéder et manipuler les données JSON 
    clan_list = clan_json['items']
    for clans in clan_list:
        print(clans['name'], clans['tag'])
        clan_tag = clans['tag'] # ID du clan
        clanID = clan_tag[1:] # on retire le hastag
        url = f"https://api.clashofclans.com/v1/clans/%23{clanID}" 
        response = requests.get(url, headers=searchClanHeader) # envoie de la requete a l'API 
        time.sleep(1)
        clan = response.json() # on convertit la reponse au format JSON
        clan = json.dumps(clan) # convertit la reponse au format JSON
        clan = json.loads(clan) # convertit une chaîne de caractères JSON en une structure de données Python afin de pouvoir accéder et manipuler les données JSON
        member = clan['memberList'] # on recupere la liste des membre
        for stat in member: # pour chaque membre
            playerId = stat['tag'] # on recupere le tag des membre
            cursor.execute('SELECT tag_du_joueur FROM Player WHERE tag_du_joueur = ?', (playerId,)) # on recherche si il y a deja ce clan dans la base de donnée 
            resultat = cursor.fetchone() # on recupere les donnée
            if resultat == None: # si il n'y a pas deja le ce clan dans la base de donnée 
                playerTag = playerId[1:] # on retire le hastag
                urlPlayer = f'https://api.clashofclans.com/v1/players/%23{playerTag}'
                responsePlayer = requests.get(urlPlayer, headers=searchPlayerHeader) #on recupere les info des joueurs
                time.sleep(1)
                # on recupere les donnée pour la database
                player_json = responsePlayer.json()
                player_json = json.dumps(player_json)
                player_json= json.loads(player_json)
                playerAchievements = player_json['achievements']
                playerTotalDonnation = playerAchievements[14]
                playerTotalJDCPoint = playerAchievements[31]
                playerClanID = player_json['clan']
                playerLabels = player_json['labels']
                # verifie le nombre de labels pour eviter les erreures
                if len(playerLabels) == 3:
                    playerLabels1 = playerLabels[0]
                    playerLabels1 = playerLabels1['name']
                    playerLabels2 = playerLabels[1]
                    playerLabels2 = playerLabels2['name']
                    playerLabels3 = playerLabels[2]
                    playerLabels3 = playerLabels3['name']
                elif len(playerLabels) == 2:
                    playerLabels1 = playerLabels[0]
                    playerLabels1 = playerLabels1['name']
                    playerLabels2 = playerLabels[1]
                    playerLabels2 = playerLabels2['name']
                    playerLabels3 = None
                elif len(playerLabels) == 1:
                    playerLabels1 = playerLabels[0]
                    playerLabels1 = playerLabels1['name']
                    playerLabels2 = None
                    playerLabels3 = None 
                else:
                    playerLabels1 = None
                    playerLabels2 = None
                    playerLabels3 = None                
                cursor.execute('INSERT INTO Player (hdv, nom, tag_du_joueur, trophée, lvl, étoileDeGuerre, PréferenceDeGuerre, donnationTotal, pointsJDCTotal, label1, label2, label3, clanID, dateDeModification) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (player_json['townHallLevel'], player_json['name'], player_json['tag'], player_json['trophies'], player_json['expLevel'], player_json['warStars'], player_json['warPreference'], playerTotalDonnation['value'], playerTotalJDCPoint['value'], playerLabels1, playerLabels2, playerLabels3, playerClanID['tag'], str(datetime.datetime.now()))) # on place toutes les donné dans la base de donnée
                print(resultat, 'insert', player_json['townHallLevel'], player_json['name'], player_json['tag'], player_json['trophies'], player_json['expLevel'], player_json['warStars'], player_json['warPreference'], playerTotalDonnation['value'], playerTotalJDCPoint['value'], playerLabels1, playerLabels2, playerLabels3, playerClanID['tag'], str(datetime.datetime.now())) # on affiche dans le terminale les log 
                conn.commit() # on enregistre les modification de la data base 
            else: # si le tag du joueur existe deja dans la base de donnée , on update toutes les data
                playerId = stat['tag']
                playerTag = playerId[1:]
                urlPlayer = f'https://api.clashofclans.com/v1/players/%23{playerTag}'
                responsePlayer = requests.get(urlPlayer, headers=searchPlayerHeader)
                time.sleep(1)
                player_json = responsePlayer.json()
                player_json = json.dumps(player_json)
                player_json= json.loads(player_json)
                playerAchievements = player_json['achievements']
                playerTotalDonnation = playerAchievements[14]
                playerTotalJDCPoint = playerAchievements[31]
                playerClanID = player_json['clan']
                playerLabels = player_json['labels']
                if len(playerLabels) == 3:
                    playerLabels1 = playerLabels[0]
                    playerLabels1 = playerLabels1['name']
                    playerLabels2 = playerLabels[1]
                    playerLabels2 = playerLabels2['name']
                    playerLabels3 = playerLabels[2]
                    playerLabels3 = playerLabels3['name']
                elif len(playerLabels) == 2:
                    playerLabels1 = playerLabels[0]
                    playerLabels1 = playerLabels1['name']
                    playerLabels2 = playerLabels[1]
                    playerLabels2 = playerLabels2['name']
                    playerLabels3 = None
                elif len(playerLabels) == 1:
                    playerLabels1 = playerLabels[0]
                    playerLabels1 = playerLabels1['name']
                    playerLabels2 = None
                    playerLabels3 = None 
                else:
                    playerLabels1 = None
                    playerLabels2 = None
                    playerLabels3 = None                
                cursor.execute('UPDATE Player SET hdv = ?, nom = ?, tag_du_joueur = ?, trophée = ?, lvl = ?, étoileDeGuerre = ?, PréferenceDeGuerre = ?, donnationTotal = ?, pointsJDCTotal = ?, label1 = ?, label2 = ?, label3 = ?, clanID = ?, dateDeModification = ? WHERE tag_du_joueur = ?', (player_json['townHallLevel'], player_json['name'], player_json['tag'], player_json['trophies'], player_json['expLevel'], player_json['warStars'], player_json['warPreference'], playerTotalDonnation['value'], playerTotalJDCPoint['value'], playerLabels1, playerLabels2, playerLabels3, playerClanID['tag'], str(datetime.datetime.now()), player_json['tag']))
                print(resultat,'update',player_json['townHallLevel'], player_json['name'], player_json['tag'], player_json['trophies'], player_json['expLevel'], player_json['warStars'], player_json['warPreference'], playerTotalDonnation['value'], playerTotalJDCPoint['value'], playerLabels1, playerLabels2, playerLabels3, playerClanID['tag'], str(datetime.datetime.now())) 
                conn.commit()