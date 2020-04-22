# Now we have already built: Match (10), Participant (80), Player (68) tables in tftlazy DB
# Now we want to: request by puuid in Player, call their recent 10 tft matches by TFT-MATCH
# https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/QyseHxyW19xv5j7SP7VxoYqib-H5nO4JsMaaOZSipXc1pVGjWDJsKl5Yttrhdf0HaUHIgadSLIiBuw/ids?count=10&api_key=RGAPI-519de4fe-b919-4188-a2cf-abd692d88355

import urllib.request
import urllib.parse
import urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

# If you have a RIOT API key, enter it here
# my API Key, Expires: Mon, Mar 30th, 2020 @ 5:02pm (PT) in 23 hours and 59 minutes
api_key = 'RGAPI-c57d6d2b-9022-4f07-a9a3-671163ddbc16'
serviceurl_puuid = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/'

# TFT DB
conn = sqlite3.connect('tftlazy.sqlite')
cur = conn.cursor()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# define a function to convert tuble to string


def convertTuple(tup):
    str = ''.join(tup)
    return str

# # Driver code
# tuple = ('g', 'e', 'e', 'k', 's')
# str = convertTuple(tuple)
# print(str)


# read from Player table
cur.execute("SELECT puuid FROM Player")
rows = cur.fetchall()
# print(type(rows))
print(len(rows))
for player in rows:
    # print(type(row),row)  row is a tuple looks like this <class 'tuple'> ('v599oPunHZPeOPKgKDH_Im75nehkTjg22yJh6FIfyizv4CHkEym_mBWMWosZCxri_xyF-QlbvActsg',)
    puuid = convertTuple(player)
    # print(type(puuid),puuid)
    url = serviceurl_puuid + puuid+"/ids?count=10&api_key="+api_key
    # https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/znalUxrcsHcva5mcpAk--0QHpYAT13fPoE2JnKZUBMbDaPwJZb0MIhYh3xQD3jj2IZr9pDaTcs14Xw/ids?count=10&api_key=RGAPI-519de4fe-b919-4188-a2cf-abd692d88355
    print('Retrieving', url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    # print(type(js),js) #js is a list of 10 match_id
    for match in js:
        match_id = match
        cur.execute(
            'INSERT OR IGNORE INTO Match (match_id) VALUES ( ? )', (match_id,))

conn.commit()
