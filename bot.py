import json
import sqlite3
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

# todo: faire while currentwar == inwar ... et pereil pour les autre status

conn = sqlite3.connect('CocPlayer.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 


bot = interactions.Client(token=TOKEN, intents=Intents.ALL) # crée le bot



################################################
#
#       message when the bot is ready
#
################################################




@listen()
async def on_ready(): # quand le bod est pret 
    print(f'{bot.user} est en marche') #afficher ceci dans le terminal
    
###############################################

#       search command

###############################################

@slash_command(name = 'recherchejoueur', description = "rechercher des joueur selon leurs stats") # on crée une commande et on initialiser sont nom et sa description 
async def rechercheJoueur(ctx): # la fonction qui est rattacher a cette commande 
    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.BLURPLE, label='les joueurs ayant le plus de trophée', custom_id="trophy", ), Button(style=ButtonStyle.BLURPLE, label='les plus actifs dans les jeux de clans', custom_id="jdc"), Button(style=ButtonStyle.BLURPLE, label='les joueur dans un clan français ayant donné le plus de troupes', custom_id="don"))] #on crée la partie interactive du message 
    await ctx.send('selectionner les statistiques que vous désirer' , components=components) # on definis le contenue du message et on rattache la partie interactive du message 





################################################
#
#       currentwar commands
#
################################################


