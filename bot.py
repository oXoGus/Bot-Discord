import json
import sqlite3
import discord
import interactions
import requests
import requests_cache
from discord.ext import commands
from interactions import (Button, ButtonStyle, OptionType, SlashContext, ActionRow, StringSelectMenu, Embed, listen, slash_command, slash_option)
from interactions.api.events import Component
from interactions.ext.paginators import Paginator




conn = sqlite3.connect('CocPlayer.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 


TOKEN = "MTExODUzODE2NDI2OTc1MjMyMA.G9au5g.hReBnZrtyN09Cf0oam5cnzqdj4zhNf64TYa9f8"
intents = discord.Intents.default() # permitions du bot 
intents.message_content = True
intents.presences = True
intents.members = True
bot = interactions.Client(token=TOKEN) # crée le bot

GDCBotheader = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImMzYzAzNDE0LTcyYTQtNDYxZC04YTA1LTA4NTE5NjIzM2ZmNSIsImlhdCI6MTY4Njc2OTk1Niwic3ViIjoiZGV2ZWxvcGVyLzc4ZjdjMzM2LWM2NjUtYzdmYi0xYzhkLTE0YjlhZTY4NjEwMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgxLjY0LjI1NS4xMTkiXSwidHlwZSI6ImNsaWVudCJ9XX0._YGz_-sXj7XvIDH9sM9KqggUVK9VpkwKaYbk87VESOH3WAfMWoOOXkVmvimNrVs-REoSyveWaEjvx5M3S6BAPQ'
} # header pour l'api de clash of clan


################################################
#
#       message when the bot is ready                                                                               
#
################################################

@listen()
async def on_ready(): # quand le bod est pret 
    print(f'{bot.user} est en marche')


################################################
#
#       command fonction                                                                               
#
################################################


@slash_command(name = 'recherchejoueur', description = "rechercher des joueur selon leurs stats") # on crée une commande et on initialiser sont nom et sa description 
async def rechercheJoueur(ctx): # la fonction qui est rattacher a cette commande 
    components: list[ActionRow] = [ActionRow(Button(style=ButtonStyle.BLURPLE, label='les joueurs ayant le plus de trophée', custom_id="trophy", ), Button(style=ButtonStyle.BLURPLE, label='les plus actifs dans les jeux de clans', custom_id="jdc"), Button(style=ButtonStyle.BLURPLE, label='les joueur dans un clan français ayant donné le plus de troupes', custom_id="don"))] #on crée la partie interactive du message 
    await ctx.send('selectionner les statistiques que vous désirer' , components=components,) # on definis le contenue du message et on rattache la partie interactive du message 

@slash_command(name='dazdaz', description='fsefs')
async def fsefsef(ctx):
    components = StringSelectMenu("Pizza", "Pasta", "Burger", "Salad", placeholder='?', min_values=0, max_values=1,)
    await ctx.send('selectionner les statistiques que vous désirer' , components=components,)
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

################################################
#
#        coc profile command
#
################################################
@slash_command(name = 'p', description = "afficher les stats d'un joueur")
@slash_option(name = 'tag', description="tag du joueur", required=True, opt_type=OptionType.STRING )
async def p(ctx : SlashContext, tag : str) :
    try: 
        player_id = tag[1:]
        url = f"https://api.clashofclans.com/v1/players/%23{player_id}"
        response = requests.get(url, headers=GDCBotheader)
        user_json = response.json()  
        user_json = json.dumps(user_json)
        user_json = json.loads(user_json)      
        # embed message
        embed_profile = discord.Embed(title=user_json['name'], description="profil d'"+ user_json['name'], color=discord.Color.random())
        embed_profile.add_field(name="Champ 1", value="Valeur 1", inline=False)
        embed_profile.add_field(name="Champ 2", value="Valeur 2", inline=False) 
        embeds = embed_profile.to_dict()
        await ctx.send(embeds=embeds)
    except KeyError:
        await ctx.send("Erreur : tag du joueur invalide.")
    except Exception: # si il y a une erreur qui n'est pas mentionner plus haut 
        await ctx.send("Erreur : veuillez réessayer plus tard.")




################################################
#
#       ldc command                                                                              
#
################################################
def ldcsetup(ctx): 
    ldc(ctx)
    return ctx
     


# ldc preview in one select channel update if sth is new
def ldc(user_message, war_tag_id, war_tags):
    return
    #init_ldc(user_message)
    #ldc_find_war_tag_id(war_tags, war_tag_id)
# ldc preview in one select channel update if sth is new

async def init_ldc(user_message):
    clan_id = str(user_message[10:])
    clan_api_id = str(user_message[11:])
    url = "https://api.clashofclans.com/v1/clans/%23"+ str(clan_api_id) + "/currentwar/leaguegroup" 
    response = requests.get(url, headers=GDCBotheader)
    setup1 = response.json()
    setup_json = json.dumps(setup1)
    war_tags = json.loads(setup_json)
    return war_tags



def id(user_message):
    clan_id = str(user_message[10:])
    return clan_id

def ldc_udate_data(war_tag_id):
    requests_cache.install_cache('api_cache')
    url = "https://api.clashofclans.com/v1/clanwarleagues/wars/%23" + war_tag_id
    response = requests.get(url, headers=GDCBotheader)
    if not response.from_cache:
        requests_cache.cache_response(response)
    previous_response = requests_cache.get_cache().get(url)
    if previous_response is not None and previous_response.content != response.content:
        ldc_info = requests.get(url, headers=GDCBotheader)
        ldc_info = response.json()
        ldc_info = json.dumps(ldc_info)
        ldc_info = json.loads(ldc_info)
        if float(ldc_info['clan']['destructionPercentage']) < float(ldc_info['opponent']['destructionPercentage']):
            title = ldc_info['clan']['name'] + '  ' +ldc_info['clan']['stars'] + '   vs   ' + '**' + ldc_info['opponent']['stars'] + '**' + '   **' + ldc_info['opponent']['name'] + '**'
        else: 
            title = '**' +ldc_info['clan']['name'] + '**' + '  ' +'**' +ldc_info['clan']['stars']+ '**' + '   vs   ' +  ldc_info['opponent']['stars']  +'  '+  ldc_info['opponent']['name'] 
        embed_profile = discord.Embed(title=title, description=None, color=discord.Color.random())
        embed_profile.add_field(name="Champ 1", value="Valeur 1", inline=True)
        embed_profile.add_field(name="Champ 2", value="Valeur 2", inline=True) 
        return embed_profile





# ldc preview in one select channel update if sth is new
async def ldc_find_war_tag_id(war_tags, clan_id):
    for round in war_tags['rounds']:
        for war_tags in round['warTags']:
            war_tag_id = war_tags
            war_tag_id = str(war_tag_id[1:])
            print(war_tags)
            url = "https://api.clashofclans.com/v1/clanwarleagues/wars/%23" + war_tag_id
            response = requests.get(url, headers=GDCBotheader)
            setup2 = response.json()
            setup2_ = json.dumps(setup2)
            setup2_json = json.loads(setup2_)
            if war_tags == '#0':
                break
            elif (setup2_json['clan']['tag'] == clan_id or setup2_json['opponent']['tag'] == clan_id) and setup2_json['state'] == 'inWar':
                print('real id is: '+ war_tag_id)
            return war_tag_id
                        


bot.start() 









