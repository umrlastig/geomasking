# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:05:38 2020

@author: houfa
"""

import csv 

#on lit le fichier CSV dont on souhaite obtenir les statistiques d'une donnée 
b=open('result_k_agregation75v2batitamp5.csv')
dataCSV=csv.reader(b)
listdataCSV=list(dataCSV)

A=[]
#on ajoute dans une liste, la valeur qu'on souhaite étudier, il faut donc bien choisir la bonne colonne
for k in range(1,len(listdataCSV)):
    A.append(int(float(listdataCSV[k][11])))
u=0

#on va recenser le nombre de points de la base pour lesquelles la valeur étudiée est en dessous d'un certain seuil 
for k in range(len(A)):
    if A[k]<5:
        u+=1

samples = sorted(A)

s=0
moy=0
#on calcule la valeur moyenne de l'attribut étudié
for k in range(len(A)):
    s+=A[k]
moy=s/len(A)

def find_median(sorted_list):
    #algorithme permettant de trouver la valeur médiane de l'attribut étudié ainsi que les quartiles
    indices = []

    list_size = len(sorted_list)
    median = 0

    if list_size % 2 == 0:
        indices.append(int(list_size / 2) - 1)  # -1 because index starts from 0
        indices.append(int(list_size / 2))

        median = (sorted_list[indices[0]] + sorted_list[indices[1]]) / 2
        pass
    else:
        indices.append(int(list_size / 2))

        median = sorted_list[indices[0]]
        pass

    return median, indices
    pass

median, median_indices = find_median(samples)
Q1, Q1_indices = find_median(samples[:median_indices[0]])
Q2, Q2_indices = find_median(samples[median_indices[-1] + 1:])

quartiles = [Q1, median, Q2]

#Affichage du bilan des résultats
print("Nombre de points avec une anonymité insuffisante:{}".format(u))
print("(Q1, median, Q3): {}".format(quartiles))
print("moy:{}".format(moy))
print("min:{}".format(min(samples)))
print("max:{}".format(max(samples)))