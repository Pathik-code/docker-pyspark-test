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
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data = generate_data()
    producer.send('sensor-data', value=data)
    print(f"Sent: {data}")
    time.sleep(1)
