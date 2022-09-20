import base64
from email.policy import default
import threading
from time import time
from connect import connect_mqtt
import logging
import asyncio
from paho.mqtt.client import Client as mqtt_client
import click
import time
from utils import check_file, chunk_md5, load_json
from utils import exit, generate_md5, get_size, chunk_md5
CHUNKSIZE = 999
chunknumber = 0
lock = threading.Lock()


def publish(client: mqtt_client, qos: int, topic: str, message: str, retain: bool):
    result = client.publish(topic, message, qos, retain)
    time.sleep(0.1)
    status = result[0]  # result: [0, 1]
    if status == 0:
        logging.info(f"Send `{message}` to topic `{topic}`")
    else:
        logging.info(f"Failed to send message to topic {topic}")


def send_file(client, topic, file, qos, retain):
    """ split, send chunk and wait for lock release
    """
    global chunknumber
    time.sleep(0.2)   # pause for mqtt subscribe
    timeid = str(int(time.time()))
    filesize = get_size(file)
    filehash = generate_md5(file)

    payload = {
        "timeid": timeid,
        "filename": file,
        "filesize": filesize,
        "filehash": filehash,
        "encode": "base64",
        "end": False}

    with open(file, 'rb') as f:
        while True:
            chunk = f.read(CHUNKSIZE)
            if chunk:
                data = base64.b64encode(chunk)
                payload.update({
                    "chunkdata": data.decode(),
                    "chunknumber": chunknumber,
                    "chunkhash": chunk_md5(data),
                    "chunksize": len(chunk)})
                client.publish(topic, payload, qos, retain)
                lock.acquire()
                chunknumber += 1
            else:
                del payload["chunknumber"]
                del payload["chunkdata"]
                del payload["chunkhash"]
                del payload["chunksize"]
                payload.update({"end": True})
                logging.info("END transfer file:", file)
                client.publish(topic, payload, qos, retain)
                break
    time.sleep(0.2)
    exit(0)


def publish_file(client, topic, payload, qos, retain):
    try:
        client.publish(topic, payload, qos, retain)
        if payload["end"] is False:
            print(
                "send chunk:", payload["chunknumber"], "time:",
                int(time.time()-float(payload["timeid"])), "sec")
    except Exception as e:
        logging.error(e)


def confirm_and_release(top, msg):
    """ receive confirmation to save chunk
    and release lock for next msg
    """
    global chunknumber
    try:
        j = load_json(msg.decode())
    except Exception as e:
        logging.error("json2msg", e)
        exit(2)
    try:
        if j["chunknumber"] == chunknumber:
            lock.release()
    except Exception as e:
        logging.error(e)
        exit(3)


def on_message(client, userdata, msg):
    ev = threading.Thread(target=confirm_and_release,
                          args=(msg.topic, msg.payload))
    ev.daemon = True
    ev.start()


def run(qos: int, topic: str, message: str, file: str, retain: bool):
    client = connect_mqtt()
    client.subscribe(f"{topic}/status")
    client.enable_logger(logging.Logger("Mqtt Logger"))
    if file:
        publish_thread = threading.Thread(target=send_file, args=(client,topic,file,qos,retain))
        publish_thread.daemon = True
        publish_thread.start()
    client.loop_start()
    publish(client, qos, topic, message,retain)


@click.command()
@click.option("--qos", "-q", default=0, type=click.Choice([0, 1, 2]), help="defines the QoS")
@click.option("--topic", "-t",type=str, help="sets the message's topic")
@click.option("--message", "-m", default=None, type=str, help="message to be sent to the subscribers")
@click.option("--file", "-f", default=None, type=str, help="file to be sent to the subscribers")
@click.option("--retain", "-r", default=False, type=click.Choice([True, False]), help="""if set to True, 
              the will message will be set as the “last known good”/retained message for the topic""")
def main(topic,message, file,qos, retain):
    if file and not check_file(file):
        logging.error("no file", file)
        return 1
    elif file:
        logging.info(
            f"starting the transfer of file {file}  chunksize = {CHUNKSIZE} byte")
    run(qos, topic, message, file, retain)


if __name__ == '__main__':
    main()
