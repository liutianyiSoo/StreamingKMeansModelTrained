from time import sleep
from json import dumps
from kafka import KafkaProducer
from sklearn.datasets import make_blobs
from datetime import datetime
import csv


def create_data(n_samples, n_features, centers, std):
    features, target = make_blobs(n_samples = n_samples,
                                  # two feature variables,
                                  n_features = n_features,
                                  # four clusters,
                                  centers = centers,
                                  # with .65 cluster standard deviation,
                                  cluster_std = std,
                                  # shuffled,
                                  shuffle = True)
    return features, target

# Create random centers
random_centers, _ = create_data(8,3,8,3)
with open('random_centers.csv','w') as f:
    fieldnames = ['x','y','z']
    writer = csv.DictWriter(f,fieldnames)
    writer.writeheader()
    for i in range(len(random_centers)):
        dct= {}
        for j in range(len(random_centers[i])):
            dct[fieldnames[j]]=random_centers[i][j]
        writer.writerow(dct)

# Create Centers for production
centers, cluster_num = create_data(8,3,8,3)
with open('centers.csv','w') as f:
    fieldnames = ['x','y','z']
    writer = csv.DictWriter(f,fieldnames)
    writer.writeheader()
    for i in range(len(centers)):
        dct= {}
        for j in range(len(centers[i])):
            dct[fieldnames[j]]=centers[i][j]
#         dct[fieldnames[len(centers[i])]] = cluster_num[i]
        writer.writerow(dct)

features, target = create_data(10000,3,centers,0.65)
with open('data.csv','w') as f:
    fieldnames = ['x','y','z','target']
    writer = csv.DictWriter(f,fieldnames)
    writer.writeheader()
    for i in range(len(features)):
        dct= {}
        for j in range(len(features[i])):
            dct[fieldnames[j]]=features[i][j]
        dct[fieldnames[len(features[i])]] = target[i]
        writer.writerow(dct)
sleep(10)
producer = KafkaProducer(bootstrap_servers=['192.168.122.121:9092'], value_serializer = lambda x: dumps(x).encode('utf-8'))
for i in range(len(features)):
    message = str(datetime.now()) + ',' + ' '.join([str(j) for j in features[i]]) + ',' + str(target[i])
    print(message)
    producer.send('test',value=message)

