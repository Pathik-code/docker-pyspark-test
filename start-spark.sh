#!/bin/bash

if [ "$SPARK_MODE" == "master" ]; then
    /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
else
    /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker $SPARK_MASTER_URL
fi
