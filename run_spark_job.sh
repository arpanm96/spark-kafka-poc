#!/bin/bash

../spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.0.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 \
--deploy-mode client --conf "spark.cores.max=3" --conf "spark.executor.cores=1" \
kafka_batch_ingestion.py localhost:9092
