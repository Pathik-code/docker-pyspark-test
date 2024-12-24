from kafka import KafkaProducer
import json
import time
import random

def generate_stock_data():
    return {
        "stock_id": random.randint(1, 100),
        "price": round(random.uniform(100.0, 500.0), 2),
        "volume": random.randint(1000, 10000),
        "timestamp": int(time.time())
    }

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data = generate_stock_data()
    producer.send('stock-data', value=data)
    print(f"Sent: {data}")
    time.sleep(1)
