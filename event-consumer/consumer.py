import json
import os
import logging
import signal
import sys
from kafka import KafkaConsumer
import psycopg2

logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
)

# Graceful shutdown
def signal_handler(sig, frame):
    logging.info("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Kafka consumer
consumer = KafkaConsumer(
    os.getenv("EVENT_TOPIC", "events"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "kafka:9092"),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=os.getenv("GROUP_ID", "event-consumers"),
)

# DB connection
def get_db_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        database=os.getenv("POSTGRES_DB", "events"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

# Create table if not exists
conn = get_db_conn()
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS event_log (
            id SERIAL PRIMARY KEY,
            user_id TEXT,
            event_type TEXT,
            url TEXT,
            ts DOUBLE PRECISION
        );
    """)
conn.commit()
conn.close()

# Consume events
for msg in consumer:
    event = msg.value
    try:
        conn = get_db_conn()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO event_log (user_id, event_type, url, ts) VALUES (%s, %s, %s, %s)",
                (event["user_id"], event["event_type"], event.get("url"), event["ts"])
            )
        conn.commit()
        conn.close()
        logging.info(f"Inserted event: {event}")
    except Exception as e:
        logging.error(f"Failed to insert event: {e}")
        # In real system: send to DLQ or retry queue