from utils import exit, generate_md5, chunk_md5
import base64
from paho.mqtt.client import Client, MQTTMessage
from genericpath import getsize
import time
from utils import logger
from mqtt_client import MqttClient
import json
import threading


class MqttPublish(MqttClient):
    lock = threading.Lock()
    chunk_size = 999
    chunk_number = 0

    def __init__(self, topic, qos, client_id: str | None = None):
        super().__init__(topic, qos, client_id)
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883)
        self.client.subscribe(f"{self.topic}/status")

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        ev = threading.Thread(target=self.confirm_and_release,
                              args=(msg.topic, msg.payload))
        ev.daemon = True
        ev.start()

    @classmethod
    def confirm_and_release(cls, top: str, msg: bytes):
        """ receive confirmation to save chunk
    and release lock for next msg
    """
        try:
            j = json.loads(msg.decode())
        except Exception as e:
            logger.error(e)
            exit(2)
        try:
            if j["chunknumber"] == cls.chunk_number:
                cls.lock.release()
        except Exception as e:
            logger.error(e)
            exit(3)

    @classmethod
    def send_file(cls, client, topic, file, qos, retain):
        """ split, send chunk and wait for lock release
        """
        timeid = str(int(time.time()))
        filesize = getsize(file)
        filehash = generate_md5(file)

        payload = {
            "timeid": timeid,
            "filename": file.split('/')[-1],
            "filesize": filesize,
            "filehash": filehash,
            "encode": "base64",
            "end": False}

        with open(file, 'rb') as f:
            while True:
                chunk = f.read(cls.chunk_size)
                if chunk:
                    data = base64.b64encode(chunk)
                    payload.update({
                        "chunkdata": data.decode(),
                        "chunknumber": cls.chunk_number,
                        "chunkhash": chunk_md5(data),
                        "chunksize": len(chunk)})
                    cls.publish_file(
                        client, topic, json.dumps(payload), qos, retain)
                    # cls.lock.acquire()
                    cls.chunk_number += 1
                else:
                    del payload["chunknumber"]
                    del payload["chunkdata"]
                    del payload["chunkhash"]
                    del payload["chunksize"]
                    payload.update({"end": True})
                    logger.info(f"END transfer file: {file}")
                    cls.publish_file(
                        client, topic, json.dumps(payload), qos, retain)
                    break
        exit(0)

    @staticmethod
    def publish_file(client, topic, payload, qos, retain):
        try:
            client.publish(topic, payload, qos, retain)
            if (mssg := json.loads(payload)) and (mssg["end"] is False):
                logger.info(f"""send chunk:{mssg["chunknumber"]} 
                            time:{int(time.time()-float(mssg["timeid"]))} sec""")
        except Exception as e:
            logger.error(e)
