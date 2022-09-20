import base64
from time import thread_time
import click
# from _typeshed import ReadableBuffer
from paho.mqtt.client import Client as mqtt_client
from paho.mqtt.client import MQTTMessage
from pandas import DataFrame
import _thread
import logging
from connect import connect_mqtt
from utils import check_path, mk_dir, check_temp_files, exit, dump_json, chunk_md5, load_json
data = {
    'time elapsed': [],
    'file sizes': []
}
df = DataFrame()


def on_message(client: mqtt_client, userdata, message: MQTTMessage):

    if type(message.payload) is bytes and type(message.payload.decode()) is not str:
        _thread.start_new_thread(convert_and_send, (client,
                                                    message.topic,
                                                    message.payload,
                                                    message.qos,
                                                    message.retain))
    else:
        logging.info("Recieving Message")
        print(message.topic)
        print(message.payload.decode())

    df = DataFrame(data)
    df.to_csv('./out/results.csv')
    print(data)


def make_temp(client: mqtt_client, top: str, od: str, data: bytes, hash: str, number: int, timeid: int, filename: str):
    """ save data to temp file
        and send recieved chunknumber
    """
    if chunk_md5(data.encode()) == hash:
        fname = od+"/"+str(timeid)+"_"+filename+"_.temp"
        with open(fname, "ab") as f:
            try:
                f.write(base64.b64decode(data))
            except Exception as e:
                print("ERR: write file", fname, e)
                return 1
        # if number == 0:
        #     f = open(fname, "wb")
        logging.info("saved chunk", number, "to", fname)
        client.publish(f"{top}/status", dump_json({"chunknumber": number}))


def convert_and_send(client, top, msg, qos, retain):
    """ convert msg to json,
        send data to file
    """
    try:
        msg = msg.decode()
        j = load_json(msg)
    except Exception as e:
        logging.error("msg2json", e)
        exit(2)
    try:
        if j["end"] is False:
            make_temp(client, top,
                      j["chunkdata"],
                      j["chunkhash"],
                      j["chunknumber"],
                      j["timeid"],
                      j["filename"])
        if j["end"] is True:
            check_temp_files(j["filename"], j["timeid"], j["filehash"])
            data["time elapsed"].append(thread_time())
            data["file sizes"].append(j["filesize"])
            exit(0)
    except Exception as e:
        logging.error("parse json", e)
        exit(3)


def subscribe(client: mqtt_client, topic):
    client.subscribe(topic)
    client.on_message = on_message


def run(topic: str):
    client = connect_mqtt()
    subscribe(client, topic)
    client.loop_forever()


@click.command()
@click.option("--topic", "-t", type=str, help="sets the message's topic")
@click.option("--output-dir", "-od", default="./out", type=str, help="Directory of transmitted files")
def main(topic, output_dir):
    od = output_dir
    if not check_path(od):
        try:
            mk_dir(od)
        except Exception as e:
            logging.error(e)
            return 1
    run(topic)


if __name__ == '__main__':
    main()
