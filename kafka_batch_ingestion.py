from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Kafka to Spark Demo") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    topic = "demo_poc"
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", 'broker:29092') \
        .option("subscribe", topic) \
        .load()

    kafka_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")


    def process_batch(df, batch_id):
        print("Processing batch", batch_id)
        json_str_df = spark.read.json(df.rdd.map(lambda r: r.value))
        json_df = df.withColumn('json', from_json(col('value'), json_str_df.schema))
        flattened_df = json_df.select(col('json.*'))

        print("Logging json df schema and data")
        json_df.printSchema()
        json_df.show()

        print("Logging flattened df schema and data")
        flattened_df.show()
        flattened_df.printSchema()

        flattened_df \
            .write \
            .format("console")

    kafka_df.writeStream \
        .trigger(once=True) \
        .option("checkpointLocation", "/tmp/_spark_offsets/" + topic) \
        .foreachBatch(process_batch) \
        .start() \
        .awaitTermination()
