import time
import subprocess
import paho.mqtt.client as mqtt

from features.support.wait_helpers import *


BROKER_HOST = '0.0.0.0'
BROKER_PORT = 52129
BROKER_CMD = 'mosquitto -p {}'.format(BROKER_PORT)

class MqttService(object):

    def __init__(self):
        self._mosquitto_process = None
        self._client = None
        self._client_connected_count = 0

    @property
    def client_connected_count(self):
        return self._client_connected_count

    def start(self):
        self._start_mosquitto()
        self._connect_to_mosquitto()

    def stop(self):
        self._client.disconnect()
        self._client.loop_stop()
        self._mosquitto_process.kill()
        self._mosquitto_process.wait()
        self._mosquitto_process = None

    def publish(self, topic, message, retain=False):
        self._client.publish(topic, message, retain=retain)

    def _start_mosquitto(self):
        print("Starting mosquitto")
        subprocess.call('pkill -f "{}"'.format(BROKER_CMD), shell=True)
        self._mosquitto_process = subprocess.Popen(BROKER_CMD.split())

    def _connect_to_mosquitto(self):
        print("Connecting to mosquitto")
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(BROKER_HOST, BROKER_PORT)
        self._client.loop_start()
        self._wait_for_mqtt_connection()

    def _wait_for_mqtt_connection(self):
        if not eventually(lambda: self.client_connected_count == 1, retries=24):
            raise Exception('Expected tests to connect to MQTT broker.')

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("$SYS/broker/clients/total")

    def _on_message(self, client, userdata, msg):
        print('{}: {}'.format(msg.topic, msg.payload.decode('utf-8')))
        if msg.topic == '$SYS/broker/clients/total':
            self._client_connected_count = int(msg.payload.decode('utf-8'))
