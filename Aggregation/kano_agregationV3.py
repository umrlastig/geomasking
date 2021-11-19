# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 14:38:29 2020

@author: houfa
"""

import csv
import math
import psycopg2

conn = psycopg2.connect(user="postgres", password="postgres", database="donnees_hospitalieres_COVID19", host="localhost", port="5432")

#on lit le fichier des données non anonymisees
b=open('donnees_generees78densiteord.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

#on lit le fichier des données agrégées
c=open('donnees_agregees78v2iris_ord.csv')
dataCSVAG=csv.reader(c)
listdataCSVAG=list(dataCSVAG)

#on lit le fichier des centroids sur lesquels on a agrégés
d=open('iris78_compte_centerv2id.csv')
dataCSVC=csv.reader(d)
listdataCSVC=list(dataCSVC)

def kano(xa,ya,xb,yb):
    #fonction retournant la valeur de la k-anonymité d'un couple de points non-anonymisé et anonymisé
    u=[]
    cursorK=conn.cursor()
    queryK="Select * from public.bano7893 as b WHERE ST_DWithin(b.geom,ST_SetSRID(ST_Point(%s,%s),2154),ST_Distance(ST_SetSRID(ST_Point(%s,%s),2154),ST_SetSRID(ST_Point(%s,%s),2154)))" 
    cursorK.execute(queryK,(xa,ya,xa,ya,xb,yb))
    recordsK= cursorK.fetchall()
    for k in range(len(list(recordsK))):
        u.append(list(recordsK[k]))
    return(u)
    

def dista(xa,ya,xb,yb):
    #fonction retournant la distance euclidienne entre un couple de points 
    n=math.sqrt(((xa-xb)**2)+((ya-yb)**2))
    return(n)

def irisvoisin(xa,ya):
        #fonction retournant le centroid le plus proche du point considéré 
        min=dista(xa,ya,float(listdataCSVC[1][2]),float(listdataCSVC[1][3]))
        e=listdataCSVC[1]
        for i in range(2,len(listdataCSVC)):
            if dista(xa,ya,float(listdataCSVC[i][2]),float(listdataCSVC[i][3]))<min:
                min=dista(xa,ya,float(listdataCSVC[i][2]),float(listdataCSVC[i][3]))
                e=listdataCSVC[i]
        return(e)
        
    
couple=[]

data=[]

for k in range(1,len(listdataCSV)):
    #pour chaque point, on récupère ses attributs
    v=[]
    w=0
    t=[]
    t.append(listdataCSV[k][0])
    t.append(listdataCSV[k][1])
    t.append(listdataCSV[k][2])
    t.append(listdataCSV[k][3])
    t.append(listdataCSV[k][4])
    t.append(listdataCSV[k][5])
    t.append(listdataCSV[k][6])
    t.append(listdataCSV[k][7])
    t.append(listdataCSV[k][8])
    t.append(listdataCSVAG[k][9])
    t.append(listdataCSVAG[k][10])
    v.append(t)
    
    #on cherche les points de la bano inclues dans la k-anonymité du point
    w=kano(float(listdataCSVAG[k][9]),float(listdataCSVAG[k][10]),float(listdataCSV[k][9]),float(listdataCSV[k][10]))
    for i in range(len(w)):
        #on ne garde que ceux qui ont le même centroide le plus proche, donc qui auraient été agrégés sur le même centroide
        if irisvoisin(float(listdataCSV[k][9]),float(listdataCSV[k][10]))==irisvoisin(float(w[i][6]),float(w[i][7])):
            v.append(w[i])
    print(v[0],len(v)-1)
    data.append(v)

datas=[]    
for k in range(len(data)):
    #pour chaque point on récupère les attributs et la longueur de la liste des points de la k_anonymité qui correspond à la valeur de la k_anonymité
    f=[]
    f.append(data[k][0][0])
    f.append(data[k][0][1])
    f.append(data[k][0][2])
    f.append(data[k][0][3])
    f.append(data[k][0][4])
    f.append(data[k][0][5])
    f.append(data[k][0][6])
    f.append(data[k][0][7])
    f.append(data[k][0][8])
    f.append(data[k][0][9])
    f.append(data[k][0][10])
    f.append(len(data[k])-1)
    datas.append(f)
    
    
#en sortie on récupère la donnée avec la valeur de la k_anonymité
with open('result_k_agregation78v2iris2test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","x","y","k"])
    for i in range(len(datas)):
        writer.writerow(datas[i])
    
    