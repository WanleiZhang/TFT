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

cur.execute('''
CREATE TABLE IF NOT EXISTS Player(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    puuid TEXT NOT NULL UNIQUE
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Match(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    match_id TEXT NOT NULL,
    data_version TEXT
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Participant(
    match_id TEXT NOT NULL,
    puuid TEXT NOT NULL,
    placement,
    trait1 TEXT,
    trait1_n TEXT,
    trait2 TEXT,
    trait2_n TEXT,
    trait3 TEXT,
    trait3_n TEXT,
    trait4 TEXT,
    trait4_n TEXT,
    trait5 TEXT,
    trait5_n TEXT,
    trait6 TEXT,
    trait6_n TEXT,
    trait7 TEXT,
    trait7_n TEXT,
    trait8 TEXT,
    trait8_n INTEGER,
    trait9 TEXT,
    trait9_n TEXT,
    trait10 TEXT,
    trait10_n TEXT,
    PRIMARY KEY (match_id,puuid)
)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Check to see if we are already in progress...
fh = open("matchseed.data")
count = 0
for line in fh:
    if count > 10:
        print('Retrieved 10 seed matches, restart to retrieve more')
        break

    match_id = line.strip()
    print('')
    cur.execute("SELECT data_version FROM Match WHERE match_id= ?", (match_id, ))

    try:
        row = cur.fetchone()[0]
        print("Found in database ", match_id)
        continue
    except:
        pass

    url = serviceurl_match + match_id+"?api_key="+api_key
    # https://americas.api.riotgames.com/tft/match/v1/matches/OC1_285896624?api_key=RGAPI-75dbb1e3-41f7-443b-8b17-e12171bd25d5
    print('Retrieving', url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    count = count + 1

    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    # if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
    #     print('==== Failure To Retrieve ====')
    #     print(data)
    #     break
    data_version = js["metadata"]["data_version"]
    match_id = js["metadata"]["match_id"]
    cur.execute('INSERT OR IGNORE INTO Match (match_id,data_version) VALUES ( ?,? )',
                (match_id, data_version))

    for key in js["info"]["participants"]:
        # print(type(key),key)
        placement = key["placement"]
        puuid = key["puuid"]
        # print(type(placement),placement)
        trait1 = key["traits"][0]["name"]
        trait1_n = key["traits"][0]["num_units"]
        trait2 = key["traits"][1]["name"]
        trait2_n = key["traits"][1]["num_units"]
        trait3 = key["traits"][2]["name"]
        trait3 = key["traits"][2]["name"]
        trait3_n = key["traits"][2]["num_units"]
        trait4 = key["traits"][3]["name"]
        trait4_n = key["traits"][3]["num_units"]
        trait5 = key["traits"][4]["name"]
        trait5_n = key["traits"][4]["num_units"]
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
    # if count % 10 == 0 :
    #     print('Pausing for a bit...')
    #     time.sleep(5)
conn.commit()
#cur.execute('SELECT match_id,data_version FROM Match LIMIT 5')
cur.execute('SELECT * FROM Participant LIMIT 5')
view = cur.fetchone()
print(view)
