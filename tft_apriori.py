import sqlite3
import json
import codecs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from apyori import load_transactions

old = ['OC1_284720127', 'OC1_285024403', 'OC1_285013753', 'OC1_285004984',
       'OC1_284999599', 'OC1_284828342']  # these matches are old version

conn = sqlite3.connect('tftlazy.sqlite')
cur = conn.cursor()

cur.execute('SELECT placement,trait1,trait2,trait3,trait4,trait5,trait6,trait7,trait8,trait9,trait10 FROM Participant WHERE match_id NOT IN (SELECT match_id FROM InvalidMatch)')
rows = cur.fetchall()

df = pd.DataFrame(rows)

df.columns = ['placement',

              ]
# print(df)

# dataTypeSeries = df.dtypes
# print('Data type of each column of df :')
# print(dataTypeSeries)

df_win = df[df['placement'] <= 4]

df_win.to_csv('D:/DataProjects/TFT/dfwin.csv', index=False)
# print(len(df_win))
# print(df_win.head())

# #convert the df into a list of list
# records = []
# for i in range(0, 3002):
#     records.append([str(df_win.values[i,j]) for j in range(0, 11)])

# #print(records)

# rules=apriori(records,
#              min_support=0.1,
#              min_confidence=0.90,
#              min_lift=1.0,
#              min_length=2,
#              max_length=None)

# results=list(rules)

# #print(results)
# print(len(results),type(results))

# print(results[0:5])
