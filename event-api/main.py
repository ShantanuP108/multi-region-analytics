from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import os
import json
import logging
from kafka import KafkaProducer
import psycopg2
from psycopg2.extras import RealDictCursor

# Structured JSON logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
)

class Event(BaseModel):
    user_id: str
    event_type: str
    url: str | None = None
    ts: float | None = None

app = FastAPI(title="Event Ingest API")

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks="all",
    retries=3,
    linger_ms=5,
)

EVENT_TOPIC = os.getenv("EVENT_TOPIC", "events")
DLQ_TOPIC = os.getenv("DLQ_TOPIC", "events_dlq")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    # Prometheus will scrape this later
    return {"status": "metrics endpoint (to be instrumented)"}

@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
async def ingest(event: Event, response: Response):
    payload = event.dict()
    if payload.get("ts") is None:
        import time
        payload["ts"] = time.time()
    
    try:
        producer.send(EVENT_TOPIC, payload)
        logging.info(f"Event queued: {payload}")
        return {"queued": True}
    except Exception as e:
        logging.error(f"Failed to send to Kafka: {e}")
        # Fallback to DLQ
        try:
            producer.send(DLQ_TOPIC, payload)
            logging.info("Event sent to DLQ")
        except Exception as dlq_err:
            logging.error(f"DLQ also failed: {dlq_err}")
        return {"queued": False, "error": str(e)}
@app.get("/analytics")
def get_analytics():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "events"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres")
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Total events
            cur.execute("SELECT COUNT(*) as total FROM event_log")
            total = cur.fetchone()["total"]

            # Top URLs
            cur.execute("""
                SELECT url, COUNT(*) as count
                FROM event_log
                WHERE url IS NOT NULL
                GROUP BY url
                ORDER BY count DESC
                LIMIT 5
            """)
            top_urls = [row["url"] for row in cur.fetchall()]

        conn.close()
        return {
            "total_events": total,
            "top_urls": top_urls
        }
    except Exception as e:
        logging.error(f"Analytics query failed: {e}")
        return {"error": "Failed to fetch analytics"}, 500