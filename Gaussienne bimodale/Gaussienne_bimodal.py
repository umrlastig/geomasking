# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:33:19 2020

@author: houfa
"""
import csv
import numpy as np
import random
import math

b=open('donnees_generees93id.csv')
#on place les données à anonymisées dans une liste
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)



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
    if aleat>=0.5:
        #on ajoute à chaque coordonnée, les valeurs correspondant à la distance et l'angle tirées
        x=a[0]*math.cos(angle)
        y=a[0]*math.sin(angle)
        inter.append(float(listdataCSV[k][9])+x)
        inter.append(float(listdataCSV[k][10])+y)
    else:
        #on ajoute à chaque coordonnée, les valeurs correspondant à la distance et l'angle tirées
        x=o[0]*math.cos(angle)
        y=o[0]*math.sin(angle)
        inter.append(float(listdataCSV[k][9])+x)
        inter.append(float(listdataCSV[k][10])+y)
    
    #on ajoute à la donnée, les nouvelles coordonnées    
    data.append(inter)

#on crée un fichier CSV avec les nouvelles données
with open('donnees_anonymisees_bimodal.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","X","Y"])
    for i in range(len(data)):
        writer.writerow(data[i])