import requests
import json
import time
import random
import string
import sqlite3
import time
import datetime
from cachetools import TTLCache
from datetime import datetime, timedelta

searchClanHeader = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdlMGI2MzZhLTA3ZjAtNDZmNy1iYzg2LTM2ZjI5ZDAzODFjZSIsImlhdCI6MTY4NjQxNDMwOCwic3ViIjoiZGV2ZWxvcGVyLzc4ZjdjMzM2LWM2NjUtYzdmYi0xYzhkLTE0YjlhZTY4NjEwMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgxLjY0LjI1NS4xMTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.9IU9v1-2NqfOpN5s55zElfw28OdBPqBXAHQAC44MNns5DgoMPeFfDFP-Y2txMy0I-N6g522jN7qmT91lc_D-lw'
}

searchPlayerHeader = {
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUzZWM1MzUxLWI1NjktNDY5NC04ODM5LWM2YTkzY2YzZTMxNSIsImlhdCI6MTY4NjQxNDMyNywic3ViIjoiZGV2ZWxvcGVyLzc4ZjdjMzM2LWM2NjUtYzdmYi0xYzhkLTE0YjlhZTY4NjEwMiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgxLjY0LjI1NS4xMTkiXSwidHlwZSI6ImNsaWVudCJ9XX0.iVl9N2k_85Wio9ZvBVv36bzHyoTYjWYQeXuvdmogIEk4gFiVfSKbHF_fsgjEqe1Yd81Bn2zqzHK6wQQ_xEwt0A'
}


class GDCUpdate : 

    def __init__(self, clan_tag):
        self.clan_tag = clan_tag

    def get_clan_data(self):
            url = f"https://api.clashofclans.com/v1/clans/{self.clan_tag}"
            headers = searchClanHeader
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                clan_data = response.json()
                clan_data = json.dumps(clan_data)
                clan_data = json.loads(clan_data)
                return clan_data
            
            else:    # Gérer les erreurs de requête
                pass

i=5
while i>2:
    i =i-1
    print(i)
clanWarStatus = 1
while not clanWarStatus == 'over':