@slash_command(name='gdc', description="visualiser la gdc dun clan")
@slash_option(name='id', description='le tag du clan', required=True, opt_type=OptionType.STRING)
async def gdc(ctx : SlashContext, id):
    channel = ctx.channel
    id=id[1:]
    url = f"https://api.clashofclans.com/v1/clans/%23{id}/currentwar"
    while True:
        try:
            

            response = requests.get(url, headers=GDCBotheader) 
            currentwar = response.json()  
            currentwar = json.dumps(currentwar)
            currentwar = json.loads(currentwar)


            if currentwar['state'] == 'notInWar': # si le clan n'est pas dans une guerre 
                await ctx.send(content="Ce clan n'est actuellement pas en guerre ! refaite la commande quand le clan aura trouver une guerre.")# on met l'embed dans une variable pour le modifier
                break

            
            # on recupere toutes les informations sur le clan
            clanInfo = currentwar['clan']
            clanMemberInfo = clanInfo['members']
            clanMemberInfo = sorted(clanMemberInfo, key= lambda x : x['mapPosition'])# on ordonne les joueurs de la guerre en fonction de leur position dans la guerre
            # on recupere toutes les informations sur le clan
            opponentInfo = currentwar['opponent'] 
            opponentMemberInfo = opponentInfo['members']
            opponentMemberInfo = sorted(opponentMemberInfo, key= lambda x : x['mapPosition'])# on ordonne les joueurs de la guerre en fonction de leur position dans la guerre
            

            if currentwar['state'] == 'preparation': # si le clan est en preparation  
                await channel.send(content=f"**La guerre a été déclarée contre [{opponentInfo['name']}](https://www.clashofstats.com/clans/{opponentInfo['name']}-{opponentInfo['tag']}/members/) !**")     
                prepartionMessage = await channel.send(content='tkt')
            

            while currentwar['state'] == 'preparation':
                starTime = currentwar['startTime']
                starTime = parser.parse(starTime)
                timestampStartTime = f"<t:{int(starTime.timestamp())}:R>"
                preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre commence** {timestampStartTime}",  inline=False)
                await prepartionMessage.edit(embed=preparationEmbed)
                await asyncio.sleep(60)
                response = requests.get(url, headers=GDCBotheader) 
                currentwar = response.json()  
                currentwar = json.dumps(currentwar)
                currentwar = json.loads(currentwar)

            if currentwar['state'] == 'inWar': # si le clan est dans une guerre 
                endTime = currentwar['endTime']
                endTime = parser.parse(endTime)
                timestampEndTime = f"<t:{int(endTime.timestamp())}:R>"
                try:
                    preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                    preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                    preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine** {timestampEndTime}",  inline=False)
                    await prepartionMessage.edit(embed=preparationEmbed)
                except Exception :
                    preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                    preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                    preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine** {timestampEndTime}",  inline=False)
                    prepartionMessage = await channel.send(embed=preparationEmbed)


                
                messID=[]
                for jsp in range(int(currentwar['teamSize']/5)):
                    warMessage = await channel.send(content='.')
                    messID.append(warMessage)
                    print(messID)      
  
            while currentwar['state'] == 'inWar':
                endTime = currentwar['endTime']
                endTime = parser.parse(endTime)
                timestampEndTime = f"<t:{int(endTime.timestamp())}:R>"
                preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine** {timestampEndTime}",  inline=False)
                await prepartionMessage.edit(embed=preparationEmbed)
                

                for a in range(int(currentwar['teamSize']/5)):
                    clanValue=""
                    opponentValue =""
                    embeds = Embed(color=interactions.Color.from_rgb(255, 128, 0))
                    for i in range(5):
                        i = i + a * 5
                        try:
                            for z in range(len(opponentMemberInfo)):
                                if opponentMemberInfo[z]['tag'] == clanMemberInfo[i]['bestOpponentAttack']['attackerTag']:
                                    opponentMemberInfodef = opponentMemberInfo[z]['mapPosition']
                                    opponentMemberInfodefName = opponentMemberInfo[z]['name']
                                    break
                            try:
                                clanValue = clanValue + "**{}. {}** {}  {} \n\n".format(
                                    clanMemberInfo[i]['mapPosition'],
                                    clanMemberInfo[i]['name'],
                                    ("" if len(clanMemberInfo[i]['attacks']) == 2 else ":crossed_swords:" ),
                                    "{}. {} :star::star::star:".format(
                                        opponentMemberInfodef,
                                        opponentMemberInfodefName
                                    ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                        "{}. {} :star::star:".format(
                                            opponentMemberInfodef,
                                            opponentMemberInfodefName
                                        ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                            "{}. {} :star:".format(
                                                opponentMemberInfodef,
                                                opponentMemberInfodefName
                                            ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else 
                                            "{}. {}: 0 étoile".format(
                                                    opponentMemberInfodef,
                                                    opponentMemberInfodefName
                                            )
                                        )
                                    )
                                )
                            except Exception: 
                                clanValue = clanValue + "**{}. {} :crossed_swords::crossed_swords: ** {} \n\n".format(
                                    clanMemberInfo[i]['mapPosition'],
                                    clanMemberInfo[i]['name'],
                                    "{}. {} :star::star::star:".format(
                                        opponentMemberInfodef,
                                        opponentMemberInfodefName
                                    ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                        "{}. {} :star::star:".format(
                                            opponentMemberInfodef,
                                            opponentMemberInfodefName
                                        ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                            "{}. {} :star:".format(
                                                opponentMemberInfodef,
                                                opponentMemberInfodefName
                                            ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else 
                                            "{}. {}: 0 étoile".format(
                                                    opponentMemberInfodef,
                                                    opponentMemberInfodefName
                                            )
                                        )
                                    )
                                )
                        except Exception:
                            try:
                                clanValue = clanValue + f"**{clanMemberInfo[i]['mapPosition']}. {clanMemberInfo[i]['name']} {'' if len(clanMemberInfo[i]['attacks']) == 2 else ':crossed_swords:' }** n'a pas encore été attaqué\n\n"
                            except Exception:
                                clanValue = clanValue + f"**{clanMemberInfo[i]['mapPosition']}. {clanMemberInfo[i]['name']} :crossed_swords::crossed_swords:** n'a pas encore été attaqué \n\n"

                        try:
                            for z in range(len(clanMemberInfo)):
                                if clanMemberInfo[z]['tag'] == opponentMemberInfo[i]['bestOpponentAttack']['attackerTag']:
                                    opponentMemberInfodef = clanMemberInfo[z]['mapPosition']
                                    opponentMemberInfodefName = clanMemberInfo[z]['name']
                                    break
                            try : 
                                opponentValue = opponentValue + " **{}. {} {}** {} \n\n".format(
                                    opponentMemberInfo[i]['mapPosition'],
                                        opponentMemberInfo[i]['name'], 
                                            ("" if len(opponentMemberInfo[i]['attacks']) == 2 else ":crossed_swords:" ), 
                                        "{}. {}: :star::star::star:".format(
                                            opponentMemberInfodef,
                                            opponentMemberInfodefName
                                        ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                            "{}. {}: :star::star:".format(
                                                opponentMemberInfodef,
                                                opponentMemberInfodefName
                                            ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                                "{}. {}: :star:".format(
                                                    opponentMemberInfodef,
                                                    opponentMemberInfodefName
                                                ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else
                                                "{}. {}: 0 étoile".format(
                                                    opponentMemberInfodef,
                                                    opponentMemberInfodefName
                                                )
                                            )
                                        )
                                    )
                            except Exception: 
                                opponentValue = opponentValue + " **{}. {} :crossed_swords::crossed_swords:** {} \n\n".format(
                                    opponentMemberInfo[i]['mapPosition'],
                                        opponentMemberInfo[i]['name'], 

                                        "{}. {}: :star::star::star:".format(
                                            opponentMemberInfodef,
                                            opponentMemberInfodefName
                                        ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                            "{}. {}: :star::star:".format(
                                                opponentMemberInfodef,
                                                opponentMemberInfodefName
                                            ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                                "{}. {}: :star:".format(
                                                    opponentMemberInfodef,
                                                    opponentMemberInfodefName
                                                ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else
                                                "{}. {}: 0 étoile".format(
                                                    opponentMemberInfodef,
                                                    opponentMemberInfodefName
                                                )
                                            )
                                        )
                                    )
                        except Exception : 
                            try:
                                opponentValue = opponentValue + f" **{opponentMemberInfo[i]['mapPosition']}. {opponentMemberInfo[i]['name']} {'' if len(opponentMemberInfo[i]['attacks']) == 2 else ':crossed_swords:' }** n'a pas encore été attaqué\n\n"
                            except Exception:
                                opponentValue = opponentValue + f" **{opponentMemberInfo[i]['mapPosition']}. {opponentMemberInfo[i]['name']} :crossed_swords::crossed_swords:** n'a pas encore été attaqué\n\n"
                    embeds.add_field(name='votre clan' , value=clanValue , inline=True)
                    print(clanValue) 
                    embeds.add_field(name='le clan adverse', value=opponentValue, inline=True )
                    print(opponentValue)
                    try : 
                        await messID[a].edit(content='',embed=embeds)
                    except Exception: # si on ne peut pas modifier le message parce que les 15 minute apres l'envoie du message sont passé
                        for e in range(len(messID)): # on supprime tout les messages qui ont été envoyées
                            await messID[e].delete()
                        messID=[] # on reinisialise la liste des messages 
                        for jsp in range(int(currentwar['teamSize']/5)): # on réenvoie les messages
                            warMessage = await channel.send(content='yo !')
                            messID.append(warMessage)


                await asyncio.sleep(60)
                response = requests.get(url, headers=GDCBotheader) 
                currentwar = response.json()  
                currentwar = json.dumps(currentwar)
                currentwar = json.loads(currentwar)
                
                if currentwar['state'] == 'warEnded':
                    warEndedEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                    warEndedEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                    warEndedEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + {'\nVous avez gagnée le guerre' if a == 1 else "z"},  inline=False)
                    warEndedMessage = await channel.send(embed=warEndedEmbed)
                while currentwar['state'] == 'warEnded':
                    pass


            
            
                           
        except Exception:
            traceback.print_exc()
            await ctx.send('veuiller reessayer plus tard')
            break



@slash_command(name = 'pa', description = "afficher les stats d'un joueur")
async def pa(ctx: SlashContext):
    channel = ctx.channel
    for emoji in await ctx.guild.fetch_all_custom_emojis():
        print(f"<:{emoji.name}:{emoji.id}>")
    embed = Embed(title="stats du joueur", color=interactions.Color.from_rgb(255, 128, 0))
    try:
        messID=[]
        for jsp in range(4):
            warMessage = await channel.send(content=f"<:p_:1136624579314450523>")
            messID.append(warMessage)
        print(messID)
        for i in range(4):
            await messID[i].edit(content='',embed=embed)
            print(messID[i])
        for i in range(4):
            await messID[i].delete()
        

    except Exception:
        traceback.print_exc()
  


################################################
#
#        coc profile command
#
################################################


# todo : faire plusieur embed(labo, info géneral, son clan)
# todo : faire en sorte que l'on fasse uniquement 2 requete a l'api lorsqu'on effectue la commande 
# todo : une fois que la commande a été effectuer on evoie l'embed info géneral avec trois boutons (info géneral, labo, son clan) 
# todo : quand on appuis sur ses boutons on modifit le message initale par l'embed correspondant


@slash_command(name = 'p', description = "afficher les stats d'un joueur")
@slash_option(name = 'tag', description="tag du joueur", required=True, opt_type=OptionType.STRING )
async def p(ctx : SlashContext, tag : str) :
        tag = tag[1:]
        try:    
            url = f"https://api.clashofclans.com/v1/players/%23{tag}"
            response = requests.get(url, headers=infoGeneraleHeader)
            user_json = response.json()
            user_json = json.dumps(user_json)
            user = json.loads(user_json) 
            embed_profile = Embed(title=f"info génerale du joueur {user['tag']}", description=f"**psedo du joueur : {user['name']}**", color=interactions.Color.random(), timestamp=datetime.now())
            embed_profile.add_field(name="nombre de trophées du joueur :", value=f"{user['trophies']} {ligueAPI[user['league']['name']]}", inline=True)
            embed_profile.add_field(name="nombre d'etoiles de guerre :", value=f"{user['warStars']} <:st:1138557349913706616>", inline=True)
            CWLTotal = sorted(user['achievements'], key=lambda x : x['name'] != "War League Legend")[0]
            embed_profile.add_field(name="nombre d'étoiles gagnée pendant les ligue de clans :", value=f"{CWLTotal['value']} <:st:1138557349913706616>", inline=True)
            embed_profile.add_field(name=f"nombre d'attaque gagnée cette saison : {user['attackWins']} <:cc:1138557308083908648>", value=f" ", inline=True)
            combatTotal = sorted(user['achievements'], key=lambda x : x['name'] != "Conqueror")[0]
            embed_profile.add_field(name="nombre de combat gagnée au total :", value=f"{combatTotal['value']} <:cc:1138557308083908648>", inline=True)
            embed_profile.add_field(name="nombre de défense gagnée cette saison :", value=f"{user['defenseWins']} <:cc:1138557308083908648>", inline=True)
            try:
                embed_profile.add_field(name="rôle dans son clan :", value="{}".format("chef" if user['role'] =="leader" else("chef adjoint" if user['role'] == "coLeader" else ("ainé" if user['role'] == "admin" else "membre"))), inline=True)
            except Exception:
                embed_profile.add_field(name="rôle dans son clan :", value="n'est actuellement pas dans un clan")
            embed_profile.add_field(name="préference de guerre :", value=f"{'<:yy:1137489567973388348>' if user['warPreference'] == 'in' else '<:nn:1137489472989188276>'}", inline=True)
            embed_profile.add_field(name=f"nombre de troupe donnée cette saison : {user['donations']} <:dd:1138557463851962509>", value=f" ", inline=True)
            embed_profile.add_field(name="nombre de troupe recu cette saison :", value=f"{user['donationsReceived']} <:dd:1138557463851962509>", inline=True)      
            embed_profile.add_field(name="contribution a la capitale de clan :", value=f"{user['clanCapitalContributions']} <:jj:1137489208232124476>", inline=True)  
            embed_profile.add_field(name="niveau d'hotel de ville :", value=f"{user['townHallLevel']}", inline=True)
            embed_profile.add_field(name="{} :".format("niveau de la giga tour de l'enfer" if user['townHallLevel'] == 13 or 14 or 15 else "niveau de la giga tesla"), value=f"{user['townHallWeaponLevel']}")
            embed_profile.add_field(name="niveau du joueur :", value=f"{user['expLevel']} <:exp:1137420369259675669>", inline=True)
            jdcTotal = sorted(user['achievements'], key=lambda x : x['name'] != "Games Champion")[0]
            embed_profile.add_field(name="points aux jeux de clans totaux :", value=f"{jdcTotal['value']}", inline=True)
            try:
                text = ""
                for label in user['labels']:
                    text = text + f"{labelsEmoji[label['name']]['emoji']} {labelsEmoji[label['name']]['Fr']} | "
                embed_profile.add_field(name="les labels du joueur :", value=text, inline=False)
            except Exception:
                traceback.print_exc()

            embed_profile.set_thumbnail(url=hdvPNG[user['townHallLevel']-1]['th'][user['townHallWeaponLevel']-1])
            embed_profile.set_footer(text=user['tag'])
            embedInfoGenerale = embed_profile.to_dict()
            try:
                user['clan']
                try:
                    user['heroes']
                    try:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                    except Exception :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
            except Exception :
                try :
                    user['heroes']
                    try :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                    except Exception:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
            await ctx.send(embed=embedInfoGenerale, components=components)
        except KeyError:
            traceback.print_exc()
            await ctx.send("Erreur : tag du joueur invalide.")
        except Exception: # si il y a une erreur qui n'est pas mentionner plus haut 
            await ctx.send("Erreur : veuillez réessayer plus tard.")
            traceback.print_exc()


def fillclanMembersDB(clanJSON):
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
            playerData= json.loads(player_json)
            playerName = playerData['name']
            playerRole = stat['role']
            playerExp = playerData['expLevel']
            trophiesLeagueID = playerData['league']['id']
            etoilesDeGuerre = playerData['warStars']
            preferenceDeGuerre = playerData['warPreference']
            troops = playerData['troops']
            spells = playerData['spells']
            heroes = playerData['heroes']
            trpRose = []
            for i in range(len(trpRoseAPI)):
                if sorted(troops, key= lambda x : x['name'] != trpRoseAPI[i])[0] == trpRoseAPI[i]:
                    trpRose.append(sorted(troops, key= lambda x : x['name'] != trpRoseAPI[i])[0]['level'])
                else:
                    pass
            trpNoir = []
            for i in range(len(trpNoirAPI)):
                if sorted(troops, key= lambda x : x['name'] != trpNoirAPI[i])[0] == trpNoirAPI[i]:
                    trpNoir.append(sorted(troops, key= lambda x : x['name'] != trpNoirAPI[i])[0]['level'])
                else:
                    trpNoir.append(None)
            sort = []
            for i in range(len(sortAPI)):
                if sorted(spells, key= lambda x : x['name'] != sortAPI[i])[0] == sortAPI[i]:
                    sort.append(sorted(spells, key= lambda x : x['name'] != sortAPI[i])[0]['level'])
                else:
                    sort.append(None)
            hero = []
            for i in range(len(herosAPI)):
                if sorted(heroes, key= lambda x : x['name'] != herosAPI[i])[0] == herosAPI[i]:
                    hero.append(sorted(heroes, key= lambda x : x['name'] != herosAPI[i])[0]['level'])
                else:
                    hero.append(None)
            superTroops = []
            for i in range(len(superToopsAPI)):
                if sorted(troops, key= lambda x : x['name'] != superToopsAPI[i])[0] == superToopsAPI[i]:
                    try :
                        superTroops.append(sorted(troops, key= lambda x : x['name'] != superToopsAPI[i])[0]['superTroopIsActive'])
                    except Exception :
                        superTroops.append("false")
                else:
                    superTroops.append(None)
            enginDeSieges = []
            for i in range(len(enginDeSiegeAPI)):
                if sorted(troops, key= lambda x : x['name'] != enginDeSiegeAPI[i])[0] == enginDeSiegeAPI[i]:
                    enginDeSieges.append(sorted(troops, key= lambda x : x['name'] != enginDeSiegeAPI[i])[0]['level'])
                else:
                    superTroops.append(None)
            familliers = []
            for i in range(len(famillierAPI)):
                if sorted(heroes, key= lambda x : x['name'] != famillierAPI[i])[0] == famillierAPI[i]:
                    hero.append(sorted(heroes, key= lambda x : x['name'] != famillierAPI[i])[0]['level'])
                else:
                    hero.append(None)
            cursor.execute(f"INSERT INTO clanMembers{clanJSON['tag']} ({clanMembersDB[0]}, {clanMembersDB[1]}, {clanMembersDB[2]}, {clanMembersDB[3]}, {clanMembersDB[4]}, {clanMembersDB[5]}, {clanMembersDB[6]}, {clanMembersDB[7]}, {clanMembersDB[8]}, {clanMembersDB[9]}, {clanMembersDB[10]}, {clanMembersDB[11]}, {clanMembersDB[12]}, {clanMembersDB[13]}, {clanMembersDB[14]}, {clanMembersDB[15]}, {clanMembersDB[16]}, {clanMembersDB[17]}, {clanMembersDB[18]}, {clanMembersDB[19]}, {clanMembersDB[20]}, {clanMembersDB[21]}, {clanMembersDB[22]}, {clanMembersDB[23]}, {clanMembersDB[24]}, {clanMembersDB[25]}, {clanMembersDB[26]}, {clanMembersDB[27]}, {clanMembersDB[28]}, {clanMembersDB[29]}, {clanMembersDB[30]}, {clanMembersDB[31]}, {clanMembersDB[32]}, {clanMembersDB[33]}, {clanMembersDB[34]}, {clanMembersDB[35]}, {clanMembersDB[36]}, {clanMembersDB[37]}, {clanMembersDB[38]}, {clanMembersDB[39]}, {clanMembersDB[40]}, {clanMembersDB[41]}, {clanMembersDB[42]}, {clanMembersDB[43]}, {clanMembersDB[44]}, {clanMembersDB[45]}, {clanMembersDB[46]}, {clanMembersDB[47]}, {clanMembersDB[48]}, {clanMembersDB[49]}, {clanMembersDB[50]}, {clanMembersDB[51]}, {clanMembersDB[52]}, {clanMembersDB[53]}, {clanMembersDB[54]}, {clanMembersDB[55]}, {clanMembersDB[56]}, {clanMembersDB[57]}, {clanMembersDB[58]}, {clanMembersDB[59]}, {clanMembersDB[60]}, {clanMembersDB[61]}, {clanMembersDB[62]}, {clanMembersDB[63]}, {clanMembersDB[64]}, {clanMembersDB[65]}, {clanMembersDB[66]}, {clanMembersDB[67]}, {clanMembersDB[68]}, {clanMembersDB[69]}, {clanMembersDB[70]}, {clanMembersDB[71]}, {clanMembersDB[72]}, {clanMembersDB[73]}, {clanMembersDB[74]}, {clanMembersDB[75]}, {clanMembersDB[76]}, {clanMembersDB[77]}, {clanMembersDB[78]}, {clanMembersDB[79]}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (playerTag, playerName, playerRole, trophiesLeagueID, etoilesDeGuerre,superToopsAPI[0], superToopsAPI[1], superToopsAPI[2], superToopsAPI[3], superToopsAPI[4], superToopsAPI[5], superToopsAPI[6], superToopsAPI[7], superToopsAPI[8], superToopsAPI[9], superToopsAPI[10], superToopsAPI[11], superToopsAPI[12], superToopsAPI[13], superToopsAPI[14], trpRoseAPI[0],  trpRoseAPI[1], trpRoseAPI[2], trpRoseAPI[3], trpRoseAPI[4], trpRoseAPI[5], trpRoseAPI[6], trpRoseAPI[7], trpRoseAPI[8], trpRoseAPI[9], trpRoseAPI[10], trpRoseAPI[11], trpRoseAPI[12], trpRoseAPI[13], trpRoseAPI[14], trpRoseAPI[15], sort[0],  sort[1],  sort[2],  sort[3],  sort[4],  sort[5], sort[6], sort[7], sort[8], sort[9], sort[10], sort[11], sort[12], trpNoir[0],  trpNoir[1], trpNoir[2], trpNoir[3], trpNoir[4], trpNoir[5], trpNoir[6], trpNoir[7], trpNoir[8], trpNoir[9], enginDeSieges[0], enginDeSieges[1], enginDeSieges[2], enginDeSieges[3], enginDeSieges[4], enginDeSieges[5], enginDeSieges[6], hero[0], hero[1], hero[2], hero[3], familliers[0], familliers[1], familliers[2], familliers[3], familliers[4], familliers[5], familliers[6], familliers[7], ))
            conn.commit()
        except Exception :
            pass



def createClanJSONFromDB(clanJSON):
    pass

@slash_command(name= 'syncro_clan', description = 'syncroniser un clan a un channel')
@slash_option(name= 'channel', description='channel', required=True, opt_type=OptionType.CHANNEL)
@slash_option(name= 'tag', description='tag', required=True, opt_type=OptionType.STRING)
async def syncoClan(ctx : SlashContext ,channel:interactions.TYPE_MESSAGEABLE_CHANNEL, tag):
    tagID = tag[1:]
    try:
        resp = requests.get(url=f"https://api.clashofclans.com/v1/clans/%23{tagID}", headers=clanHeader)
        resp.raise_for_status()
        resp = resp.json()
        clan = json.dumps(resp)
        clanJSON = json.loads(clan)
        await ctx.send(content='syncronisation éffectué')
    except Exception:
        return await ctx.send(content=f"Le clan avec l'ID : {tagID} n'existe pas ! verifier bien l'ID du clan")
    
    while True:
        cursor.execute(f"SELECT * FROM clanMembers{clanJSON['tag']}")
        if cursor.fetchone() is None :
            cursor.execute(f"CREATE TABLE clanMembers{clanJSON['tag']} (tag TEXT CHECK(LENGTH(tag) <= 20), \
                           player TEXT CHECK(LENGTH(player) <= 30), \
                           role TEXT CHECK(LENGTH(role) <= 20), \
                           expLevel INTEGER CHECK(expLevel <= 600), \
                           trophieLeague INTEGER, \
                           étoilesDeGuerre INTEGER CHECK(étoilesDeGuerre <= 10000), \
                           préferenceDeGuerre TEXT CHECK(LENGTH(préferenceDeGuerre) <= 4), \
                           RagedBarbarian TEXT CHECK(LENGTH(RagedBarbarian) <= 5), \
                           SuperArcher TEXT CHECK(LENGTH(SuperArcher) <= 5), \
                           SneakyGoblin TEXT CHECK(LENGTH(SneakyGoblin) <= 5), \
                           SuperWallBreaker TEXT CHECK(LENGTH(SuperWallBreaker) <= 5), \
                           SuperGiant TEXT CHECK(LENGTH(SuperGiant) <= 5), \
                           RocketBalloon TEXT CHECK(LENGTH(RocketBalloon) <= 5), \
                           SuperWizard TEXT CHECK(LENGTH(SuperWizard) <= 5), \
                           SuperDragon TEXT CHECK(LENGTH(SuperDragon) <= 5), \
                           InfernoDragon TEXT CHECK(LENGTH(InfernoDragon) <= 5), \
                           SuperMinion TEXT CHECK(LENGTH(SuperMinion) <= 5), \
                           SuperValkyrie TEXT CHECK(LENGTH(SuperValkyrie) <= 5), \
                           SuperWitch TEXT CHECK(LENGTH(SuperWitch) <= 5), \
                           IceHound TEXT CHECK(LENGTH(IceHound) <= 5), \
                           SuperBowler TEXT CHECK(LENGTH(SuperBowler) <= 5), \
                           SuperHogRider TEXT CHECK(LENGTH(SuperHogRider) <= 5), \
                           Barbare INTEGER CHECK(Barbare <= 35), \
                           Archer INTEGER CHECK(Archer <= 35), \
                           géant INTEGER CHECK(géant <= 35), \
                           gobelin INTEGER CHECK(gobelin <= 35), \
                           sapeur INTEGER CHECK(sapeur <= 35), \
                           ballon INTEGER CHECK(ballon <= 35), \
                           sorcier INTEGER CHECK(sorcier <= 35), \
                           guérisseuse INTEGER CHECK(guérisseuse <= 35), \
                           dragon INTEGER CHECK(dragon <= 35), \
                           P.E.K.K.A INTEGER CHECK(P.E.K.K.A <= 35), \
                           BébéDragon INTEGER CHECK(BébéDragon <= 35), \
                           mineur INTEGER CHECK(mineur <= 35), \
                           Edrag INTEGER CHECK(Edrag <= 35), \
                           yeti INTEGER CHECK(yeti <= 35), \
                           ChevaucheurDeDragon INTEGER CHECK(ChevaucheurDeDragon <= 35), \
                           éléctroTitanide INTEGER CHECK(éléctroTitanide <= 35), \
                           sortDeFoudre INTEGER CHECK(sortDeFoudre <= 35), \
                           sortDeGuérison INTEGER CHECK(sortDeGuérison <= 35), \
                           sortDeRage INTEGER CHECK(sortDeRage <= 35), \
                           sortDeSaut INTEGER CHECK(sortDeSaut <= 35), \
                           sortDeGel INTEGER CHECK(sortDeGel <= 35), \
                           sortDeClonage INTEGER CHECK(sortDeClonage <= 35), \
                           sortInvisibilité INTEGER CHECK(sortInvisibilité <= 35), \
                           sortDeRappel INTEGER CHECK(sortDeRappel <= 35), \
                           sortDePoison INTEGER CHECK(sortDePoison <= 35), \
                           sortSismique INTEGER CHECK(sortSismique <= 35), \
                           sortDePrécipitation INTEGER CHECK(sortDePrécipitation <= 35), \
                           sortSquelettique INTEGER CHECK(sortSquelettique <= 35), \
                           sortDeBat INTEGER CHECK(sortDeBat <= 35), \
                           gargouille INTEGER CHECK(gargouille <= 35), \
                           cochon INTEGER CHECK(cochon <= 35), \
                           Valkyrie INTEGER CHECK(Valkyrie <= 35), \
                           golem INTEGER CHECK(golem <= 35), \
                           sorcière INTEGER CHECK(sorcière <= 35), \
                           molosseDeLave INTEGER CHECK(molosseDeLave <= 35), \
                           bouliste INTEGER CHECK(bouliste <= 35), \
                           golemDeGlace INTEGER CHECK(golemDeGlace <= 35), \
                           chasseuse INTEGER CHECK(chasseuse <= 35), \
                           apprentiGardien INTEGER CHECK(apprentiGardien <= 35), \
                           Broyeur INTEGER CHECK(Broyeur <= 35), \
                           dirigeable INTEGER CHECK(dirigeable <= 35), \
                           Démolisseur INTEGER CHECK(Démolisseur <= 35), \
                           Caserne INTEGER CHECK(Caserne <= 35), \
                           lanceBuches INTEGER CHECK(lanceBuches <= 35), \
                           Catapulte INTEGER CHECK(Catapulte <= 35), \
                           foreuse INTEGER CHECK(foreuse <= 35), \
                           RoiDesBarbares INTEGER CHECK(RoiDesBarbares <= 150), \
                           ReineDesArchères INTEGER CHECK(ReineDesArchères <= 150), \
                           warden INTEGER CHECK(warden <= 150), \
                           championne INTEGER CHECK(championne <= 75), \
                           L.A.S.S.I INTEGER CHECK(L.A.S.S.I <= 35), \
                           mightyYak INTEGER CHECK(mightyYak <= 35), \
                           electroOwl INTEGER CHECK(electroOwl <= 35), \
                           Unicorn INTEGER CHECK(Unicorn <= 35), \
                           Frosty INTEGER CHECK(Frosty <= 35), \
                           Diggy INTEGER CHECK(Diggy <= 35), \
                           poisonLizard INTEGER CHECK(poisonLizard <= 35), \
                           Phoenix INTEGER CHECK(Phoenix <= 35))")
            

    


        





################################################
#
#       if button click                                                                               
#
################################################


@listen()
async def on_component(event: Component):
    ctx = event.ctx
    
    if event.ctx.custom_id == 'trophy':
        embeds = []
        for i in range(25):
            cursor.execute('SELECT * FROM Player ORDER BY trophée DESC, LvlDuClan ASC LIMIT 5 OFFSET ?', (0+5*i,))
            resultat = cursor.fetchall()
            embeds_ = Embed(title='Les joueur dans un clan français ayant le plus de trophée') 
            for line in resultat:
                embed = f'hdv : **{line[0]}**  |  psedo : **{line[1]}**  |  Tag du joueur : **{line[2]}**  |  nombre de trophée : **{line[3]}**  |  Niveau : **{line[4]}**  |  étoiles de guerre : **{line[5]}**  |  préference de guerre : **{line[6]}**  |  capacité de renfort donné : **{line[7]}**  |  point aux jeux de clan totale : **{line[8]}**  |  badge1 : **{line[9]}**  |  badge2 : **{line[10]}**  |  badge3 : **{line[11]}**.'
                embeds_.add_field(name=line[1], value=embed) # type: ignore
            embeds.append(embeds_)   
        
        paginator = Paginator.create_from_embeds(bot, *embeds)
        paginator.show_select_menu = True
        
        await paginator.send(ctx)

    elif event.ctx.custom_id == 'jdc':
        embeds = []
        for i in range(25):
            cursor.execute('SELECT * FROM Player ORDER BY pointsJDCTotal DESC, LvlDuClan ASC LIMIT 5 OFFSET ?', (0+5*i,))
            resultat = cursor.fetchall()
            embeds_ = Embed(title='Les joueur dans un clan français ayant fait le plus de point au jeux de clan') 
            for line in resultat:
                embed = f'hdv : **{line[0]}**  |  psedo : **{line[1]}**  |  Tag du joueur : **{line[2]}**  |  nombre de trophée : **{line[3]}**  |  Niveau : **{line[4]}**  |  étoiles de guerre : **{line[5]}**  |  préference de guerre : **{line[6]}**  |  capacité de renfort donné : **{line[7]}**  |  point aux jeux de clan totale : **{line[8]}**  |  badge1 : **{line[9]}**  |  badge2 : **{line[10]}**  |  badge3 : **{line[11]}**.'
                embeds_.add_field(name=line[1], value=embed) # type: ignore
            embeds.append(embeds_)   
        
        paginator = Paginator.create_from_embeds(bot, *embeds)
        paginator.show_select_menu = True
        
        await paginator.send(ctx)

    elif event.ctx.custom_id == 'don':
        embeds = []
        for i in range(25):
            cursor.execute('SELECT * FROM Player ORDER BY donnationTotal DESC, LvlDuClan ASC LIMIT 5 OFFSET ?', (0+5*i,))
            resultat = cursor.fetchall()
            embeds_ = Embed(title='Les joueur dans un clan français ayant donnée de troupes') 
            for line in resultat:
                embed = f'hdv : **{line[0]}**  |  psedo : **{line[1]}**  |  Tag du joueur : **{line[2]}**  |  nombre de trophée : **{line[3]}**  |  Niveau : **{line[4]}**  |  étoiles de guerre : **{line[5]}**  |  préference de guerre : **{line[6]}**  |  capacité de renfort donné : **{line[7]}**  |  point aux jeux de clan totale : **{line[8]}**  |  badge1 : **{line[9]}**  |  badge2 : **{line[10]}**  |  badge3 : **{line[11]}**.'
                embeds_.add_field(name=line[1], value=embed) # type: ignore
            embeds.append(embeds_)   
        
        paginator = Paginator.create_from_embeds(bot, *embeds)
        paginator.show_select_menu = True
        
        await paginator.send(ctx)
    elif event.ctx.custom_id == "info_géneral":
        

        embeds = ctx.message.embeds # on recupere la liste des embeds du message 
        embed = embeds[0] # on prend que le premier embed(il y en a qu'un mais obligé)
        title = embed.title # on extrait le contenue de la description de cet embed
        tag = title.split()[-1][1:] # on transforme cette description en une liste, on a donc tout les mots sans les espaces et on trouve le bon index ou se trouve le tag du joueur 
        print(tag)
        try:    
            url = f"https://api.clashofclans.com/v1/players/%23{tag}"
            response = requests.get(url, headers=infoGeneraleHeader)
            user_json = response.json()
            user_json = json.dumps(user_json)
            user = json.loads(user_json) 
            embed_profile = Embed(title=f"info génerale du joueur {user['tag']}", description=f"**psedo du joueur : {user['name']}**", color=interactions.Color.random(), timestamp=datetime.now())
            embed_profile.add_field(name="nombre de trophées du joueur :", value=f"{user['trophies']} {ligueAPI[user['league']['name']]}", inline=True)
            embed_profile.add_field(name="nombre d'etoiles de guerre :", value=f"{user['warStars']} <:st:1138557349913706616>", inline=True)
            CWLTotal = sorted(user['achievements'], key=lambda x : x['name'] != "War League Legend")[0]
            embed_profile.add_field(name="nombre d'étoiles gagnée pendant les ligue de clans :", value=f"{CWLTotal['value']} <:st:1138557349913706616>", inline=True)
            embed_profile.add_field(name=f"nombre d'attaque gagnée cette saison : {user['attackWins']} <:cc:1138557308083908648>", value=f" ", inline=True)
            combatTotal = sorted(user['achievements'], key=lambda x : x['name'] != "Conqueror")[0]
            embed_profile.add_field(name="nombre de combat gagnée au total :", value=f"{combatTotal['value']} <:cc:1138557308083908648>", inline=True)
            embed_profile.add_field(name="nombre de défense gagnée cette saison :", value=f"{user['defenseWins']} <:cc:1138557308083908648>", inline=True)
            try:
                embed_profile.add_field(name="rôle dans son clan :", value="{}".format("chef" if user['role'] =="leader" else("chef adjoint" if user['role'] == "coLeader" else ("ainé" if user['role'] == "admin" else "membre"))), inline=True)
            except Exception:
                embed_profile.add_field(name="rôle dans son clan :", value="n'est actuellement pas dans un clan")
            embed_profile.add_field(name="préference de guerre :", value=f"{'<:yy:1137489567973388348>' if user['warPreference'] == 'in' else '<:nn:1137489472989188276>'}", inline=True)
            embed_profile.add_field(name=f"nombre de troupe donnée cette saison : {user['donations']} <:dd:1138557463851962509>", value=f" ", inline=True)
            embed_profile.add_field(name="nombre de troupe recu cette saison :", value=f"{user['donationsReceived']} <:dd:1138557463851962509>", inline=True)      
            embed_profile.add_field(name="contribution a la capitale de clan :", value=f"{user['clanCapitalContributions']} <:jj:1137489208232124476>", inline=True)  
            embed_profile.add_field(name="niveau d'hotel de ville :", value=f"{user['townHallLevel']}", inline=True)
            embed_profile.add_field(name="{} :".format("niveau de la giga tour de l'enfer" if user['townHallLevel'] == 13 or 14 or 15 else "niveau de la giga tesla"), value=f"{user['townHallWeaponLevel']}")
            embed_profile.add_field(name="niveau du joueur :", value=f"{user['expLevel']} <:exp:1137420369259675669>", inline=True)
            jdcTotal = sorted(user['achievements'], key=lambda x : x['name'] != "Games Champion")[0]
            embed_profile.add_field(name="points aux jeux de clans totaux :", value=f"{jdcTotal['value']}", inline=True)
            try:
                text = ""
                for label in user['labels']:
                    text = text + f"{labelsEmoji[label['name']]['emoji']} {labelsEmoji[label['name']]['Fr']} | "
                embed_profile.add_field(name="les labels du joueur :", value=text, inline=False)
            except Exception:
                traceback.print_exc()

            embed_profile.set_thumbnail(url=hdvPNG[user['townHallLevel']-1]['th'][user['townHallWeaponLevel']-1])
            embed_profile.set_footer(text=user['tag'])
            embedInfoGenerale = embed_profile.to_dict()
            try:
                user['clan']
                try:
                    user['heroes']
                    try:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                    except Exception :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
            except Exception :
                try :
                    user['heroes']
                    try :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                    except Exception:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=True, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
            await ctx.send(embed=embedInfoGenerale, components=components)
        except KeyError:
            traceback.print_exc()
            await ctx.send("Erreur : tag du joueur invalide.")
        except Exception: # si il y a une erreur qui n'est pas mentionner plus haut 
            await ctx.send("Erreur : veuillez réessayer plus tard.")
            traceback.print_exc()


    elif event.ctx.custom_id == 'info_labo':

        embeds = ctx.message.embeds # on recupere la liste des embeds du message 
        embed = embeds[0] # on prend que le premier embed(il y en a qu'un mais obligé)
        title = embed.title # on extrait le contenue de la description de cet embed
        tag = title.split()[-1][1:] # on transforme cette description en une liste, on a donc tout les mots sans les espaces et on trouve le bon index ou se trouve le tag du joueur
        print(tag) # débug
        try:    
            url = f"https://api.clashofclans.com/v1/players/%23{tag}"
            response = requests.get(url, headers=laboHeader)
            user_json = response.json()
            user_json = json.dumps(user_json)
            user = json.loads(user_json) 
            troops = user['troops']
            sort = user['spells']
            
            embedLabo = Embed(title=f"le labo et les heros du joueur {user['tag']}", description=f"**psedo du joueur : {user['name']}**", color=interactions.Color.random(), timestamp=datetime.now()) # on recée l'embed de base
            try:
                embedLabo.set_thumbnail(url=laboPNG[user['townHallLevel']-1])
            except Exception:
                traceback.print_exc()
            embedLabo.add_field(name="Les troupes d'élexire", value=" ", inline=False)
            for i in range(math.ceil(len(trpRoseFR)/2)): # on divise le nb de trp par 2 et on arrondit a l'entier superieur avec math.ceil()
                trp = [] # on reinisialise les data des trp
                i = i*2 # on multiplie i pas 2 pour avoir un pas de 2 
                for e in range(2): #on crée une boucle pour recuperer les data 2 par 2 
                    i = i + e
                    try:
                        trpTest = sorted(troops, key= lambda x : x['name'] != trpRoseAPI[i])[0] # on trie la liste pour que le premier index corespond a ce qu'on cherche
                        if trpTest['name'] == trpRoseAPI[i]: # on verifie que ce sont les bonnes troupes
                            trpTest['name'] = trpRoseFR[i] # on traduit le nom des trp en fr
                            trp.append(trpTest) # et on ajoute la troupes a la liste
                    except Exception:
                        pass
                    
                    
                
                try: 
                    embedLabo.add_field(name=f"{emojiTrpRoseFR[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f"\n**{emojiTrpRoseFR[trp[1]['name']]} : lvl {trp[1]['level']} {'MAX !' if trp[1]['level'] == trp[1]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[1]['name']] == trp[1]['level'] else '')}**", inline=True)
                except Exception:
                    try:
                        embedLabo.add_field(name=f"{emojiTrpRoseFR[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f" ", inline=True)
                    except Exception:
                        traceback.print_exc()


            embedLabo.add_field(name="Les sort", value=" ", inline=False)
            for i in range(math.ceil(len(sortDataFR)/2)): # on divise le nb de trp par 2 et on arrondit a l'entier superieur avec math.ceil()
                trp = [] # on reinisialise les data des trp
                i = i*2 # on multiplie i pas 2 pour avoir un pas de 2 
                for e in range(2): #on crée une boucle pour recuperer les data 2 par 2 
                    i = i + e
                    try: 
                        trpTest = sorted(sort, key= lambda x : x['name'] != sortAPI[i])[0] # on trie la liste pour que le premier index corespond a ce qu'on cherche
                        if trpTest['name'] == sortAPI[i]: # on verifie que ce sont les bonnes troupes
                            trpTest['name'] = sortDataFR[i] # on traduit le nom des trp en fr
                            trp.append(trpTest) # et on ajoute la troupes a la liste
                    except Exception :
                        pass
                    
                try: 
                    embedLabo.add_field(name=f"{emojiSortFR[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f"\n**{emojiSortFR[trp[1]['name']]} : lvl {trp[1]['level']} {'MAX !' if trp[1]['level'] == trp[1]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[1]['name']] == trp[1]['level'] else '')}**", inline=True)
                except Exception:
                    try:
                        embedLabo.add_field(name=f"{emojiSortFR[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f" ", inline=True)
                    except Exception:
                        traceback.print_exc()


            embedLabo.add_field(name="Les troupes d'élexire noir", value=" ", inline=False)
            for i in range(math.ceil(len(trpNoirFR)/2)): # on divise le nb de trp par 2 et on arrondit a l'entier superieur avec math.ceil()
                trp = [] # on reinisialise les data des trp
                i = i*2 # on multiplie i pas 2 pour avoir un pas de 2 
                for e in range(2): #on crée une boucle pour recuperer les data 2 par 2 
                    i = i + e
                    try:
                        trpTest = sorted(troops, key= lambda x : x['name'] != trpNoirAPI[i])[0] # on trie la liste pour que le premier index corespond a ce qu'on cherche
                        if trpTest['name'] == trpNoirAPI[i]: # on verifie que ce sont les bonnes troupes
                            trpTest['name'] = trpNoirFR[i] # on traduit le nom des trp en fr
                            trp.append(trpTest) # et on ajoute la troupes a la liste
                    except Exception:
                        pass 
                    
                try: 
                    embedLabo.add_field(name=f"{emojiTrpNoirFR[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f"\n**{emojiTrpNoirFR[trp[1]['name']]} : lvl {trp[1]['level']} {'MAX !' if trp[1]['level'] == trp[1]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[1]['name']] == trp[1]['level'] else '')}**", inline=True)
                except Exception:
                    try:
                        embedLabo.add_field(name=f"{emojiTrpNoirFR[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f" ", inline=True)
                    except Exception:
                        traceback.print_exc()
            
            try:
                user['clan']
                try:
                    user['heroes']
                    try:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=True, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                    except Exception :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=True, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=True, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
            except Exception :
                try :
                    user['heroes']
                    try :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=True, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                    except Exception:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=True, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=True, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
            
            embedLabo = embedLabo.to_dict()
            await ctx.edit_origin(embed=embedLabo, components=components)


        except Exception:
            traceback.print_exc()


    elif event.ctx.custom_id == "info_hero":
        embeds = ctx.message.embeds # on recupere la liste des embeds du message 
        embed = embeds[0] # on prend que le premier embed(il y en a qu'un mais obligé)
        title = embed.title # on extrait le contenue de la description de cet embed
        tag = title.split()[-1][1:] # on transforme cette description en une liste, on a donc tout les mots sans les espaces et on trouve le bon index ou se trouve le tag du joueur
        print(tag) # débug
        try:    
            url = f"https://api.clashofclans.com/v1/players/%23{tag}"
            response = requests.get(url, headers=laboHeader)
            user_json = response.json()
            user_json = json.dumps(user_json)
            user = json.loads(user_json) 
            héros = user['heroes']
            famillier = user['troops']
            embedHeros = Embed(title=f"les heros du joueur {user['tag']}", description=f"**psedo du joueur : {user['name']}  **", color=interactions.Color.random(), timestamp=datetime.now()) # on recée l'embed de base
            embedHeros.add_field(name="Les héros", value=" ", inline=False)
            for i in range(math.ceil(len(hérosFR)/2)): # on divise le nb de trp par 2 et on arrondit a l'entier superieur avec math.ceil()
                trp = [] # on reinisialise les data des trp
                i = i*2 # on multiplie i pas 2 pour avoir un pas de 2 
                for e in range(2): #on crée une boucle pour recuperer les data 2 par 2 
                    i = i + e
                    try:
                        trpTest = sorted(héros, key= lambda x : x['name'] != herosAPI[i])[0] # on trie la liste pour que le premier index corespond a ce qu'on cherche
                        if trpTest['name'] == herosAPI[i]: # on verifie que ce sont les bonnes troupes
                            trpTest['name'] = hérosFR[i] # on traduit le nom des trp en fr
                            trp.append(trpTest) # et on ajoute la troupes a la liste
                    except Exception:
                        pass
                    
                try: 
                    embedHeros.add_field(name=f"{emojiHero[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f"\n**{emojiHero[trp[1]['name']]} : lvl {trp[1]['level']} {'MAX !' if trp[1]['level'] == trp[1]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[1]['name']] == trp[1]['level'] else '')}**", inline=True)
                except Exception:
                    try:
                        embedHeros.add_field(name=f"{emojiHero[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f" ", inline=True)
                    except Exception:
                        traceback.print_exc()
        

            embedHeros.add_field(name="Les famillier", value=" ", inline=False)
            for i in range(math.ceil(len(famillierAPI)/2)): # on divise le nb de trp par 2 et on arrondit a l'entier superieur avec math.ceil()
                trp = [] # on reinisialise les data des trp
                i = i*2 # on multiplie i pas 2 pour avoir un pas de 2 
                for e in range(2): #on crée une boucle pour recuperer les data 2 par 2 
                    i = i + e
                    try:
                        trpTest = sorted(famillier, key= lambda x : x['name'] != famillierAPI[i])[0] # on trie la liste pour que le premier index corespond a ce qu'on cherche
                        if trpTest['name'] == famillierAPI[i]: # on verifie que ce sont les bonnes troupes
                            trp.append(trpTest) # et on ajoute la troupes a la liste
                    except Exception:
                        pass
                    
                try: 
                    embedHeros.add_field(name=f"{emojiFamillier[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f"\n**{emojiFamillier[trp[1]['name']]} : lvl {trp[1]['level']} {'MAX !' if trp[1]['level'] == trp[1]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[1]['name']] == trp[1]['level'] else '')}**", inline=True)
                except Exception:
                    try:
                        embedHeros.add_field(name=f"{emojiFamillier[trp[0]['name']]} : lvl {trp[0]['level']} {'MAX !' if trp[0]['level'] == trp[0]['maxLevel'] else ('max pour son hdv !' if betterTroops[user['townHallLevel']-1][trp[0]['name']] == trp[0]['level'] else '')}", value=f" ", inline=True)
                    except Exception:
                        traceback.print_exc()
            if herosthumbnail[user['townHallLevel']-1] != "":
                embedHeros.set_thumbnail(url=herosthumbnail[user['townHallLevel']-1])
            try:
                user['clan']
                try:
                    user['heroes']
                    try:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                    except Exception :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False))]
            except Exception :
                try :
                    user['heroes']
                    try :
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                    except Exception:
                        components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
                except Exception:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=True), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True))]
            embedHeros = embedHeros.to_dict()
            await ctx.edit_origin(embed=embedHeros, components=components)


        except Exception:
            traceback.print_exc()
    
    elif event.ctx.custom_id == "info_clan" :
        try:
            embeds = ctx.message.embeds # on recupere la liste des embeds du message 
            embed = embeds[0] # on prend que le premier embed(il y en a qu'un mais obligé)
            title = embed.title # on extrait le contenue de la description de cet embed
            tag = title.split()[-1][1:] # on transforme cette description en une liste, on a donc tout les mots sans les espaces et on trouve le bon index ou se trouve le tag du joueur
            print(tag) # débug 
            url = f"https://api.clashofclans.com/v1/players/%23{tag}"
            response = requests.get(url, headers=laboHeader)
            user_json = response.json()
            user_json = json.dumps(user_json)
            user = json.loads(user_json)
            clanTag = user['clan']['tag'][1:]
            clanUrl = f"https://api.clashofclans.com/v1/clans/%23{clanTag}"
            response = requests.get(clanUrl, headers=laboHeader)
            userClan = response.json()
            userClan = json.dumps(userClan)
            userClan = json.loads(userClan)
            print(userClan)
            clanEmbed = Embed(title=f"clan de {user['name']} {user['tag']}", description=f"**{userClan['name']}** {userClan['tag']}", color=interactions.Color.random(), timestamp=datetime.now())
            clanEmbed.add_field(name=f"description :", value=f"{userClan['description']}", inline=False)
            clanEmbed.add_field(name=f"statut du clan :", value=f"{userClan['requiredTrophies']} <:tr:1137414233693376632>", inline=True)
            clanEmbed.add_field(name=f"trophées requis :", value=f"{clanType[userClan['type']]}", inline=True)
            try:
                clanEmbed.add_field(name=f"location du clan :", value=f"{userClan['location']['name']}", inline=True)
            except Exception: 
                clanEmbed.add_field(name=f"location du clan :", value=f"location indéterminer", inline=True)
            clanEmbed.set_thumbnail(url=userClan['badgeUrls']['large'])
            clanEmbed.add_field(name=f"niveau du clan :", value=f"{userClan['clanLevel']}", inline=True)
            clanEmbed.add_field(name=f"trophées du clan :" , value=f"{userClan['clanPoints']} <:tr:1137414233693376632>       {userClan['clanBuilderBasePoints']} <:Icon_Versus_Trophy:1146190738695143534>", inline=True)
            clanEmbed.add_field(name=f"trophée de la capitale de clan :", value=f"{userClan['clanCapitalPoints']} {ligueAPI[userClan['capitalLeague']['name']]}", inline=True)
            clanEmbed.add_field(name=f"trophée requis :", value=f"{userClan['requiredTrophies']}", inline=True)
            clanEmbed.add_field(name=f"victoire en guerre :", value=f"{userClan['warWins']}", inline=True)
            clanEmbed.add_field(name=f"victoire concecutive en guerre :", value=f"{userClan['warWinStreak']}", inline=True)
            clanEmbed.add_field(name=f"ligue de clan :", value=f"{ligueLDC[userClan['warLeague']['name']]}", inline=True)

            
            try:
                user['heroes']
                try:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True), Button(style=ButtonStyle.PRIMARY, label='les membre du clan', custom_id="info_clan_membre", disabled=False))]
                except Exception :
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True), Button(style=ButtonStyle.PRIMARY, label='les membre du clan', custom_id="info_clan_membre", disabled=False))]
            except Exception:
                components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=True), Button(style=ButtonStyle.PRIMARY, label='les membre du clan', custom_id="info_clan_membre", disabled=False))]
            clanEmbed = clanEmbed.to_dict()
            await ctx.edit_origin(embed=clanEmbed, components=components)
        except Exception : 
            traceback.print_exc()


    elif event.ctx.custom_id == "info_clan_membre" :
        try :
            embeds = ctx.message.embeds # on recupere la liste des embeds du message 
            embed = embeds[0] # on prend que le premier embed(il y en a qu'un mais obligé)
            title = embed.title # on extrait le contenue de la description de cet embed
            tag = title.split()[-1][1:] # on transforme cette description en une liste, on a donc tout les mots sans les espaces et on trouve le bon index ou se trouve le tag du joueur
            embeds = ctx.message.embeds # on recupere la liste des embeds du message 
            embed = embeds[0] # on prend que le premier embed(il y en a qu'un mais obligé)
            descption = embed.description # on extrait le contenue de la description de cet embed
            clanTag = descption.split()[-1][1:] # on transforme cette description en une liste, on a donc tout les mots sans les espaces et on trouve le bon index ou se trouve le tag du joueur
            print(clanTag) 
            try:
                userUrl = f"https://api.clashofclans.com/v1/players/%23{tag}"
                response = requests.get(userUrl, headers=laboHeader)
                user = response.json()
                user = json.dumps(user)
                user = json.loads(user)
                
            except Exception:
                traceback.print_exc()
            try:
                clanUrl = f"https://api.clashofclans.com/v1/clans/%23{clanTag}"
                response = requests.get(clanUrl, headers=laboHeader)
                userClan = response.json()
                userClan = json.dumps(userClan)
                userClan = json.loads(userClan)
            except Exception:
                traceback.print_exc()
            memberEmbed = Embed(title=f"membre du clan de {user['name']} {user['tag']}", description=f"**{userClan['name']} {userClan['tag']}**", color=interactions.Color.random(), timestamp=datetime.now())
            coleaders = []
            admins = []
            members = []
            for member in userClan['memberList']:
                if member['role'] == "leader":
                    chef = member
                elif member['role'] == "coLeader":
                    coleaders.append(member)
                elif member['role'] == "admin":
                    admins.append(member)
                elif member['role'] == "member":
                    members.append(member)

            memberEmbed.add_field(name=f"membre : {userClan['members']}/50", value=" ")
            memberEmbed.add_field(name=f"Chef", value=f"{chef['name']} {chef['tag']} {chef['expLevel']} <:exp:1137420369259675669> {chef['trophies']} {ligueAPI[chef['league']['name']]} <:dd:1138557463851962509> {chef['donations']} <:dd:1138557463851962509> {chef['donationsReceived']}")
            coleaderValue = ""
            for coleader in coleaders:
                coleaderValue = coleaderValue + f"{coleader['name']} {coleader['tag']} {coleader['expLevel']} <:exp:1137420369259675669> {coleader['trophies']} {ligueAPI[coleader['league']['name']]}  <:dd:1138557463851962509> {coleader['donations']} <:dd:1138557463851962509> {coleader['donationsReceived']} \n"
            memberEmbed.add_field(name=f"Chef adjoint", value=coleaderValue)
            
            adminValue = ""
            for admin in admins:
                adminValue = adminValue + f"{admin['name']} {admin['tag']} {admin['expLevel']} <:exp:1137420369259675669> {admin['trophies']} {ligueAPI[admin['league']['name']]}  <:dd:1138557463851962509> {admin['donations']} <:dd:1138557463851962509> {admin['donationsReceived']} \n"
            memberEmbed.add_field(name=f"ainé", value=adminValue)
            
            memberValue =""
            for member in members:
                memberValue = memberValue + f"{member['name']} {member['tag']} {member['expLevel']} <:exp:1137420369259675669> {member['trophies']} {ligueAPI[member['league']['name']]} {member['builderBaseTrophies']} <:Icon_Versus_Trophy:1146190738695143534> <:dd:1138557463851962509> {member['donations']} <:dd:1138557463851962509> {member['donationsReceived']} \n"
            memberEmbed.add_field(name=f"membre", value=memberValue)
            try:
                user['heroes']
                try:
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False, emoji=herostemoji[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False), Button(style=ButtonStyle.PRIMARY, label='les membre du clan', custom_id="info_clan_membre", disabled=True))]
                except Exception :
                    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False), Button(style=ButtonStyle.PRIMARY, label='les membre du clan', custom_id="info_clan_membre", disabled=True))]
            except Exception:
                components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.PRIMARY, label='les héros du joueur', custom_id="info_hero", disabled=False), Button(style=ButtonStyle.PRIMARY, label='le labo du joueur', custom_id="info_labo", disabled=False, emoji=emojiLabo[user['townHallLevel']-1]), Button(style=ButtonStyle.PRIMARY, label='les infos générales du joueur', custom_id="info_géneral", disabled=False, emoji="<:ii:1137487775671787620>"), Button(style=ButtonStyle.PRIMARY, label='le clan du joueur', custom_id="info_clan", disabled=False), Button(style=ButtonStyle.PRIMARY, label='les membre du clan', custom_id="info_clan_membre", disabled=True))]
            memberEmbed = memberEmbed.to_dict()
            await ctx.edit_origin(embed=memberEmbed, components=components)
        except Exception:
            traceback.print_exc()





