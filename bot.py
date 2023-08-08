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
from interactions import slash_command, SlashContext, Modal, ShortText, ParagraphText
import time
import asyncio
import math
import timestamp
from config import TOKEN, GDCBotheader, laboHeader, clanHeader, infoGeneraleHeader
from trpData import betterTroops, trpRoseFR, trpRoseAPI, emojiTrpRoseFR, trpNoirFR, emojiTrpNoirFR , trpNoirAPI, hdvPNG, sortAPI, sortDataFR , emojiSortFR, laboPNG, herosAPI, hérosFR, emojiHero, ligueAPI, emojiFamillier, famillierAPI, herosthumbnail, emojiLabo, herostemoji, labelsEmoji

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
                time_difference = starTime  -  datetime.now(timezone.utc)
                hours = time_difference // 3600 
                minutes = (time_difference % 3600) // 60
                preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre commence dans : {int(hours)} heures et {int(minutes)} minutes**",  inline=False)
                await prepartionMessage.edit(embed=preparationEmbed)
                await asyncio.sleep(60)
                response = requests.get(url, headers=GDCBotheader) 
                currentwar = response.json()  
                currentwar = json.dumps(currentwar)
                currentwar = json.loads(currentwar)

            if currentwar['state'] == 'inWar': # si le clan est dans une guerre 
                messID=[]
                for jsp in range(int(currentwar['teamSize']/5)):
                    warMessage = await channel.send(content='yo !')
                    messID.append(warMessage)
                    print(messID)      
  
            while currentwar['state'] == 'inWar':
                endTime = currentwar['endTime']
                endTime = parser.parse(endTime)
                time_difference = endTime  -  datetime.now(timezone.utc)
                hours = time_difference // 3600 
                minutes = (time_difference % 3600) // 60
                try:
                    preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                    preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                    preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine dans : {int(hours)} heures et {int(minutes)} minutes**",  inline=False)
                    await prepartionMessage.edit(embed=preparationEmbed)
                except Exception :
                    preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                    preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                    preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine dans : {int(hours)} heures et {int(minutes)} minutes**",  inline=False)
                    prepartionMessage = await channel.send(embed=preparationEmbed)

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
    warTagId = await ldc_find_war_tag_id(tag)
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
        time_difference = endTime  -  datetime.now(timezone.utc)
        hours = time_difference.seconds // 3600 
        minutes = (time_difference.seconds % 3600) // 60
        preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
        preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
        preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine dans : {int(hours)} heures et {int(minutes)} minutes**",  inline=False)
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
            time_difference = endTime  -  datetime.now(timezone.utc)
            hours = time_difference.seconds // 3600 
            minutes = (time_difference.seconds % 3600) // 60
            try:
                preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine dans : {int(hours)} heures et {int(minutes)} minutes**",  inline=False)
                await prepartionMessage.edit(embed=preparationEmbed)
            except Exception :
                prepartionMessage.delete()
                preparationEmbed = Embed(title = f"{clanInfo['name']}   {clanInfo['stars']}          vs           {opponentInfo['stars']}   {opponentInfo['name']}", color=interactions.Color.from_rgb(255, 128, 0))
                preparationEmbed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
                preparationEmbed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['attacks']}    |     {opponentInfo['attacks']}" + f"\nla guerre se termine dans : {int(hours)} heures et {int(minutes)} minutes**",  inline=False)
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
