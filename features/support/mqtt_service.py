import time
import subprocess
import paho.mqtt.client as mqtt

from features.support.wait_helpers import *


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

    def _start_mosquitto(self):
        print("Starting mosquitto")
        self._mosquitto_process = subprocess.Popen(['mosquitto', '-p', '52129'])
        time.sleep(3)

    def _connect_to_mosquitto(self):
        print("Connecting to mosquitto")
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect("0.0.0.0", port=52129)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("$SYS/#")

    def _on_message(self, client, userdata, msg):
        print('{}: {}'.format(msg.topic, msg.payload.decode('utf-8')))
        if msg.topic == '$SYS/broker/clients/total':
            self._client_connected_count = int(msg.payload.decode('utf-8'))
