import websocket
import json
import finnhub
from kafka import KafkaProducer, KafkaConsumer
from key import api_key, ip_address, S3_BUCKET_NAME, S3_FILE_PREFIX 
from s3fs import S3FileSystem
import boto3

# Finnhub API key
FINNHUB_API_KEY = api_key

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = [ip_address]
KAFKA_TOPIC = 'btcusdt_trades'

# S3 Configuration
S3_BUCKET_NAME = S3_BUCKET_NAME
S3_FILE_PREFIX = S3_FILE_PREFIX 

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Initialize S3 client
s3_client = boto3.client('s3')

def upload_to_s3(data, count):
    filename = f"{S3_FILE_PREFIX}/btcusdt_trades_{count}.json"
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=filename, Body=json.dumps(data))
    print(f"Uploaded {filename} to s3")

# Finnhub client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def on_message(ws, message):
    data = json.loads(message)

    if data['type'] == 'trade':
        for trade in data['data']:
            # Send trade data to Kafka
            trade_data = {
                'price': trade['p'],
                'timestamp': trade['t'],
                'volume': trade['v']
            }

            producer.send(KAFKA_TOPIC, trade_data)
            print(f"Sent to Kafka: {trade_data}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={FINNHUB_API_KEY}",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)

    ws.run_forever()

    #Continuously consume data from Kafka and write to s3
    for count, message in enumerate(consumer):
        print(f"Received from Kafka: {message.value}")
        # Upload the message to s3
        upload_to_s3(message.value, count)
    
