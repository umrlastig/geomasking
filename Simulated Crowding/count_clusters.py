# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:03:33 2020

@author: houfa
"""
import csv 

#on lit le fichier avec la disposition des points dans les clusters
b=open('donnees_detec_clusterna.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

a=[]
#on va chercher le nombre de cluster
for k in range(1,len(listdataCSV)):
    a.append(int(listdataCSV[k][12]))

data=[]
for k in range(max(a)+1):
    #pour chaque cluster, on compte le nombre de points qui lui appartiennent
    t=[k]
    c=0
    for i in range(len(a)):
        if a[i]==k:
            c+=1
    t.append(c)
    data.append(t)

#en sortie on a donc un fichier avec le compte de points dans chaque cluster
with open('count_clusters.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["labels","Nombre"])
    for i in range(len(data)):
        writer.writerow(data[i])
    
