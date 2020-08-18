name := "StreamingKMeansModelTrained"

version := "0.1"

//scalaVersion := "2.13.3"

scalaVersion := "2.12.0"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.0.0-preview2"
libraryDependencies += "org.apache.spark" %% "spark-mllib" % "3.0.0-preview2"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.0.0-preview2"
libraryDependencies += "org.apache.spark" %% "spark-sql-kafka-0-10" % "3.0.0" % "provided"
libraryDependencies += "org.apache.spark" %% "spark-streaming-kafka-0-10" % "3.0.0"






