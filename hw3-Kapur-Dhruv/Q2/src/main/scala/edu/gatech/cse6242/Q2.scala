package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

object Q2 {

	def main(args: Array[String]) {
    	val sc = new SparkContext(new SparkConf().setAppName("Q2"))
		val sqlContext = new SQLContext(sc)
		import sqlContext.implicits._

    	// read the file
    	val file = sc.textFile("hdfs://localhost:8020" + args(0))
		/* TODO: Needs to be implemented */
        
        //Converting Records of RDD into rows

        val out = file.map(_.split("\t")).map(x => (x(0).toInt, x(2).trim.toInt)).toDF("src","outweight")
        val inp = file.map(_.split("\t")).map(x => (x(1).toInt, x(2).trim.toInt)).toDF("tgt","inweight")

        //Calculating the avg of inedge and outedge

        val outedge = out.filter(out("outweight") >= 10).groupBy("src").agg(avg(out("outweight"))).withColumnRenamed("avg(outweight)", "outweight")
        val inedge =  inp.filter(inp("inweight")>= 10).groupBy("tgt").agg(avg(inp("inweight"))).withColumnRenamed("avg(inweight)", "inweight")
        
        // Join
        val df = outedge.join(inedge, outedge("src") === inedge("tgt")).selectExpr("src", "outweight-inweight")

                        val filenew = df.map(f => f.mkString("\t"))

    	// store output on given HDFS path.
    	// YOU NEED TO CHANGE THIS
    	filenew.saveAsTextFile("hdfs://localhost:8020" + args(1))
  	}
}
