from confluent_kafka import Consumer, KafkaException, KafkaError
import json


kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'django-consumer-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(kafka_config)
topics = ['user_cache_update', 'asset_cache_update']
consumer.subscribe(topics)


def handle_message(msg):
    message_value = msg.value().decode('utf-8')
    message_data = json.loads(message_value)
    if 'user_cache_update' in msg.topic():
        print("Received user cache update:", message_data)
    elif 'asset_cache_update' in msg.topic():
        print("Received asset cache update:", message_data)
    else:
        print("Received unknown message type:", message_data)


def consume_messages():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f'End of partition reached: {msg.partition}')
                else:
                    raise KafkaException(msg.error())
            else:
                handle_message(msg)
    except KeyboardInterrupt:
        print("Consumer interrupted")
    finally:
        consumer.close()
