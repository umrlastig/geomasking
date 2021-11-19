# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:57:00 2020

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

c=open('donnees_anonymisees_bimodal.csv')
#on place les données anonymisées dans une liste
dataCSV=csv.reader(c)
recordsDGA=list(dataCSV)


for i in range(1, len(list(recordsDG))):
    
    ki=[]
    
    #on calcule la k-anonymité pour chaque couple de points non anonymisé/anonymisé
    cursorK=conn.cursor()
    queryK="Select count(*) from public.bano7593 as b WHERE ST_DWithin(b.geom,ST_SetSRID(ST_Point(%s,%s),2154),ST_Distance(ST_SetSRID(ST_Point(%s,%s),2154),ST_SetSRID(ST_Point(%s,%s),2154)))" 
    cursorK.execute(queryK,(recordsDGA[i][9],recordsDGA[i][10],recordsDGA[i][9],recordsDGA[i][10],recordsDG[i][9],recordsDG[i][10]))
    recordsK= cursorK.fetchall()

    #on ajoute les attributs du point considéré et ses coordonnées anonymisées
    ki.append(recordsDGA[i][0])
    ki.append(recordsDGA[i][1])
    ki.append(recordsDGA[i][2])
    ki.append(recordsDGA[i][3])
    ki.append(recordsDGA[i][4])
    ki.append(recordsDGA[i][5])
    ki.append(recordsDGA[i][6])
    ki.append(recordsDGA[i][7])
    ki.append(recordsDGA[i][8])
    ki.append(recordsDGA[i][9])
    ki.append(recordsDGA[i][10])
    
    if recordsK[0][0]==0:
        #dans d'extrêmement rare cas, le calcul peut donner 0 ce qui est une erreur, on ajoute juste 0.5m à la distance et le calcul sera bon
        cursorKs=conn.cursor()
        queryKs="Select count(*) from public.bano7593 as b WHERE ST_DWithin(b.geom,ST_SetSRID(ST_Point(%s,%s),2154),ST_Distance(ST_SetSRID(ST_Point(%s,%s),2154),ST_SetSRID(ST_Point(%s,%s),2154))+0.5)"
        cursorKs.execute(queryKs,(recordsDGA[0][9],recordsDGA[0][10],recordsDGA[0][9],recordsDGA[0][10],recordsDG[i][9],recordsDG[i][10]))
        recordsKs= cursorKs.fetchall()
        ki.append(recordsKs[0][0])
    else:
        ki.append(recordsK[0][0])
    k.append(ki)
    print(ki)

#en sortie on se retrouve avec un fichier CSV avec chaque point anonymisé et sa valeur de k-anonymité
with open('result_k_bimodal.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","x","y","k"])
    for i in range(len(k)):
        writer.writerow(k[i])
