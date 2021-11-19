# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:33:19 2020

@author: houfa
"""
import csv
import numpy as np
import random
import math
import psycopg2

#on établit une connexion avec la base postgreSQL
conn = psycopg2.connect(user="postgres", password="postgres", database="donnees_hospitalieres_COVID19", host="localhost", port="5432")

b=open('donnees_genereesdensite.csv')
#on place les données à anonymisées dans une liste
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

def kano(xa,ya,xb,yb):
    #fonction permettant de calculer la k-anonymité d'un couple de points non anonymisé et anonymisé
    cursorK=conn.cursor()
    queryK="Select count(*) from public.bano7593 as b WHERE ST_DWithin(b.geom,ST_SetSRID(ST_Point(%s,%s),2154),ST_Distance(ST_SetSRID(ST_Point(%s,%s),2154),ST_SetSRID(ST_Point(%s,%s),2154)))" 
    cursorK.execute(queryK,(xa,ya,xa,ya,xb,yb))
    recordsK= cursorK.fetchall()
    return(int(recordsK[0][0]))

data=[]

def gaussian(mu,et,n):
    #fonction retournant une valeur selon une gaussienne avec les paramètres d'entrée
    values=np.random.normal(mu,et,n)
    return values



for k in range(1,len(listdataCSV)):
    #on tire des valeurs selon des gaussiennes centrées sur 30 et 60m
    a=gaussian(30,5,1)
    o=gaussian(60,10,1)
    
    #on reprend les attributs de la donnée
    inter=[]
    inter.append(listdataCSV[k][0])
    inter.append(listdataCSV[k][1])
    inter.append(listdataCSV[k][2])
    inter.append(listdataCSV[k][3])
    inter.append(listdataCSV[k][4])
    inter.append(listdataCSV[k][5])
    inter.append(listdataCSV[k][6])
    inter.append(listdataCSV[k][7])
    inter.append(listdataCSV[k][8])
    
    #on tire un nombre en 0 et 1 au hasard pour choisir avec une chance sur deux quelle valeur de gaussienne est utilisée
    aleat=random.random()
    #on tire un angle au hasard
    angle=random.random()*math.pi*2
    
    #Selon la valeur de densité, on va renforcer ou diminuer la distance à ajouter aux coordonnées
    if int(listdataCSV[k][11])>=7000:
        #on ajoute à chaque coordonnée, les valeurs correspondant à la distance et l'angle tirées
        if aleat>=0.5:
            x=a[0]*math.cos(angle)*0.6
            y=a[0]*math.sin(angle)*0.6
            
        else:
            x=o[0]*math.cos(angle)*0.6
            y=o[0]*math.sin(angle)*0.6

            
    elif int(listdataCSV[k][11])<7000 and int(listdataCSV[k][11])>=6000:
        if aleat>=0.5:
            x=a[0]*math.cos(angle)*0.8
            y=a[0]*math.sin(angle)*0.8
 
        else:
            x=o[0]*math.cos(angle)*0.8
            y=o[0]*math.sin(angle)*0.8

            
    elif int(listdataCSV[k][11])<5+6000 and int(listdataCSV[k][11])>=4500:
        if aleat>=0.5:
            x=a[0]*math.cos(angle)
            y=a[0]*math.sin(angle)

        else:
            x=o[0]*math.cos(angle)
            y=o[0]*math.sin(angle)

    
    elif int(listdataCSV[k][11])<4500 and int(listdataCSV[k][11])>=2500:
        if aleat>=0.5:
            x=a[0]*math.cos(angle)*1.25
            y=a[0]*math.sin(angle)*1.25

        else:
            x=o[0]*math.cos(angle)*1.25
            y=o[0]*math.sin(angle)*1.25

    elif int(listdataCSV[k][11])<2500 and int(listdataCSV[k][11])>=1800:
        if aleat>=0.5:
            x=a[0]*math.cos(angle)*1.5
            y=a[0]*math.sin(angle)*1.5

        else:
            x=o[0]*math.cos(angle)*1.5
            y=o[0]*math.sin(angle)*1.5

    elif int(listdataCSV[k][11])<1800 and int(listdataCSV[k][11])>=1000:
        if aleat>=0.5:
            x=a[0]*math.cos(angle)*1.75
            y=a[0]*math.sin(angle)*1.75

        else:
            x=o[0]*math.cos(angle)*1.75
            y=o[0]*math.sin(angle)*1.75

    else:
        if aleat>=0.5:
            x=a[0]*math.cos(angle)*2
            y=a[0]*math.sin(angle)*2

        else:
            x=o[0]*math.cos(angle)*2
            y=o[0]*math.sin(angle)*2

    #on calcule la k-anonymité après déplacement du point dans une direction et la direction opposée
    #on ajoute à la base le point pour laquelle la direction donne la meilleure k-anonymité
    if kano(float(listdataCSV[k][9])+x,float(listdataCSV[k][10])+y,float(listdataCSV[k][9]),float(listdataCSV[k][10]))>=kano(float(listdataCSV[k][9])-x,float(listdataCSV[k][10])-y,float(listdataCSV[k][9]),float(listdataCSV[k][10])):
        inter.append(float(listdataCSV[k][9])+x)
        inter.append(float(listdataCSV[k][10])+y)
    else:
        inter.append(float(listdataCSV[k][9])-x)
        inter.append(float(listdataCSV[k][10])-y)
                        
    #on ajoute à la donnée, les nouvelles coordonnées   
    data.append(inter)

#on crée un fichier CSV avec les nouvelles données   
with open('donnees_anonymisees_bimodal75kmin2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","X","Y"])
    for i in range(len(data)):
        writer.writerow(data[i])