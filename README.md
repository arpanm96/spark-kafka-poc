#### Structured Streaming With Kafka POC

Setting up a POC setup to read data from a Kafka topic in batch mode using streaming query 
and ingest data incrementally by managing the Kafka offsets via Spark checkpointing.
 
### Setup

- Run `python3 -m venv venv` to setup a virtual environment for Python
- Run `source venv/bin/activate` to enter into the virtual environment
- Run `pip3 install pyspark` to install pyspark dependency
- Download the confluent kafka community binaries from [here](https://docs.confluent.io/platform/current/installation/installing_cp/zip-tar.html#get-the-software)
- Add the binary to your path `export CONFLUENT_HOME=/path/to/confluent-<version> && export PATH=$CONFLUENT_HOME/bin:$PATH`

### Startup

- Run `docker-compose up -d` to bring up the Kafka and the Spark cluster
- Run `docker-compose ps -a` to check if both the Kafka and Spark cluster are up 

### Ingestion

- Run `kafka-topics --bootstrap-server localhost:9092 --topic demo_poc --partitions 3 --create` to create a topic
- Run `kafka-console-producer --broker-list 127.0.0.1:9092 --topic demo_poc` to write messages to the topic
- Write any json message such as `{"id": 1, "name": "demo"}`

### Processing

- Run `docker exec -it spark-worker-2 bash` to login in one of the Spark worker pods
- Run `cd demo` to navigate into the poc folder
- Run `./run_spark_job.sh` to run the spark job