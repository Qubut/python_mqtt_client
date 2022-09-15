from connect import connect_mqtt
from paho.mqtt.client import Client as mqtt_client
import time
from argparse import ArgumentParser

def publish(client:mqtt_client,topic:str):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run(topic:str):
    client = connect_mqtt()
    client.loop_start()
    publish(client,topic)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("topic")
    topic = parser.parse_args()._get_kwargs()[0][1]
    run(topic)
