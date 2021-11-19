# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:08:20 2020

@author: houfa
"""

import csv

#on lit le fichier des données agrégées
b=open('donnees_detec_cluster_agregation75v2bati.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

#on lit le fichier des données non anonymisees avec leur disposition dans les clusters
c=open('donnees_detec_clusterna.csv')
dataCSVNA=csv.reader(c)
listdataCSVNA=list(dataCSVNA)

dataNA=[]
dataAG=[]

for k in range(1,len(listdataCSVNA)):
    #on récupère tous les points de la base non anonymisés qui font partie d'un cluster
    #on trie par groupe chaque point et les autres points qui appartiennent au même cluster
    t=[]
    t.append(listdataCSVNA[k])
    if int((listdataCSVNA[k][12]))!=-1:
        for i in range(1,len(listdataCSVNA)):
            if int(listdataCSVNA[i][12])==int(listdataCSVNA[k][12]) and int(listdataCSVNA[i][0])!=int(listdataCSVNA[k][0]):
                t.append(listdataCSVNA[i])
    dataNA.append(t)
    
for k in range(1,len(listdataCSV)):
    #on récupère tous les points de la base agrégés qui font partie d'un cluster
    #on trie par groupe chaque point et les autres points qui appartiennent au même cluster
    u=[]
    u.append(listdataCSV[k])
    if int(listdataCSV[k][11])!=-1:
        for i in range(1,len(listdataCSV)):
            if int(listdataCSV[i][11])==int(listdataCSV[k][11]) and int(listdataCSV[i][0])!=int(listdataCSV[k][0]):
                u.append(listdataCSV[i])
    dataAG.append(u)

datas=[]

for k in range(len(dataNA)):
    w=0
    new=0
    v=[]
    #on récupère les attributs du point considéré pour la préservation de clusters
    v.append(dataNA[k][0][0])
    v.append(dataNA[k][0][1])   
    v.append(dataNA[k][0][2])
    v.append(dataNA[k][0][3])
    v.append(dataNA[k][0][4])
    v.append(dataNA[k][0][5])
    v.append(dataNA[k][0][6])
    v.append(dataNA[k][0][7])
    v.append(dataNA[k][0][8])
    v.append(dataNA[k][0][9])
    v.append(dataNA[k][0][10])
    #pour chaque point on va voir avec quelle part de points il est toujours lié dans un cluster
    if len(dataNA[k])>1 and len(dataAG[k])>1:
        for i in range(1,len(dataNA[k])):
            if dataNA[k][i] in dataAG[k]:
                w+=1
        new=len(dataAG[k])-w-1
        per=len(dataNA[k])-w-1
        v.append(w)
        v.append(new)
        v.append(per)
        pa=w/len(dataNA[k])
        pa=pa*100
        pa=int(pa*1000)
        pa=(float(pa))/1000
        v.append(pa)
        pn=new/len(dataAG)
        pn=pn*100
        pn=int(pn*1000)
        pn=(float(pn))/1000
        v.append(pn)
        pd=per/len(dataAG[k])
        pd=pd*100
        pd=int(pd*1000)
        pd=(float(pd))/1000
        v.append(pd)
    elif len(dataNA[k])>1 and len(dataAG[k])==1:
        v.append('DEVENU BRUIT')
        new=0
        v.append(new)
        per=len(dataNA[k])-1
        v.append(per)
        pa=0
        v.append(pa)
        pn=0
        v.append(pn)
        pd=0
        v.append(pd)
    elif len(dataNA[k])==1 and len(dataAG[k])>1:
        v.append('ANCIEN BRUIT')
        new=len(dataAG[k])-1
        v.append(new)
        per=0
        v.append(per)
        pa=0
        v.append(pa)
        pn=100
        v.append(pn)
        pd=0
        v.append(pd)
    else:
        v.append('TOUJOURS BRUIT')
        new=0
        v.append(new)
        per=0
        v.append(per)
        pa=100
        v.append(pa)
        pn=0
        v.append(pn)
        pd=0
        v.append(pd)
    datas.append(v)

zeron=0
vingtn=0
quanten=0
soixn=0

zeroc=0
vingtc=0
quantec=0
soixc=0

zerop=0
vingtp=0
quantep=0
soixp=0

db=0
ab=0
tb=0

for k in range(len(datas)):
    if type(datas[k][11])==int:
        if datas[k][14]>=75:
            soixc+=1
        elif datas[k][14]>=50 and datas[k][14]<75:
            quantec+=1
        elif datas[k][14]>=25 and datas[k][14]<50:
            vingtc+=1
        else:
            zeroc+=1
        if datas[k][15]>=75:
            soixn+=1
        elif datas[k][15]>=50 and datas[k][15]<75:
            quanten+=1
        elif datas[k][15]>=25 and datas[k][15]<50:
            vingtn+=1
        else:
            zeron+=1
        if datas[k][16]>=75:
            soixp+=1
        elif datas[k][16]>=50 and datas[k][16]<75:
            quantep+=1
        elif datas[k][16]>=25 and datas[k][16]<50:
            vingtp+=1
        else:
            zerop+=1
    elif datas[k][11]=='DEVENU BRUIT':
        db+=1
    elif datas[k][11]=='ANCIEN BRUIT':
        ab+=1
    else:
        tb+=1
        
print('Statistiques de la clusterisation') 
print(' ')       
print("Nombre de points étant toujours liés à plus de 75% des points de leur ancien cluster:{}".format(soixc))
print("Nombre de points étant toujours liés avec entre 50 et 75% des points de leur ancien cluster:{}".format(quantec))
print("Nombre de points étant toujours liés avec entre 25 et 50% des points de leur ancien cluster:{}".format(vingtc))
print("Nombre de points étant toujours liés à moins de 25% des points de leur ancien cluster:{}".format(zeroc))

print('')
print("Nombre de points étant liés à plus de 75% de nouveaux points dans leur nouveau cluster:{}".format(soixn))
print("Nombre de points étant liés avec entre 50 et 75% de nouveaux points dans leur nouveau cluster:{}".format(quanten))
print("Nombre de points étant liés avec entre 25 et 50% de nouveaux points dans leur nouveau cluster:{}".format(vingtn))
print("Nombre de points étant liés avec moins de 25% de nouveaux points dans leur nouveau cluster:{}".format(zeron))

print('')
print("Nombre de points n'étant plus liés à plus de 75% des points de leur ancien cluster:{}".format(soixp))
print("Nombre de points n'étant plus liés avec entre 50 et 75% des points de leur ancien cluster:{}".format(quantep))
print("Nombre de points n'étant plus liés avec entre 25 et 50% des points de leur ancien cluster:{}".format(vingtp))
print("Nombre de points n'étant plus liés à moins de 25% des points de leur ancien cluster:{}".format(zerop))
        
print('')
print("Nombre de points toujours dans le bruit:{}".format(tb))
print("Nombre de points passés dans le bruit :{}".format(db))
print("Nombre de points n'étant plus dans le bruit':{}".format(ab))
   
    
                
    