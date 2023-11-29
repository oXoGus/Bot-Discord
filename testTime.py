import interactions, json, requests, traceback
from interactions import (Button, ButtonStyle, OptionType, SlashContext, ActionRow, StringSelectMenu, CustomEmoji, Embed, PartialEmoji,Intents, listen, slash_command, slash_option)
from interactions.api.events import Component
from interactions.ext.paginators import Paginator
from config import TOKEN, GDCBotheader, laboHeader, clanHeader, infoGeneraleHeader
from datetime import datetime, timezone, timedelta
from dateutil import parser



bot = interactions.Client(token=TOKEN, intents=Intents.ALL) # crée le bot



################################################
#
#       message when the bot is ready
#
################################################




@listen()
async def on_ready(): # quand le bod est pret 
    print(f'{bot.user} est en marche') #afficher ceci dans le terminal





@slash_command(name='gdc', description="visualiser la gdc dun clan")
@slash_option(name='id', description='le tag du clan', required=True, opt_type=OptionType.STRING)
async def gdc(ctx : SlashContext, id):
    channel = ctx.channel
    id=id[1:]
    url = f"https://api.clashofclans.com/v1/clans/%23{id}/currentwar"
    try:
        response = requests.get(url, headers=GDCBotheader) 
        currentwar = response.json()  
        currentwar = json.dumps(currentwar)
        currentwar = json.loads(currentwar)
        starTime = parser.parse(currentwar['endTime'])

        # Convert timedelta to seconds
        timestamp = int(starTime.timestamp())

        await ctx.send(content=f"<t:{timestamp}:R>")
    except Exception as e :
        traceback.print_exc()
        

bot.start() 