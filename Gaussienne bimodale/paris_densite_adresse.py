# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:24:01 2020

@author: houfa
"""

import psycopg2
import csv

conn = psycopg2.connect(user="postgres", password="postgres", database="donnees_hospitalieres_COVID19", host="localhost", port="5432")

k=[]
b=open('donnees_genereesdensite.csv')
#on place les données non anonymisées dans une liste
dataCSV=csv.reader(b)
recordsDG=list(dataCSV)

for i in range(len(list(recordsDG))):
    
    ki=[]
    cursorK=conn.cursor()
    queryK="Select count(*) from public.bano7593 as b WHERE ST_DWithin(b.geom,ST_SetSRID(ST_Point(%s,%s),2154),1000)" 
    cursorK.execute(queryK,(recordsDG[i][9],recordsDG[i][10]))
    recordsK= cursorK.fetchall()
    
    ki.append(recordsDG[i][0])
    ki.append(recordsDG[i][1])
    ki.append(recordsDG[i][2])
    ki.append(recordsDG[i][3])
    ki.append(recordsDG[i][4])
    ki.append(recordsDG[i][5])
    ki.append(recordsDG[i][6])
    ki.append(recordsDG[i][7])
    ki.append(recordsDG[i][8])
    ki.append(recordsDG[i][9])
    ki.append(recordsDG[i][10])
    ki.append(recordsK[0][0])
    print(ki)
    k.append(ki)
    
with open('donnees_genereesdensite.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","x","y","densite"])
    for i in range(len(k)):
        writer.writerow(k[i])