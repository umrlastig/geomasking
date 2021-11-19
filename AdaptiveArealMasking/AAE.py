'''
@author gtouya
'''

import numpy as np
import sys
import csv
import math
import block_aggregation

from shapely.geometry import Polygon, Point, LineString
from shapely import wkt

disclosure_value = 20
masking_method = "aggregation"

def gaussian(mu,et,n):
    # gives a random value following a Gaussian law
    values = np.random.normal(mu,et,n)
    return values


# First load the data, first the points to mask
print("load data")
b = open('donnees_generees78densiteord_zonetest.csv')
# put the points to anonymise in a list
dataCSV = csv.reader(b)
listdataCSV = list(dataCSV)

# Then, load the blocks to aggregate
b = open('blocks_count_78_zonetest.csv')
# put the blocks from the CSV file into a list
csv.field_size_limit(2147483647)
blocksCSV = csv.reader(b)
blockList = list(blocksCSV)

# Convert the blocks from WKT to Polygons
blocks=[[]]

for k in range(1,len(blockList)):
    #build the geometries of the blocks from the WKT strings contained in the CSV file
    wkt_poly = blockList[k][0]
    polygon = wkt.loads(wkt_poly)
    # store the number of addresses in the block to use it for aggregation
    blocks.append([polygon, blockList[k][2]])

# Then aggregates the polygons
print("aggregate blocks")
aggregated_blocks = block_aggregation.block_aggregation(blocks, disclosure_value)

# get the points ids from the list extracted from the CSV
points = []
for i in range(1,len(listdataCSV)):
    points.append(int(listdataCSV[i][1]))

print("mask points in each block")
result = [[]]
for i in range(1,len(aggregated_blocks)):
    block = aggregated_blocks[i][0]
    n_address = int(aggregated_blocks[i][1])

    # get all the points contained this aggregated block
    points_in_block = []
    nb_points = len(points)
    for j in range(1, nb_points):
        point_geom = Point(float(listdataCSV[j][10]), float(listdataCSV[j][11]))
        if block.contains(point_geom):
            points_in_block.append(j)
            points.remove(points[j])

    if len(points_in_block) == 0:
        continue

    # test the chosen masking method
    if masking_method == "aggregation":
        # aggregate all the points contained in this block around its centroid
        if len(points_in_block) > 1:
            angle = 0
            d = 3
            for k in range(1, len(points_in_block)):
                m = []
                if angle == (math.pi * 2):
                    angle = 0
                    d += 1
                m.append(listdataCSV[points_in_block[k]][1])
                m.append(listdataCSV[points_in_block[k]][2])
                m.append(listdataCSV[points_in_block[k]][3])
                m.append(listdataCSV[points_in_block[k]][4])
                m.append(listdataCSV[points_in_block[k]][5])
                m.append(listdataCSV[points_in_block[k]][6])
                m.append(listdataCSV[points_in_block[k]][7])
                m.append(listdataCSV[points_in_block[k]][8])
                m.append(listdataCSV[points_in_block[k]][9])
                x = float(listdataCSV[points_in_block[k]][10]) + (d * math.cos(angle))
                y = float(listdataCSV[points_in_block[k]][11]) + (d * math.sin(angle))
                m.append(x)
                m.append(y)
                # add k-anonymity and privacy ratio
                m.append(n_address)
                m.append(len(points_in_block)/n_address)
                result.append(m)
                angle += (math.pi / 8)

    # else:
        # make a Gaussian bimodal masking cut to stay in the aggregated block

# en sortie on a un fichier avec les attributs d'origine de chaque point, et leur nouvelle coordonnées après agrégation
with open('geomasking_AAE_78.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "identifiant", "numero", "adresse", "postal", "commune", "source", "geom", "date", "X", "Y", "k_anon", "p_ratio"])
    for i in range(len(result)):
        writer.writerow(result[i])