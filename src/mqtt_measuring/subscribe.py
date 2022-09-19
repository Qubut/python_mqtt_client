# from _typeshed import ReadableBuffer
from paho.mqtt.client import Client as mqtt_client
from paho.mqtt.client import MQTTMessage
from pandas import DataFrame
from timing import timed
from connect import connect_mqtt
from argparse import ArgumentParser
import time
from utils import getFileSize
filename = "DUMMYFILE"
data = {
        'time elapsed':[],
        'file sizes':[]
        }
df = DataFrame()
def onMessage(client:mqtt_client, userdata,message:MQTTMessage):
    print("Recieving Message")
    print(message.topic)
    time =  savePayload(client,message.payload,filename)[1]
    data["time elapsed"].append(time)
    df = DataFrame(data)
    df.to_csv('./results.csv')
    print(data)
    
@timed
def savePayload(client:mqtt_client,payload, filename:str):
    print(f"Saving {filename}")
    with open(filename,"wb") as f:
        f.write(payload)
    data["file sizes"].append(getFileSize(filename))

def subscribe(client:mqtt_client,topic):
    client.subscribe(topic)
    client.on_message = onMessage

def run(topic:str):
    client = connect_mqtt()
    # while client.is_connected == True:
    #     time.sleep(1)
    subscribe(client,topic)
    client.loop_forever()
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("topic")
    topic = parser.parse_args()._get_kwargs()[0][1]
    run(topic)
