package example.stream

import java.time.LocalDateTime

import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.common.serialization.StringDeserializer

import scala.io.Source
import scala.util.Random
import java.io.{File, PrintWriter}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.mllib.clustering.{KMeansModel, StreamingKMeansModel}
import org.apache.spark.mllib.linalg
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}
import org.apache.spark.streaming.{Seconds, StreamingContext}

object StreamingKMeansModelTraining {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("StreamingKMeansModelTraining")
    val ssc = new StreamingContext(conf,Seconds(1))

//    val filename = "/home/ronald/random_centers.csv"
//    val lines = Source.fromFile(filename).getLines.toArray.map(_.split(","))

    // read the random centers
    val centers:Array[linalg.Vector] = new Array[linalg.Vector](8)
    for (i <- 0 to centers.length-1) {
      centers(i) = Vectors.dense(Array(Random.nextDouble, Random.nextDouble, Random.nextDouble).map(_*30-15))
    }
    // create equal weights
    val weights:Array[Double] = new Array[Double](centers.length)
    for (i<-0 to weights.length-1) {
      weights(i) = 1/centers.length
    }

    val model = new StreamingKMeansModel(centers,weights)

    val brokers = args(0)
    val groupId = args(1)
    val topics = args(2)

    val topicsSet = topics.split(",").toSet
    val kafkaParams = Map[String, Object](
      ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG -> brokers,
      ConsumerConfig.GROUP_ID_CONFIG -> groupId,
      ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer],
      ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer])
    val messages = KafkaUtils.createDirectStream[String, String](
      ssc,
      LocationStrategies.PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](topicsSet, kafkaParams))

    val strippedMessages = messages.map(_.value).map(_.split("\""))
    val inputLines = strippedMessages.map(_(1).split(","))

    val timestamp = inputLines.map(_(0)).map(_+" "+LocalDateTime.now().toString())
    val coords = inputLines.map(_(1).split(" ").map(_.toDouble)).map(x => Vectors.dense(x))
    coords.foreachRDD(rdd => {
      model.update(rdd, 1.0, "batches")
    })

    ssc.start()
    ssc.awaitTerminationOrTimeout(120000)



    val file = new File("/home/ronald/kmeansModel")
    val pw = new PrintWriter(file)
    println("Centers:")
    for (i <- model.clusterCenters) {
      println(i.toString())
      pw.write(i.toString()+"\n")
    }
    pw.close()
    println("Cluster Weights:")
    for (i <- model.clusterWeights) {
      println(i.toString())
    }
    println(model.toPMML())
//    println(model.toPMML())
//    model.toPMML("/home/ronald/kmeansModel")
//    val sc = new SparkContext(conf)
//    model.save(sc, "/home/ronald/kmeansModel")
  }
}