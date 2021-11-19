# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 14:28:13 2020

@author: houfa
"""

import numpy as np
import random
import csv
import math

from shapely.geometry import Polygon, Point, LineString

#on lit le fichier CSV correspondant aux sommets formant les clusters de la base de données non anonymisées
b=open('sommet_cluster75.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

#on lit le fichier correspondant au nombre de points appartenant à chaque cluster
c=open('count_clusters.csv')
dataCSVC=csv.reader(c)
listdataCSVC=list(dataCSVC)

#on lit le fichier donnant la disposition des points non anonymisés dans les cluster
d=open('donnees_detec_clusterna.csv')
dataCSVN=csv.reader(d)
listdataCSVN=list(dataCSVN)


def gaussian(mu,et,n):
    #fonction retournant une valeur aléatoire selon une gaussienne
    values=np.random.normal(mu,et,n)
    return values

polygons=[]

for k in range(int(listdataCSVC[len(listdataCSVC)-1][0])+1):
    #on reforme à l'aide des sommets de chaque cluster, les polygones formant chaque cluster
    t=[k,int(listdataCSVC[k+1][1])]
    polyg=[]
    for i in range(1,len(listdataCSV)):
        if int(listdataCSV[i][0])==k:
            polyg.append((float(listdataCSV[i][8]), float(listdataCSV[i][9])))

    poly = Polygon(polyg)
    t.append(poly)
    polygons.append(t)
   


def random_points_within(poly, num_points,labels):
    #nouvelle version de la fonction retournant un certain nombre de points aléatoires étant contenus dans le polygone en entrée
    #dans cette version les points retournés sont en dehors des zones interdites
    min_x, min_y, max_x, max_y = poly.bounds
    ajoutable=True
    points = []
    compte=0

    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if (poly.contains(random_point)):
            points.append(random_point)
                
    return points

datas=[]


for k in range(len(polygons)):
    #pour chaque polygone de cluster on fait tourner la fonction random points pour créer des points aléatoirement
    points = random_points_within(polygons[k][2],polygons[k][1],k)
    print(k)
    for p in points:
        #les points crées aléatoirement n'ont pas d'attribut on met donc tout à 0 pour garder le même formalisme pour toutes les données
        u=[0,0,0,0,0,0,0,0,0]
        u.append(p.x)
        u.append(p.y)
        u.append(polygons[k][0])
        datas.append(u)
        
compte=0
for k in range(1,len(listdataCSVN)):
    v=[]
    #pour les points n'appartenant à aucun cluster on applique la méthode d'anonymisation par gaussienne bimodale de base
    if int(listdataCSVN[k][12])==-1:
        compte+=1
        a=gaussian(30,5,1)
        o=gaussian(60,10,1)
        v.append(listdataCSVN[k][0])
        v.append(listdataCSVN[k][1])
        v.append(listdataCSVN[k][2])
        v.append(listdataCSVN[k][3])
        v.append(listdataCSVN[k][4])
        v.append(listdataCSVN[k][5])
        v.append(listdataCSVN[k][6])
        v.append(listdataCSVN[k][7])
        v.append(listdataCSVN[k][8])
        
        aleat=random.random()
        angle=random.random()*math.pi*2
        if aleat>=0.5:
            x=a[0]*math.cos(angle)
            y=a[0]*math.sin(angle)
            v.append(float(listdataCSVN[k][9])+x)
            v.append(float(listdataCSVN[k][10])+y)
            v.append(-1)
            datas.append(v)
        else:
            x=o[0]*math.cos(angle)
            y=o[0]*math.sin(angle)
            v.append(float(listdataCSVN[k][9])+x)
            v.append(float(listdataCSVN[k][10])+y)
            v.append(-1)
            datas.append(v)

print(len(datas))    
    
#en sortie on a nos données anonymisées correctement avec le formalisme de départ 
with open('simulated_crowding75v2_3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","X","Y","labels"])
    for i in range(len(datas)):
        writer.writerow(datas[i])
