import json
import sqlite3
from random import random
import discord
import interactions
import requests
from discord.ext import commands
from interactions import (Button, ButtonStyle, OptionType, SlashContext, ActionRow, StringSelectMenu, CustomEmoji, Embed, PartialEmoji,Intents, listen, slash_command, slash_option)
from interactions.api.events import Component
from interactions.ext.paginators import Paginator
from datetime import datetime, timezone
from dateutil import parser
import traceback
from interactions import slash_command, SlashContext, Modal, ShortText, ParagraphText, slash_channel_option
import time
import asyncio
import math
from config import TOKEN, GDCBotheader, laboHeader, clanHeader, infoGeneraleHeader
from trpData import betterTroops, trpRoseFR, enginDeSiegeAPI, trpRoseAPI, clanMembersDB, emojiTrpRoseFR, superToopsAPI, trpNoirFR, emojiTrpNoirFR , trpNoirAPI, hdvPNG, sortAPI, sortDataFR , emojiSortFR, laboPNG, herosAPI, hérosFR, emojiHero, ligueAPI, emojiFamillier, famillierAPI, herosthumbnail, emojiLabo, herostemoji, labelsEmoji, clanType, ligueLDC

conn = sqlite3.connect('test.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 


async def UpdateDB(channel:interactions.TYPE_MESSAGEABLE_CHANNEL, clanJSON, clanID):
    i = random.random() 
    try:
        member = clanJSON['memberList'] # on recupere la liste des membre
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
                cursor.execute(f"SELECT * FROM clanMembers_{clanID} WHERE playerID = ?", (playerTag, )) # si le joueur etait deja dans le clan 
                if cursor.fetchone() is not None:
                    cursor.execute(f"UPDATE clanMembers_{clanID} SET playerJSON = ?, iteration = ? WHERE playerID = ?", (playerJSON, i, playerTag)) # on update ses data  
                    conn.commit() # on enregiste les modification
                else: #si le joueur n'etait pas dans le clan 
                    cursor.execute(f"INSERT INTO clanMembers_{clanID} (playerID, playerJSON, iteration) VALUES (?, ?, ?)", (playerTag, playerJSON, i )) # on entre les données dans le base de bonnée
                    conn.commit()
                    joinEmbed = Embed(title=f"{playerData['name']} a rejoint le clan !", thumbnail=hdvPNG[playerData['townHallLevel']-1], description=f"<:exp:1137420369259675669>{ playerData['expLevel']} | <:tr:1137414233693376632> {playerData['trophies']} | :star: {playerData['warStars']}")
                    await channel.send(content=f"", embed=joinEmbed)
                    print(f"{playerData['name']} a rejoint {playerData['clan']['name']} !")
            except Exception:
                traceback.print_exc()
        cursor.execute(f"SELECT * FROM clanMembers_{clanID} WHERE iteration != ?", (i, ))
        for row in cursor.fetchall():
            playerData = row[1] # on recupere le playerJSON du joueur
            print(f"{playerData['name']} a quitter le clan {playerData['clan']['name']} !")
            cursor.execute(f"DELETE FROM clanMembers_{clanID} WHERE playerID = ?", (playerData['tag'], )) # on retire le joueur de la db 

    except Exception:
        traceback.print_exc()
        

def insertPlayerBD(clanJSON, clanID):
    i = random.random(1001)
    cursor.execute(f"CREATE TABLE clanMembers_{clanID} (playerID TEXT, playerJSON TEXT, iteration INTEGER)")
    conn.commit()
    resp = requests.get(url=f"https://api.clashofclans.com/v1/clans/%23{clanID}", headers=clanHeader)
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
            playerJSON = json.dumps(player_json)
            playerData = json.loads(playerJSON)
            cursor.execute(f"INSERT INTO clanMembers_{clanID} (playerID, playerJSON, iteration) VALUES (?, ?, ?)", (playerTag, playerJSON, i ))
            conn.commit()
        except : 
            traceback.print_exc()
    return member, clan

def clanRequests(clanID):
    resp = requests.get(url=f"https://api.clashofclans.com/v1/clans/%232Q8G0LPU0", headers=clanHeader)
    resp.raise_for_status()
    resp = resp.json()
    clan = json.dumps(resp)
    clanJSON = json.loads(clan)
    return clanJSON


@slash_command(name= 'syncro_clan', description = 'syncroniser un clan a un channel')
@slash_option(name= 'channel', description='channel', required=True, opt_type=OptionType.CHANNEL)
@slash_option(name= 'tag', description='tag', required=True, opt_type=OptionType.STRING)
async def syncroClan(ctx : SlashContext ,channel:interactions.TYPE_MESSAGEABLE_CHANNEL, clanTag):
    clanID = clanTag[1:]
    try:
        resp = requests.get(url=f"https://api.clashofclans.com/v1/clans/%232Q8G0LPU0", headers=clanHeader)
        resp.raise_for_status()
        resp = resp.json()
        clan = json.dumps(resp)
        clanJSON = json.loads(clan)
    except:
        return "le tag du clan est ivalide !"
    
    try :
        cursor.execute(f"SELECT * FROM clanMembers_{clanID}") #on cherche si la table existe deja (exeption si la table n'existe pas)
    except:
        insertPlayerBD(clanJSON, clanID)
    UpdateDB(channel, clanJSON, clanID)
    
    
    

    while True:
        previewPlayerData = []
        cursor.execute(f"SELECT * FROM clanMembers_{clanID}")
        for player in cursor.fetchall():
            previewPlayerData.append(json.loads(player[1]))

        clanJSON = clanRequests(clanID)

        nextPlayerData = []
        member = clanJSON['memberList'] # on recupere la liste des membre
        for stat in member: # pour chaque membre
            playerID = stat['tag'][1:] # on retire le hastag
            responsePlayer = requests.get(url=f'https://api.clashofclans.com/v1/players/%23{playerID}', headers=clanHeader) #on recupere les info des joueurs
            time.sleep(1)            # on recupere les donnée pour la database
            player_json = responsePlayer.json()
            playerJSON = json.dumps(player_json)
            nextPlayerData.append(json.loads(playerJSON))

        for n in len(previewPlayerData):
            if previewPlayerData[n][...] != nextPlayerData[n][...]:
                channel.send("message")
        """
        faire pour tout ce qui peut etre amélorer 
        """
        UpdateDB(channel, clanJSON, clanID)
        

    






syncroClan(clanTag="#2Q8G0LPU3")
