from itertools import permutations
import csv

def squaredDistance(a,b):
    dist = 0
    for i in range(len(a)):
        dist += (a[i]-b[i])**2
    return dist

modelCenters = []
with open('/home/ronald/kmeansModel','r') as f:
    line = f.readline()
    while line:
        points = line[1:len(line)-2].split(",")
        centers.append([float(i) for i in points])
        line = f.readline()

realCenters = []
with open('/home/ronald/centers.csv','r') as f:
    csvReader = csv.DictReader(f)
    for row in csvReader:
        center = []
        for i in row:
            center.append(row[i])
        realCenters.append(Vectors.dense(center))

perm = permutations([i for i in range(8)])

