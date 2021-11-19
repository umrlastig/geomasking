# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:19:26 2020

@author: houfa
"""

import csv 

A=[]
N=[]
D=[]
E=[]
UA=[]
UNA=[]
C=[]

#on ouvre et ajoute dans des listes les fichiers CSV recensant tous les arcs de la triangulation de Delaunay
b=open('triang_delaunay_nonano.csv')
c=open('triang_delaunay_bimodal75kmin4.csv')
triangnaCSV=csv.reader(c)
triangCSV=csv.reader(b)
listTriangano=list(triangCSV)
listTriangna=list(triangnaCSV)

for k in range(1,len(listTriangano)):
    #on recense tous les arcs de la triangulation de Delaunay de la base de données anonymisées
    D.append([int(float(listTriangano[k][0])),int(float(listTriangano[k][1]))])
    D.append([int(float(listTriangano[k][1])),int(float(listTriangano[k][2]))])
    D.append([int(float(listTriangano[k][0])),int(float(listTriangano[k][2]))])
    
    
for k in range(1,len(listTriangna)):
    #on recense tous les arcs de la triangulation de Delaunay de la base de données non-anonymisées
    E.append([int(float(listTriangna[k][0])),int(float(listTriangna[k][1]))])
    E.append([int(float(listTriangna[k][1])),int(float(listTriangna[k][2]))])
    E.append([int(float(listTriangna[k][0])),int(float(listTriangna[k][2]))])
    
for k in range(len(D)):
    #on nettoie les deux listes en enlevant les doublons, pour que chaque arc unique ne soit compté qu'une seule fois
    if D[k] not in A and [D[k][1],D[k][0]] not in A:
        A.append(D[k])
for k in range(len(E)):
    if E[k] not in N and [E[k][1],E[k][0]] not in N:
        N.append(E[k])
       
for k in range(len(A)):
    for i in range(len(N)):
        #on recense tous les arcs en commun des deux triangulations
        if A[k][0]==N[i][0] and A[k][1]==N[i][1]:
            C.append(A[k])
        elif A[k][0]==N[i][1] and A[k][1]==N[i][0]:
            C.append(A[k])

for k in range(len(A)):
    #on recense les arcs uniques à la triangulation de la base de données anonymisées
    if A[k] not in C and [A[k][1],A[k][0]] not in C:
        UA.append(A[k])
        
for k in range(len(N)):
    #on recense les arcs uniques à la triangulation de la base de données non-anonymisées
    if N[k] not in C and [N[k][1],N[k][0]] not in C:
        UNA.append(N[k])
    
print("Nombre d'arcs total de la triangulation de la base de données anonymisées:{}".format(len(A)))
print("Nombre d'arcs total de la triangulation de la base de données non-anonymisées:{}".format(len(N)))
print("Nombre d'arcs en commun aux deux triangulations".format(len(C))) 