from fabric.api import sudo
from fabric.operations import reboot
from fabric2 import Connection, Config
from invoke import Responder
from fabric2.transfer import Transfer
import os
from time import sleep

with open('./conf/master', 'r') as f:
    array = f.readline().split()
    masterHost = array[0]
    masterPort = array[1]
    user = array[2]
    host = array[3]

config = Config(overrides={'user': user})
conn = Connection(host=host, config=config)
configMaster = Config(overrides={'user': user, 'connect_kwargs': {'password': '1'}, 'sudo': {'password': '1'}})
master = Connection(host=masterHost, config=configMaster, gateway=conn)

slaveConnections = []
configSlaves = Config(overrides={'user': user, 'connect_kwargs': {'password': '1'}, 'sudo': {'password': '1'}})
with open('./conf/slaves', 'r') as f:
    array = f.readline().split()
    while array:
        slaveConnections.append(Connection(host=array[0], config=configSlaves, gateway=conn))
        array = f.readline().split()
with open('./conf/kafka', 'r') as f:
    array = f.readline().split()
    kafka = Connection(host=array[0], config=Config(overrides={'user': user,
                                                                         'connect_kwargs': {'password': '1'},
                                                                         'sudo': {'password': '1'}}), gateway=conn)


sudopass = Responder(pattern=r'\[sudo\] password:',
                     response='1\n',
                     )


def startKafka():
    kafka.run('tmux new -d -s kafka')
    kafka.run('tmux new-window')
    kafka.run('tmux new-window')
    kafka.run('tmux send -t kafka:0 /home/ronald/kafka_2.12-2.5.0/bin/zookeeper-server-start.sh\ '
               '/home/ronald/kafka_2.12-2.5.0/config/zookeeper.properties ENTER')
    sleep(5)
    kafka.run('tmux send -t kafka:1 /home/ronald/kafka_2.12-2.5.0/bin/kafka-server-start.sh\ '
               '/home/ronald/kafka_2.12-2.5.0/config/server.properties ENTER')
    kafka.run('tmux send -t kafka:2 python3\ /home/ronald/kafkaProducer.py ENTER')

def stopKafka():
    kafka.run('tmux kill-session -t kafka')

def stop():
    stopKafka()
    stopSparkCluster()

def startSparkCluster():
    master.run('source /etc/profile && $SPARK_HOME/sbin/start-all.sh')
    # c2.run('cd /usr/local/spark && ./sbin/start-slaves.sh')


def stopSparkCluster():
    master.run('source /etc/profile && $SPARK_HOME/sbin/stop-all.sh')
    # c2.run('cd /usr/local/spark && ./sbin/stop-all.sh')

def trainModel():

    # Transfer package
    transfer = Transfer(master)
    transferKafka = Transfer(kafka)
    # Transfer datagenerator
    transferKafka.put('./kafkaProducer.py')
    # start kafka
    startKafka()
    # start spark cluster
    startSparkCluster()
    # Create Package
    os.system('sbt package')
    # Transfer files to master
    transferKafka.get('/home/ronald/random_centers.csv')
    transfer.put('./random_centers.csv')
    transferKafka.get('/home/ronald/centers.csv')
    transfer.put('./centers.csv')
    transferKafka.get('/home/ronald/data.csv')
    transfer.put('./data.csv')

    # Transfer spark application
    transfer.put('./target/scala-2.12/streamingkmeansmodeltrained_2.12-0.1.jar')
    master.run(
        'source /etc/profile && cd $SPARK_HOME && bin/spark-submit '
        '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.0.0 '
        '--class example.stream.StreamingKMeansModelTraining '
        '--master spark://' + str(masterHost) + ':7077 --executor-memory 2g '
        '~/streamingkmeansmodeltrained_2.12-0.1.jar '
        '192.168.122.121:9092 '
        'consumer-group '
        'test'
    )
    runChecker()
    stop()

def runChecker():
    # transfer checker
    transfer = Transfer(master)
    transfer.put('./checker.py')
    master.run(
        'source /etc/profile && cd $SPARK_HOME && bin/spark-submit '
        '~/checker.py'
    )
