from pypmml import Model

model = Model.load('kmeansModel')



#
# from pyspark.mllib.clustering import KMeansModel
# from pyspark.mllib.linalg import Vectors
# from pyspark import SparkContext
# import csv
# import operator
#
# sc = SparkContext(appName="Checker")
#
# model = KMeansModel.load(sc, "/home/ronald/kmeansModel")
#
# modelCenters = model.clusterCenters
# realCenters = []
# with open('/home/ronald/centers.csv','r') as f:
#     csvReader = csv.DictReader(f)
#     for row in csvReader:
#         center = []
#         for i in row:
#             center.append(row[i])
#         realCenters.append(Vectors.dense(center))
#
# distTable = []
#
# for i in modelCenters:
#     distRow = []
#     for j in realCenters:
#         distRow.append(Vectors.squared_distance(i,j))
#     distTable.append(distRow)
#
# ref = []
# for i in distTable:
#     minIndex, minValue = min(enumerate(i),key=operator.itemgetter(1))
#     ref.append(minIndex)
#     # print(str(minIndex)+' '+str(minValue))
#
#
# # dataPoint = []
# correct = 0
# incorrect = 0
# with open('/home/ronald/data.csv','r') as f:
#     csvReader = csv.DictReader(f)
#     for row in csvReader:
#         data = []
#         for i in row:
#             if i!='target':
#                 data.append(row[i])
#         if ref[model.predict(Vectors.dense(data))]==int(row['target']):
#             correct+=1
#         else:
#             # print(str(ref[model.predict(Vectors.dense(data))])+' '+str(row['target']))
#             incorrect+=1
#         # dataPoint.append(data)
#
# print(str(correct/(incorrect+correct)*100)+'%')
