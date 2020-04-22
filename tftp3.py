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
serviceurl_match = 'https://americas.api.riotgames.com/tft/match/v1/matches/'

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


# read from Match table
cur.execute("SELECT match_id FROM Match")
rows = cur.fetchall()
# print(type(rows),type(rows[0]))
print(len(rows))

count = 0
for match in rows:
    # print(type(row),row)  row is a tuple looks like this <class 'tuple'> ('v599oPunHZPeOPKgKDH_Im75nehkTjg22yJh6FIfyizv4CHkEym_mBWMWosZCxri_xyF-QlbvActsg',)
    match_id = convertTuple(match)

    # check if we have already got the patricipants info for this match_id
    cur.execute(
        "SELECT data_version FROM Participant WHERE match_id= ?", (match_id, ))

    try:
        row = cur.fetchone()[0]
        print("Found in database ", match_id)
        continue
    except:
        pass

    url = serviceurl_match + match_id+"?api_key="+api_key
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    # print(type(js),js) #js is a list of 10 match_id
    data_version = js["metadata"]["data_version"]
    cur.execute('INSERT OR IGNORE INTO Match (match_id,data_version) VALUES ( ?,? )',
                (match_id, data_version))

    for key in js["info"]["participants"]:
        # print(type(key),key)
        placement = key["placement"]
        puuid = key["puuid"]
        # print(type(placement),placement)

        try:
            trait1 = key["traits"][0]["name"]
        except IndexError:
            trait1 = "NULL"
            pass

        try:
            trait1_n = key["traits"][0]["num_units"]
        except IndexError:
            trait1_n = "NULL"
            pass

        try:
            trait2 = key["traits"][1]["name"]
        except IndexError:
            trait2 = "NULL"
            pass

        try:
            trait2_n = key["traits"][1]["num_units"]
        except IndexError:
            trait2_n = "NULL"
            pass

        try:
            trait3 = key["traits"][2]["name"]
        except IndexError:
            trait3 = "NULL"
            pass

        try:
            trait3_n = key["traits"][2]["name"]
        except IndexError:
            trait3_n = "NULL"
            pass

        try:
            trait4 = key["traits"][3]["name"]
        except IndexError:
            trait4 = "NULL"
            pass

        try:
            trait4_n = key["traits"][3]["name"]
        except IndexError:
            trait4_n = "NULL"
            pass

        try:
            trait5 = key["traits"][4]["name"]
        except IndexError:
            trait5 = "NULL"
            pass

        try:
            trait5_n = key["traits"][4]["name"]
        except IndexError:
            trait5_n = "NULL"
            pass

        try:
            trait6 = key["traits"][5]["name"]
        except IndexError:
            trait6 = "NULL"
            pass

        try:
            trait6_n = key["traits"][5]["num_units"]
        except IndexError:
            trait6_n = "NULL"
            pass

        try:
            trait7 = key["traits"][6]["name"]
        except IndexError:
            trait7 = "NULL"
            pass

        try:
            trait7_n = key["traits"][6]["num_units"]
        except IndexError:
            trait7_n = "NULL"
            pass

        try:
            trait8 = key["traits"][7]["name"]
        except IndexError:
            trait8 = "NULL"
            pass

        try:
            trait8_n = key["traits"][7]["num_units"]
        except IndexError:
            trait8_n = "NULL"
            pass

        try:
            trait9 = key["traits"][8]["name"]
        except IndexError:
            trait9 = "NULL"
            pass

        try:
            trait9_n = key["traits"][8]["num_units"]
        except IndexError:
            trait9_n = "NULL"
            pass

        try:
            trait10 = key["traits"][9]["name"]
        except IndexError:
            trait10 = "NULL"
            pass

        try:
            trait10_n = key["traits"][9]["num_units"]
        except IndexError:
            trait10_n = "NULL"
            pass

        cur.execute(
            'INSERT OR IGNORE INTO Participant (match_id,puuid,placement,trait1,trait1_n,trait2,trait2_n,trait3,trait3_n,trait4 ,trait4_n,trait5,trait5_n,trait6,trait6_n,trait7,trait7_n,trait8,trait8_n ,trait9,trait9_n,trait10,trait10_n) VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (match_id, puuid, placement, trait1, trait1_n, trait2, trait2_n, trait3, trait3_n, trait4, trait4_n, trait5, trait5_n, trait6, trait6_n, trait7, trait7_n, trait8, trait8_n, trait9, trait9_n, trait10, trait10_n))

    for player in js["metadata"]["participants"]:
        cur.execute(
            'INSERT OR IGNORE INTO Player (puuid) VALUES ( ? )', (player,))

    conn.commit()

    count = count+1

    if count % 100 == 0:
        print('Pausing for a bit...')
        time.sleep(10)

conn.commit()
#cur.execute('SELECT match_id,data_version FROM Match LIMIT 5')
cur.execute('SELECT * FROM Participant LIMIT 5')
view = cur.fetchone()
print(view)

old = ['OC1_284720127', 'OC1_285024403', 'OC1_285013753', 'OC1_285004984',
       'OC1_284999599', 'OC1_284828342']  # these matches are old version