################################################
#
#       ldc command
#
################################################
   

# ldc preview in one select channel update if sth is new
@slash_command(name = 'ldc', description = "afficher les guerre dans ce channel")
@slash_option(name = 'tag', description="tag du clan", required=True, opt_type=OptionType.STRING )
async def ldc(ctx : SlashContext, tag):
    channel = ctx.channel    
    message = await channel.send(content="veuiller patienter")
    try :
        warTagId = await ldc_find_war_tag_id(tag)
    except : 
        await ctx.send(content="Ce n'est pas l'heur des ldc ! refaites la commande quand ce sera le cas.")
        await message.delete(0)
        return
    await message.delete(0)
    while warTagId is not None:
        url = f"https://api.clashofclans.com/v1/clanwarleagues/wars/%23{warTagId}"
        response = requests.get(url, headers=GDCBotheader)
        ldcWar = response.json()
        ldcWar = json.dumps(ldcWar)
        ldcWar = json.loads(ldcWar)
        clanInfo = ldcWar['clan']
        opponentInfo = ldcWar['opponent']
        endTime = ldcWar['endTime']
        endTime = parser.parse(endTime)
        timestampEndTime = f"<t:{int(endTime.timestamp())}:R>"
        preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
        preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
        preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine** {timestampEndTime}",  inline=False)
        prepartionMessage = await channel.send(embed=preparationEmbed)
        

        messID = []
        for jsp in range(int(ldcWar['teamSize']/5)):
            warMessage = await channel.send(content='yo !')
            messID.append(warMessage)
        while True :
            url = f"https://api.clashofclans.com/v1/clanwarleagues/wars/%23{warTagId}"
            response = requests.get(url, headers=GDCBotheader)
            ldcWar = response.json()
            ldcWar = json.dumps(ldcWar)
            ldcWar = json.loads(ldcWar)


            if ldcWar['state'] == 'warEnded':
                break
            
            
            # on recupere toutes les informations sur le clan
            clanInfo = ldcWar['clan']
            clanMemberInfo = clanInfo['members']
            clanMemberInfo = sorted(clanMemberInfo, key= lambda x : x['townhallLevel'], reverse=True)# on ordonne les joueurs de la guerre en fonction de leur position dans la guerre
            # on recupere toutes les informations sur le clan
            opponentInfo = ldcWar['opponent'] 
            opponentMemberInfo = opponentInfo['members']
            opponentMemberInfo = sorted(opponentMemberInfo, key= lambda x : x['townhallLevel'], reverse=True)# on ordonne les joueurs de la guerre en fonction de leur position dans la guerre


            endTime = ldcWar['endTime']
            endTime = parser.parse(endTime)
            endTimeTimestamp = f"<t:{int(endTime.timestamp())}:R>"
            try:
                preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine** {endTimeTimestamp}",  inline=False)
                await prepartionMessage.edit(embed=preparationEmbed)
            except Exception :
                prepartionMessage.delete()
                preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine** {endTimeTimestamp}",  inline=False)
                prepartionMessage = await channel.send(embed=preparationEmbed)


            for a in range(int(ldcWar['teamSize']/5)): # on calcule le nombre d'embed nécessaire (on prend ici 5 joueur par embed)
                clanValue="" # on initialise et reinitialise le message dans l'embed 
                opponentValue ="" # on initialise et reinitialise le message dans l'embed
                embeds = Embed(color=interactions.Color.from_rgb(255, 128, 0)) # on initialise et reinitialise l'embed avec la couleur orange 
                for i in range(5): # pour 5 joueurs 
                    i = i + a * 5 # petit calcule pour mettre les joueurs de 5 en 5 
                    try:
                        for z in range(len(opponentMemberInfo)):
                            if opponentMemberInfo[z]['tag'] == clanMemberInfo[i]['bestOpponentAttack']['attackerTag']:
                                opponentMemberInfodef = opponentMemberInfo[z]['mapPosition']
                                opponentMemberInfodefName = opponentMemberInfo[z]['name']
                                break
                        try:
                            clanValue = clanValue + "**{}. {}** {}  {} \n\n".format(
                                i+1,
                                clanMemberInfo[i]['name'],
                                ("" if len(clanMemberInfo[i]['attacks']) == 1 else ":crossed_swords:" ),
                                "{} :star::star::star:".format(
                                    opponentMemberInfodefName
                                ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                    "{} :star::star:".format(
                                        opponentMemberInfodefName
                                    ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                        "{} :star:".format(
                                            opponentMemberInfodefName
                                        ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else 
                                        "{}: 0 étoile".format(
                                                opponentMemberInfodefName
                                        )
                                    )
                                )
                            )
                        except Exception: 
                            clanValue = clanValue + "**{}. {} :crossed_swords: ** {} \n\n".format(
                                i+1,
                                clanMemberInfo[i]['name'],
                                "{} :star::star::star:".format(
                                    opponentMemberInfodefName
                                ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                    "{} :star::star:".format(
                                        opponentMemberInfodefName
                                    ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                        "{} :star:".format(
                                            opponentMemberInfodefName
                                        ) if clanMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else 
                                        "{}: 0 étoile".format(
                                                opponentMemberInfodefName
                                        )
                                    )
                                )
                            )
                    except Exception:
                        try:
                            clanValue = clanValue + f"**{i+1}. {clanMemberInfo[i]['name']} {'' if len(clanMemberInfo[i]['attacks']) == 1 else ':crossed_swords:' }** n'a pas encore été attaqué\n\n"
                        except Exception:
                            clanValue = clanValue + f"**{i+1}. {clanMemberInfo[i]['name']} :crossed_swords:** n'a pas encore été attaqué \n\n"
                    try:
                        for z in range(len(clanMemberInfo)): # pour chaque joueur 
                            if clanMemberInfo[z]['tag'] == opponentMemberInfo[i]['bestOpponentAttack']['attackerTag']: # si le tag du joueur adverse est le meme que le tag de l'attaquant 
                                opponentMemberInfodefName = clanMemberInfo[z]['name'] # on recupere son psedo 
                                break
                        # les message pour un joueur qui a été attaqué et qui a attaqué
                        try : 
                            opponentValue = opponentValue + " **{}. {} {}** {} \n\n".format(
                                i+1,
                                    opponentMemberInfo[i]['name'], 
                                        ("" if len(opponentMemberInfo[i]['attacks']) == 1 else ":crossed_swords:" ), 
                                    "{}: :star::star::star:".format(
                                        opponentMemberInfodefName
                                    ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                        "{}: :star::star:".format(
                                            opponentMemberInfodefName
                                        ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                            "{}: :star:".format(
                                                opponentMemberInfodefName
                                            ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else
                                            "{}: 0 étoile".format(
                                                opponentMemberInfodefName
                                            )
                                        )
                                    )
                                )
                        # les message pour un joueur qui a été attaqué et qui n'a pas attaqué 
                        except Exception: 
                            opponentValue = opponentValue + " **{}. {} :crossed_swords:** {} \n\n".format(
                                i+1,
                                    opponentMemberInfo[i]['name'], 
                                    "{}: :star::star::star:".format(
                                        opponentMemberInfodefName
                                    ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 3 else (
                                        "{}: :star::star:".format(
                                            opponentMemberInfodefName
                                        ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 2 else (
                                            "{}. {}: :star:".format(
                                                opponentMemberInfodefName
                                            ) if opponentMemberInfo[i]['bestOpponentAttack']['stars'] == 1 else
                                            "{}: 0 étoile".format(
                                                opponentMemberInfodefName
                                            )
                                        )
                                    )
                                )
                    except Exception :  # si les joueurs n'on pas encore été attaqué
                        try: # si les joueur n attaqué
                            opponentValue = opponentValue + f" **{i+1}. {opponentMemberInfo[i]['name']} {'' if len(opponentMemberInfo[i]['attacks']) == 1 else ':crossed_swords:'}** n'a pas encore été attaqué\n\n"
                        except Exception: # si les joueur n'ont pas attaqué
                            opponentValue = opponentValue + f" **{i+1}. {opponentMemberInfo[i]['name']} :crossed_swords:** n'a pas encore été attaqué\n\n"
                embeds.add_field(name='votre clan' , value=clanValue , inline=True) # on ajoute les données des joueur du clan dans l'embed (inline=True est utiliser pour que les messages soit sous forme de colones)
                print(clanValue) 
                embeds.add_field(name='le clan adverse', value=opponentValue, inline=True )# on ajoute les données des joueur du clan adverse dans l'embed (inline=True est utiliser pour que les messages soit sous forme de colones)
                print(opponentValue)
                try : 
                    await messID[a].edit(content='',embed=embeds)
                except Exception: # si on ne peut pas modifier le message parce que les 15 minute apres l'envoie du message sont passé
                    for e in range(int(ldcWar['teamSize']/5)): # on supprime tout les messages qui ont été envoyées
                        await messID[e].delete()
                    messID=[] # on reinisialise la liste des messages 
                    for jsp in range(int(ldcWar['teamSize']/5)): # on réenvoie les messages
                        warMessage = await channel.send(content='yo !')
                        messID.append(warMessage)
            await asyncio.sleep(60)
        warTagId = await ldc_find_war_tag_id(tag)


async def ldc_find_war_tag_id(tag):
    tagID = tag[1:]
    url = f"https://api.clashofclans.com/v1/clans/%23{tagID}/currentwar/leaguegroup" 
    response = requests.get(url, headers=GDCBotheader)
    war_tags = response.json()
    war_tags = json.dumps(war_tags)
    war_tags = json.loads(war_tags)
    for round in war_tags['rounds']:
        for war_tags in round['warTags']:
            war_tag_id = war_tags
            war_tag_id = str(war_tag_id[1:])
            url = f"https://api.clashofclans.com/v1/clanwarleagues/wars/%23{war_tag_id}"
            response = requests.get(url, headers=GDCBotheader)
            ldcWar = response.json()
            ldcWar = json.dumps(ldcWar)
            ldcWar = json.loads(ldcWar)
            await asyncio.sleep(1)
            if war_tags == '#0':
                break
            elif (ldcWar['clan']['tag'] == tag or ldcWar['opponent']['tag'] == tag) and ldcWar['state'] == 'inWar':
                print('real id is: '+ war_tag_id)
                return war_tag_id

bot.start() 