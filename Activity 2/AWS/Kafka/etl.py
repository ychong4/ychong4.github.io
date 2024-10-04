import websocket
import json
import finnhub
from kafka import KafkaProducer
from key import api_key, ip_address

# Finnhub API key
FINNHUB_API_KEY = api_key

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = [ip_address]
KAFKA_TOPIC = 'stock_data'

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Finnhub client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def on_message(ws, message):
    data = json.loads(message)
    # Only process trade data
    if data['type'] == 'trade':
        for trade in data['data']:
            # Send trade data to Kafka
            producer.send(KAFKA_TOPIC, trade)
            print(f"Sent to Kafka: {trade}")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")
    # Subscribe to Apple stock
    ws.send('{"type":"subscribe","symbol":"AAPL"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={FINNHUB_API_KEY}",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)

    ws.run_forever()
