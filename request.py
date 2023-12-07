import requests, json, os, datetime
from config import GDCBotheader

path = f"/home/mathis/Desktop/dev/GDCBot/request/request{datetime.datetime.now()}.json"


resp = requests.get(url="https://api.clashofclans.com/v1/players/%23CV99LRJ2", headers=GDCBotheader)
resp = resp.json()

#with open(path, "w")  as ficherJSON:
json.dumps(resp, indent = 4)
print(resp)