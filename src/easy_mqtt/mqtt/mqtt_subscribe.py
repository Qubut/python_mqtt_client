import json
import threading
from time import thread_time
from .mqtt_client import MqttClient
from paho.mqtt.client import Client, MQTTMessage
from utils import logger, make_temp, check_temp_files


class MqttSubscribe(MqttClient):

    def __init__(self, topic: str, qos: int = 0, od='./out', client_id: str | None = None):
        self.od = od
        self.topic = topic
        self.qos = qos
        super().__init__(topic, qos, client_id)
        self.client.on_message = self.on_message

    def on_message(self, client: Client, userdata, message: MQTTMessage):
        self.convert_and_send(client,
                              message.topic,
                              message.payload,
                              message.qos,
                              message.retain, self.od)
        # threading.Thread(self.convert_and_send, (client,
        #                                          message.topic,
        #                                          message.payload,
        #                                          message.qos,
        #                                          message.retain, self.od))

    @classmethod
    def convert_and_send(cls, client: Client, top: str, msg: str,
                         qos: int, retain: bool, od: str):
        """ convert msg to json,
        send data to file
    """
        try:
            msg = msg.decode()
            j = json.loads(msg)
        except Exception as e:
            logger.info(msg)
            logger.error(e)
            exit(2)
        try:
            if j["end"] is False and make_temp(od,
                                               j["chunkdata"],
                                               j["chunkhash"],
                                               j["chunknumber"],
                                               j["timeid"],
                                               j["filename"]):

                client.publish(
                    f"{top}/status", json.dumps({"chunknumber": j["chunknumber"]}))
            if j["end"] is True:
                check_temp_files(od, j["filename"], j["timeid"], j["filehash"])
                exit(0)
        except Exception as e:
            logger.error(e)
            exit(3)
