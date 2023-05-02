import discord
import requests

TOKEN = "MTEwMTg5MTMyMjE4MjM4OTg4Mg.GzVAuO.ssVVhCxsnBVI9YPhrUr_-9ur5itG753SNEsEhY"
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)


header = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z 2FtZWFwaSIsImp0aSI6ImM0Zjc1NjMyLWYzOTMtNDI2OC1iOTJiLTI5NDRhY2ZlZDdjZiIsImlhdCI6MTY4Mjk3NjcyMywic3ViIjoiZGV2ZWxvcGVyLzc4ZjdjMzM2LWM2NjUtYzdmYi0xYzhk LTE0YjlhZTY4NjEwMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgxLjY0L jI1NS4xMTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.3iIDTxjrwealyPNWIDmFpjSCvJ5-ZxRdWWFEFHPUUwL1ePSMWcGd1kQ57ajTPBJzvyacwIymWZogGB6I4akywA'
}
def get_user(player_id) -> str :
    url = "https://api.clashofclans.com/v1/players/%23" + str(player_id)
    response = requests.get(url, headers=header)
    user_json = response.json()
    user_name_json = user_json['name']
    return(user_name_json)

@client.event
async def on_ready():
    print(f'{client.user} est en marche')

@client.event
async def on_message(message):
    user_message = str(message.content)
    channel = str(message.channel)

    if user_message.startswith("?p") :
        player_id = str(user_message.split()[1])
        print(get_user(player_id))
        await message.channel.send(content=get_user(player_id))

client.run(TOKEN)  









