FROM apache/spark:3.4.1-python3

USER root

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Add scripts
COPY start-spark.sh /
RUN chmod +x /start-spark.sh

WORKDIR /app

ENTRYPOINT ["/start-spark.sh"]

# Kafka setup
FROM confluentinc/cp-kafka:7.4.0

RUN mkdir -p /var/lib/kafka/data

EXPOSE 9092 29093

VOLUME ["/var/lib/kafka/data"]

CMD ["sh", "-c", "kafka-storage format -t $(kafka-storage random-uuid) -c /etc/kafka/kraft/server.properties && kafka-server-start /etc/kafka/kraft/server.properties"]
