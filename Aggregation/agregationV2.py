# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 10:27:58 2020

@author: houfa
"""
import csv
import math 

#on lit le fichier CSV des données à anonymisées
b=open('donnees_generees78densiteord.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

#on lit le fichier des centroid de l'unité spatiale(batiment, route, iris) sur lequel on souhaite agréger
c=open('iris78_compte_centerv2id.csv')
dataCSVAG=csv.reader(c)
listdataCSVAG=list(dataCSVAG)

data=[]
for k in range(1,len(listdataCSVAG)):
    #on ajoute chaque centroid dans une liste de listes
    t=[]
    t.append(listdataCSVAG[k])
    data.append(t)
    
def dista(xa,ya,xb,yb):
    #fonction retournant la distance euclidienne d'un couple de deux points
    n=math.sqrt(((xa-xb)**2)+((ya-yb)**2))
    return(n)

for k in range(1,len(listdataCSV)):
    #on va agréger chaque point de la base de données sur le centroid le plus proche
    min=dista(float(listdataCSV[k][9]),float(listdataCSV[k][10]),float(listdataCSVAG[1][2]),float(listdataCSVAG[1][3]))
    d=listdataCSVAG[1]
    for i in range(2,len(listdataCSVAG)):
        if dista(float(listdataCSV[k][9]),float(listdataCSV[k][10]),float(listdataCSVAG[i][2]),float(listdataCSVAG[i][3]))<min:
            min=dista(float(listdataCSV[k][9]),float(listdataCSV[k][10]),float(listdataCSVAG[i][2]),float(listdataCSVAG[i][3]))
            d=listdataCSVAG[i]
    data[int(d[0])].append(listdataCSV[k])

#A ce stade, on a pour chaque centroid les points qui lui sont agrégés dessus
datas=[]
for k in range(len(data)):
    #maintenant pour chaque centroid, on va disposer les points qui lui sont agrégés autour du centroid pour avoir en sortie le même nombre de points
    if len(data[k])>1:
        angle=0
        d=3
        for i in range(1,len(data[k])):
            m=[]
            if angle==(math.pi*2):
                angle=0
                d+=1
            m.append(data[k][i][0])
            m.append(data[k][i][1])
            m.append(data[k][i][2])
            m.append(data[k][i][3])
            m.append(data[k][i][4])
            m.append(data[k][i][5])
            m.append(data[k][i][6])
            m.append(data[k][i][7])
            m.append(data[k][i][8])
            x=float(data[k][0][2])+(d*math.cos(angle))
            y=float(data[k][0][3])+(d*math.sin(angle))
            m.append(x)
            m.append(y)
            datas.append(m)
            angle+=(math.pi/8)
            
#en sortie on a un fichier avec les attributs d'origine de chaque point, et leur nouvelle coordonnées après agrégation     
with open('donnees_agregees78v2iris.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","X","Y"])
    for i in range(len(datas)):
        writer.writerow(datas[i])
            