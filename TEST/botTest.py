import discord
from discord.ext import commands
import interactions 
import requests
import requests_cache
import json
import sqlite3
from interactions import Button, ButtonStyle, listen, slash_command, slash_option, OptionType, SlashContext, Embed, Intents
from interactions.api.events import Component
import traceback
from interactions.ext import prefixed_commands
import pytz
from datetime import datetime, timezone
from dateutil import parser

searchClanHeader = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImVjNWVkODY2LWVmMzctNDZjYi1hOTM4LWUzMWFlMmE3YjhhMCIsImlhdCI6MTY4NjQxNDM2Nywic3ViIjoiZGV2ZWxvcGVyLzc4ZjdjMzM2LWM2NjUtYzdmYi0xYzhkLTE0YjlhZTY4NjEwMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgxLjY0LjI1NS4xMTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.J_1HMMjTeUzEndQ30VTCP582vqH6rpnQw01qdIsM6I9RZ0HWOiZw9wtvlhdePfvnUHvwAKGv8Ql3rCoBR80S2Q'
}


conn = sqlite3.connect('CocPlayer.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 
################################################
#
#       bot init                                                                              
#
################################################ 

TOKEN = "MTExODUzODE2NDI2OTc1MjMyMA.G9au5g.hReBnZrtyN09Cf0oam5cnzqdj4zhNf64TYa9f8"
bot = interactions.Client(token=TOKEN, intents=Intents.DEFAULT)
prefixed_commands.setup(bot)

@listen()
async def on_ready():
    print(f"{bot.user} s'est connecté")

@slash_command(name='gdc', description="visualiser la gdc dun clan")
@slash_option(name='id', description='le tag du clan', required=True, opt_type=OptionType.STRING)
async def gdc(ctx : SlashContext, id):
    channel = ctx.channel
    id=id[1:]
    try:
        url = f"https://api.clashofclans.com/v1/clans/%23{id}/currentwar"
        response = requests.get(url, headers=searchClanHeader)
        currentwar = response.json()  
        currentwar = json.dumps(currentwar)
        currentwar = json.loads(currentwar)
        starTime = currentwar['startTime']
        starTime = parser.parse(starTime)
        time_difference = starTime  -  datetime.now(timezone.utc)
        hours = time_difference.seconds // 3600 
        minutes = (time_difference.seconds % 3600) // 60
        seconds = time_difference.seconds % 60
        clanInfo = currentwar['clan']
        clanMemberInfo = clanInfo['members']
        clanMemberInfo = sorted(clanMemberInfo, key= lambda x : x['mapPosition'])
        opponentInfo = currentwar['opponent']
        opponentMemberInfo = opponentInfo['members']
        opponentMemberInfo = sorted(opponentMemberInfo, key= lambda x : x['mapPosition'])
        embed = Embed(title = f"**{clanInfo['name']}   {clanInfo['stars']}**          vs           {opponentInfo['stars']}   {opponentInfo['name']}" if float(clanInfo['destructionPercentage']) > float(opponentInfo['destructionPercentage']) else f"{clanInfo['name']} {clanInfo['stars']}   vs   **{opponentInfo['stars']}   {opponentInfo['name']}**", color=interactions.Color.from_rgb(255, 128, 0))
        embed.set_thumbnail(url=clanInfo['badgeUrls']['small'])
        embed.add_field(name=f"pourcentage de destruction : {clanInfo['destructionPercentage']}%    |     {opponentInfo['destructionPercentage']}%", value=f"**attaques : {clanInfo['stars']}    |     {opponentInfo['stars']}\nil reste : {int(hours)} heures, {int(minutes)} minutes**",  inline=False)
        await ctx.send(embed=embed)
        print(int(currentwar['teamSize']/5))
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
                        clanValue = clanValue + f"**{clanMemberInfo[i]['mapPosition']}. {clanMemberInfo[i]['name']} {'' if len(opponentMemberInfo[i]['attacks']) == 2 else ':crossed_swords:' }** n'a pas encore été attaqué\n\n"
                    except Exception:
                        clanValue = clanValue + f"**{clanMemberInfo[i]['mapPosition']}. {clanMemberInfo[i]['name']} :crossed_swords::crossed_swords:** n'a pas encore été attaqué \n\n"

                try:
                    for z in range(len(clanMemberInfo)):
                        if clanMemberInfo[z]['tag'] == opponentMemberInfo[i]['bestOpponentAttack']['attackerTag']:
                            opponentMemberInfodef = clanMemberInfo[z]['mapPosition']
                            opponentMemberInfodefName = clanMemberInfo[z]['name']
                            break
                    try : 
                        opponentValue = opponentValue + " **{}. {}** {} \n {} \n\n".format(
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
            await channel.send(embed=embeds)
            
                           
    except Exception:
        traceback.print_exc()
        await ctx.send('fesfefsf')

@slash_command(name='gddqdqc', description="visualiser la gdc dun clan")
async def dddc(ctx : SlashContext, ):
    embed =Embed(title='adazdazd')
    embed.add_field(name="Colonne 1", value="Contenu de la colonne 1 Contenu de la colonne 2 \nContenu de la colonne 2 \nContenu de la colonne 2 \nContenu de la colonne 2 \n", inline=True)
    embed.add_field(name="Colonne 2", value="Contenu de la colonne 2 \n Contenu de la colonne 2 \nContenu de la colonne 2 \nContenu de la colonne 2 \nContenu de la colonne 2 \nContenu de la colonne 2 \nContenu de la colonne 2 \nContenu de la colonne 2 \n", inline=True)
    await ctx.send(embed=embed)
@listen()
async def on_component(event: Component):
      print('1')



bot.start()