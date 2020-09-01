from pyspark.mllib.clustering import KMeansModel
from pyspark.mllib.linalg import Vectors
from pyspark import SparkContext
from itertools import permutations
import csv
import operator


centers = []
with open('/home/ronald/kmeansModel','r') as f:
    line = f.readline()
    while line:
        points = line[1:len(line)-2].split(",")
        centers.append([float(i) for i in points])
        line = f.readline()

model = KMeansModel(centers)

modelCenters = model.clusterCenters
realCenters = []
with open('/home/ronald/centers.csv','r') as f:
    csvReader = csv.DictReader(f)
    for row in csvReader:
        center = []
        for i in row:
            center.append(row[i])
        realCenters.append(Vectors.dense(center))

perm = list(permutations([i for i in range(8)]))

totalDist = []
for i in perm:
    dist = 0
    for j in range(len(i)):
        dist += Vectors.squared_distance(modelCenters[j], realCenters[i[j]])
    totalDist.append(dist)

ref = []
minIndex, minValue = min(enumerate(totalDist),key=operator.itemgetter(1))
ref = perm[minIndex]

# dataPoint = []
correct = 0
incorrect = 0
with open('/home/ronald/data.csv','r') as f:
    csvReader = csv.DictReader(f)
    for row in csvReader:
        data = []
        for i in row:
            if i!='target':
                data.append(row[i])
        if ref[model.predict(Vectors.dense(data))]==int(row['target']):
            correct+=1
        else:
            # print(str(ref[model.predict(Vectors.dense(data))])+' '+str(row['target']))
            incorrect+=1
        # dataPoint.append(data)

print(str(correct/(incorrect+correct)*100)+'%')
