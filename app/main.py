from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, max, min
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, LongType
from pyspark.sql.window import Window

def create_spark_session():
    return SparkSession.builder \
        .appName("PySpark Server") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

def manipulate_stock_data(df):
    # Example manipulation: Calculate moving average of stock prices
    window_spec = Window.partitionBy("stock_id").orderBy("timestamp").rowsBetween(-5, 0)
    df = df.withColumn("moving_avg_price", avg("price").over(window_spec))
    return df

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
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "sensor-data") \
        .load()

    df = df.selectExpr("CAST(value AS STRING) as json") \
        .select(from_json(col("json"), schema).alias("data")) \
        .select("data.*")

    # Apply manipulation logic
    df = manipulate_stock_data(df)

    # Perform transformations and aggregations
    df = df.groupBy("stock_id").agg(
        avg("price").alias("avg_price"),
        max("price").alias("max_price"),
        min("price").alias("min_price"),
        avg("volume").alias("avg_volume")
    )

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
    # Keep the application running
    import time
    while True:
        time.sleep(1)

    import time
    while True:
        time.sleep(1)
