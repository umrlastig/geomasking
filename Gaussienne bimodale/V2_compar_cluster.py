# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 23:20:56 2020

@author: houfa
"""

import csv

#on lit le fichier CSV de la detection de clusters de la base de données anonymisées
b=open('donnees_detec_clusteragregees75v2batitamp5m.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

##on lit le fichier CSV de la detection de clusters de la base de données non-anonymisées
c=open('donnees_detec_clusterna.csv')
dataCSVNA=csv.reader(c)
listdataCSVNA=list(dataCSVNA)

result=[]
A=[]
NA=[]
numbC=[]
numbCNA=[]
P=[]

for d in range(1,len(listdataCSV)):
    #on récupère le numéro de cluster max de la base de données anonymisée, il faut bien prendre la bonne colonne correspondant à labels
    numbC.append(int(listdataCSV[d][11]))
    
for e in range(1,len(listdataCSVNA)):
    #on récupère le numéro de cluster max de la base de données anonymisée, il faut bien prendre la bonne colonne correspondant à labels
    numbCNA.append(int(listdataCSVNA[e][12]))
    


for k in range(max(numbC)+1):
    #on crée une liste où on range les points dans des listes correspondant à chaque cluster pour la base de données anonymisées
    t=[]
    for i in range(1,len(listdataCSV)):
        if int(listdataCSV[i][11])==k:
            t.append(listdataCSV[i])
    A.append(t)

for k in range(max(numbCNA)+1):
    #on crée une liste où on range les points dans des listes correspondant à chaque cluster pour la base de données non-anonymisées
    t=[]
    for i in range(1,len(listdataCSVNA)):
        if int(listdataCSVNA[i][12])==k:
            t.append(listdataCSVNA[i])
    NA.append(t)   

for k in range(len(NA)):
    m=0
    c=0
    t=[]
    #pour chaque cluster on va chercher le cluster qui a le plus de points communs avec lui
    for n in range(len(A)):
        t.append(0)
    for i in range(len(NA[k])):
        for p in range(len(A)):
            for o in range(len(A[p])):
                if int(NA[k][i][0])==int(A[p][o][0]):
                    t[p]=t[p]+1
    for w in range(len(t)):
        if t[w]>c:
            c=t[w]
            m=w
            
    P.append([k,len(NA[k]),m,len(A[m]),c])

i=0
deplace=0
for k in range(len(P)):
    #ici on regarde quels clusters ont été appariés avec le même cluster
    if P[k][0]==P[k][2]:
        i+=1
    else:
        deplace+=1

print(P)
print("Même appariement:{}".format(i),"Déplacé ou éparpillé:{}".format(deplace))    


W=[]
zero=0
vingt=0
quante=0
soix=0
for k in range(len(P)):
    #on calcule le taux de préservation des clusters de la base de données non anonymisées
    t=[]
    t.append(P[k][0])
    a=P[k][4]/P[k][1]
    a=a*100
    a=int(a*1000)
    a=(float(a))/1000
    t.append("{}%".format(a))
    W.append(t)
    if a>=75:
        soix+=1
    elif a>=50 and a<75:
        quante+=1
    elif a>=25 and a<50:
        vingt+=1
    else:
        zero+=1
print("Nombre de clusters préservés à plus de 75%:{}".format(soix))
print("Nombre de clusters préservés entre 50 et 75%:{}".format(quante))
print("Nombre de clusters préservés entre 25 et 50%:{}".format(vingt))
print("Nombre de clusters préservés à moins de 25%:{}".format(zero))


 

    
