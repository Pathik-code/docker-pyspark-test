### Step-by-Step Explanation of Docker Compose for PySpark Cluster

1. **Architecture Components**:
   - 1 Spark Master node
   - 2 Spark Worker nodes
   - Shared volumes for data and applications
   - Internal network communication

2. **Service Breakdown**:

   **Spark Master**:
   - Runs on ports 4040 (Spark UI) and 7077 (Spark master)
   - Mounts two volumes:
     -

app

: Application code
     -

data

: Data storage
   - Named container for easy reference
   - Environment variables set master configuration

   **Spark Workers**:
   - 2 replicas (workers)
   - Depends on master service
   - Same volume mounts as master
   - Connects to master via internal Docker network
   - Environment variables set worker configuration

3. **Network Flow**:
```
Client → Spark Master (7077) → Spark Workers
        ↳ Spark UI (4040)
```

4. **Volume Structure**:
```
project/
├── app/
│   └── (application code)
├── data/
│   └── (data files)
└── docker-compose.yml
```

5. **Usage**:
```bash
# Start the cluster
docker-compose up -d

# Scale workers if needed
docker-compose up -d --scale spark-worker=3

# Check running containers
docker-compose ps

# Stop the cluster
docker-compose down
```



### Project Idea: Real-time Data Processing with Kafka and PySpark

#### Project Overview
Create a real-time data processing pipeline using Kafka and PySpark. The project will involve generating data using a Kafka producer, consuming the data with PySpark, and performing transformations and aggregations on the data.

#### Steps to Complete the Project

1. **Set Up Kafka and Zookeeper**
   - Install Kafka and Zookeeper on your local machine or use Docker to set up the services.
   - Start Zookeeper and Kafka services.

2. **Create Kafka Topics**
   - Create a Kafka topic for producing and consuming data.

3. **Kafka Producer Script**
   - Write a Python script to generate and send data to the Kafka topic.

4. **PySpark Consumer Script**
   - Write a PySpark script to consume data from the Kafka topic.
   - Perform transformations and aggregations on the consumed data.
   - Save the processed data to a storage system (e.g., HDFS, S3, or a database).

5. **Run and Monitor the Pipeline**
   - Run the Kafka producer script to start generating data.
   - Run the PySpark consumer script to start processing the data.
   - Monitor the pipeline to ensure data is being processed correctly.

#### Detailed Steps

1. **Set Up Kafka and Zookeeper**
   - Download Kafka from the official website.
   - Extract the downloaded files and navigate to the Kafka directory.
   - Start Zookeeper:
     ```sh
     bin/zookeeper-server-start.sh config/zookeeper.properties
     ```
   - Start Kafka:
     ```sh
     bin/kafka-server-start.sh config/server.properties
     ```

2. **Create Kafka Topics**
   - Create a Kafka topic named `sensor-data`:
     ```sh
     bin/kafka-topics.sh --create --topic sensor-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

3. **Kafka Producer Script**
   - Create a Python script to generate and send data to the Kafka topic.

   ```python
   # filepath: /home/pathik/Documents/DataEngineer/Projects/docker-pyspark-test/app/kafka_producer.py
   from kafka import KafkaProducer
   import json
   import time
   import random

   def generate_data():
       return {
           "sensor_id": random.randint(1, 100),
           "temperature": random.uniform(20.0, 30.0),
           "humidity": random.uniform(30.0, 50.0),
           "timestamp": int(time.time())
       }

   producer = KafkaProducer(
       bootstrap_servers='localhost:9092',
       value_serializer=lambda v: json.dumps(v).encode('utf-8')
   )

   while True:
       data = generate_data()
       producer.send('sensor-data', value=data)
       print(f"Sent: {data}")
       time.sleep(1)
   ```

4. **PySpark Consumer Script**
   - Modify the existing PySpark script to consume data from the Kafka topic and perform transformations.

   ```python
   # filepath: /home/pathik/Documents/DataEngineer/Projects/docker-pyspark-test/app/main.py
   # ...existing code...
   from pyspark.sql.functions import from_json, col
   from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, LongType

   def consume_kafka_data(spark):
       schema = StructType([
           StructField("sensor_id", IntegerType()),
           StructField("temperature", DoubleType()),
           StructField("humidity", DoubleType()),
           StructField("timestamp", LongType())
       ])

       df = spark \
           .readStream \
           .format("kafka") \
           .option("kafka.bootstrap.servers", "localhost:9092") \
           .option("subscribe", "sensor-data") \
           .load()

       df = df.selectExpr("CAST(value AS STRING) as json") \
           .select(from_json(col("json"), schema).alias("data")) \
           .select("data.*")

       # Perform transformations and aggregations
       df = df.groupBy("sensor_id").avg("temperature", "humidity")

       query = df.writeStream \
           .outputMode("complete") \
           .format("console") \
           .start()

       query.awaitTermination()

   if __name__ == "__main__":
       spark = create_spark_session()
       print("PySpark Server is running!")
       spark.sparkContext.setLogLevel("INFO")
       consume_kafka_data(spark)
       # ...existing code...
   ```

5. **Run and Monitor the Pipeline**
   - Start the Kafka producer script to generate data:
     ```sh
     python /home/pathik/Documents/DataEngineer/Projects/docker-pyspark-test/app/kafka_producer.py
     ```
   - Start the PySpark consumer script to process data:
     ```sh
     python /home/pathik/Documents/DataEngineer/Projects/docker-pyspark-test/app/main.py
     ```
   - Monitor the console output to ensure data is being processed correctly.

This project will help you learn how to integrate Kafka with PySpark, perform real-time data processing, and handle streaming data.
