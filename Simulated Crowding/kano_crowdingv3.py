# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 15:52:01 2020

@author: houfa
@author: gtouya
"""

import csv
import math
import random
import numpy as np
import psycopg2

# we use a PostGIS database containing the  original addresses to make sure spatial queries are computed quickly
conn = psycopg2.connect(user="postgres", password="postgres", database="geomasking", host="localhost", port="5432")

#on lit le fichier des données anonymisées par simulated crowding
b=open('simulated_crowding75v1.csv')
dataCSVS=csv.reader(b)
listdataCSVS=list(dataCSVS)

#on lit le fichier des données non-anonymisées avec leur disposition dans les clusters
c=open('donnees_detec_clusterna.csv')
dataCSV=csv.reader(c)
listdataCSV=list(dataCSV)


def kano(xa,ya,xb,yb):
    #fonction retournant la valeur de la k-anonymité d'un couple de points non-anonymisé et anonymisé
    cursorK=conn.cursor()
    queryK="Select count(*) from public.ban_75 as b WHERE ST_DWithin(b.geom,ST_SetSRID(ST_Point(%s,%s),2154),ST_Distance(ST_SetSRID(ST_Point(%s,%s),2154),ST_SetSRID(ST_Point(%s,%s),2154)))"
    cursorK.execute(queryK,(xa,ya,xa,ya,xb,yb))
    recordsK= cursorK.fetchall()
    return(int(recordsK[0][0]))

def kano_cluster(xa,ya):
    #fonction retournant la valeur de la k-anonymité d'un couple de points non-anonymisé et anonymisé
    cursorK=conn.cursor()
    queryK="Select * from public.clusters75_hull_count as b WHERE ST_Contains(b.geom,ST_SetSRID(ST_Point(%s,%s),2154))"
    cursorK.execute(queryK,(xa,ya))
    recordsK= cursorK.fetchall()
    return([int(recordsK[0][4]), int(recordsK[0][5])])

def dista(xa,ya,xb,yb):
    #fonction retournant la distance euclidienne d'un couple de points
    n=math.sqrt(((xa-xb)**2)+((ya-yb)**2))
    return(n)
data=[]
bruit=[]

for k in range(1,len(listdataCSV)):
    #on sépare dans deux listes, les points appartenant à un cluster et ceux du 'bruit'
    if int(listdataCSV[k][12])==(-1):
        bruit.append(listdataCSV[k])

for k in range(1,len(listdataCSVS)):
    d=[]
    ka=0
    e=[]
    if int(listdataCSVS[k][11])==-1:
        # for the points outside clusters, we use the (Wang & Kwan, 2020) k-anonymity definition
        for i in range(0,len(bruit)):
            if int(listdataCSVS[k][0])==int(bruit[i][0]):
                ka=kano(float(listdataCSVS[k][9]),float(listdataCSVS[k][10]),float(bruit[i][9]),float(bruit[i][10]))
                e=bruit[i]
        d.append(e[0])
        d.append(e[1])
        d.append(e[2])
        d.append(e[3])
        d.append(e[4])
        d.append(e[5])
        d.append(e[6])
        d.append(e[7])
        d.append(e[8])
        d.append(e[9])
        d.append(e[10])
        d.append(ka)
        d.append(0.0)

    else:
        # for the points inside clusters, the k-anonymity is the number of addresses included in the region covered by the cluster.
        # we also compute the privacy ratio
        # select the cluster that contains this point
        k_ano = kano_cluster(float(listdataCSVS[k][9]),float(listdataCSVS[k][10]))
        e = listdataCSVS[k]
        d.append(e[0])
        d.append(e[1])
        d.append(e[2])
        d.append(e[3])
        d.append(e[4])
        d.append(e[5])
        d.append(e[6])
        d.append(e[7])
        d.append(e[8])
        d.append(e[9])
        d.append(e[10])
        d.append(k_ano[0])
        d.append(k_ano[1]/k_ano[0])

    data.append(d)
    print(d)
    

#en sortie on a un fichier CSV avec les points de la base de données non anonymisées et la valeur de k qui leur ai associé
with open('result_k_crowding75_v1.csv', 'w', newline='') as file:
    print("test")
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","x","y","k"])
    for i in range(len(data)):
        writer.writerow(data[i])