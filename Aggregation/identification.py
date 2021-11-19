# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 13:47:28 2020

@author: houfa
"""

import csv

b=open('iris75_compte_centerv2.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

print(listdataCSV[0])
j=0

for k in range (1,len(listdataCSV)):
    listdataCSV[k].insert(0,j)
    j+=1
    
with open('iris75_compte_centerv2id.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id","numpoints",'X','Y'])
    for i in range(1,len(listdataCSV)):
        writer.writerow(listdataCSV[i])