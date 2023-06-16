import discord
from discord.ext import commands
import interactions 
import requests
import requests_cache
import json
import sqlite3
from interactions import Button, ButtonStyle, listen
from interactions.api.events import Component

conn = sqlite3.connect('CocPlayer.db') # connection a la base de donnée
cursor = conn.cursor() # creation d'une variable pour interagire avec la base de donnée 
################################################
#
#       bot init                                                                              
#
################################################ 

TOKEN = "MTExODUzODE2NDI2OTc1MjMyMA.G9au5g.hReBnZrtyN09Cf0oam5cnzqdj4zhNf64TYa9f8"
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
bot = interactions.Client(token=TOKEN)


@listen()
async def on_ready():
    print(f"{bot.user} s'est connecté")

@interactions.slash_command(name="my_first_command", description="This is the first command I made!") 
async def my_first_command(ctx):
    components = Button(custom_id="1", style=ButtonStyle.RED, label="Click me",)
    await ctx.send("Hi there!", components=components)

@listen()
async def on_component(event: Component):
      print('1')



bot.start()