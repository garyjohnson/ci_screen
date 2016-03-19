import json
import logging
try:
    import ConfigParser as config
except:
    import configparser as config

import paho.mqtt.client as mqtt
from pydispatch import dispatcher


logger = logging.getLogger(__name__)

class MqttService(object):

    def __init__(self):
        self._settings = self.get_mqtt_settings()
        self._client = None

    def start(self):
        if self._settings is None:
            logger.info('MQTT disabled, not connecting')
            return

        logger.info('Connecting to MQTT...')
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message
        self._client.username_pw_set(self._settings['username'], self._settings['password'])
        self._client.connect(self._settings['host'], self._settings['port'])
        self._client.loop_start()

    def _on_disconnect(self, client, userdata, rc):
        logger.info('disconnected')
        print(mqtt.error_string(rc))

    def _on_connect(self, client, userdata, flags, rc):
        logger.info('Connected to MQTT')
        print('subscribing to "{}"'.format(self._settings['now_playing_topic']))
        self._client.subscribe(self._settings['now_playing_topic'])
        print('subscribed')

    def _on_message(self, client, userdata, msg):
        if msg.topic == self._settings['now_playing_topic']:
            payload = msg.payload.decode('utf-8')
            now_playing = json.loads(payload)
            print(now_playing)
            dispatcher.send(signal="NOW_PLAYING_UPDATE", sender=self, now_playing=now_playing)

    def get_mqtt_settings(self):
        logger.debug('Loading MQTT settings')
        config_parser = config.SafeConfigParser(allow_no_value=False)
        with open('ci_screen.cfg') as config_file:
            config_parser.readfp(config_file)

        mqtt_enabled = config_parser.getboolean('general', 'mqtt', fallback=False)

        mqtt_settings = None
        if mqtt_enabled and 'mqtt' in config_parser.sections():
            mqtt = config_parser['mqtt']
            mqtt_settings = {
                    'host': mqtt.get('host', ''),
                    'port': mqtt.getint('port', 0),
                    'username': mqtt.get('username', ''),
                    'password': mqtt.get('password', ''),
                    'now_playing_topic': mqtt.get('now_playing_topic', ''),
            }

        return mqtt_settings
