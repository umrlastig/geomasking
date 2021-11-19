# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:53:09 2020

@author: houfa
"""

import csv

#ce script est important pour recalculer la k-anonymité, on remet dans l'ordre croissant par id
b=open('donnees_agregees78v2iris.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

data=[]
for i in range(len(listdataCSV)):
    for k in range(1,len(listdataCSV)):
        if int(listdataCSV[k][0])==i and listdataCSV[k] not in data:
            data.append(listdataCSV[k])

with open('donnees_agregees78v2iris_ord.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","identifiant","numero","adresse","postal","commune","source","geom","date","X","Y"])
    for i in range(len(data)):
        writer.writerow(data[i])
