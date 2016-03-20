import json
import logging
try:
    import ConfigParser as config
except:
    import configparser as config

import paho.mqtt.client as mqtt
from pydispatch import dispatcher


NOW_PLAYING_SIGNAL = "NOW_PLAYING_UPDATE"
logger = logging.getLogger(__name__)


class MqttService(object):

    def __init__(self):
        self._client = None
        self._settings = self._get_mqtt_settings()

        logger.info('mqtt settings loaded: {}'.format(self._settings))

    def start(self):
        if not self._settings['enabled']:
            logger.info('mqtt disabled, not connecting')
            return

        logger.info('connecting to mqtt...')
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message
        self._client.username_pw_set(self._settings['username'], self._settings['password'])
        if self._online_topic:
            self._client.will_set(self._online_topic, '0', retain=True)
        self._client.connect_async(self._settings['host'], self._settings['port'])
        self._client.loop_start()

    @property
    def _now_playing_topic(self):
        return self._settings['now_playing_topic']

    @property
    def _online_topic(self):
        return self._settings['online_topic']

    def _on_disconnect(self, client, userdata, return_code):
        logger.info('disconnected from mqtt broker: {}'.format(mqtt.error_string(return_code)))

    def _on_connect(self, client, userdata, flags, return_code):
        logger.info('connected to mqtt broker: {}'.format(mqtt.connack_string(return_code)))

        if self._online_topic:
            logger.info('publishing to "{}"'.format(self._online_topic))
            self._client.publish(self._online_topic, '1', retain=True)

        if self._now_playing_topic:
            logger.info('subscribing to "{}"'.format(self._now_playing_topic))
            self._client.subscribe(self._now_playing_topic)

    def _on_message(self, client, userdata, message):
        payload_string = message.payload.decode('utf-8')

        if message.topic == self._now_playing_topic:
            self._handle_now_playing_message(payload_string)

    def _handle_now_playing_message(self, message):
        now_playing = json.loads(message)
        dispatcher.send(signal=NOW_PLAYING_SIGNAL, sender=self, now_playing=now_playing)

    def _get_mqtt_settings(self):
        logger.info('loading mqtt settings')
        settings = self._get_default_mqtt_settings()

        config_parser = config.SafeConfigParser(allow_no_value=False)
        with open('ci_screen.cfg') as config_file:
            config_parser.readfp(config_file)

        settings['enabled'] = config_parser.getboolean('general', 'mqtt', fallback=False)
        if settings['enabled'] and 'mqtt' in config_parser.sections():
            mqtt = config_parser['mqtt']
            settings['host'] = mqtt.get('host', '')
            settings['port'] = mqtt.getint('port', 0)
            settings['username'] = mqtt.get('username', '')
            settings['password'] = mqtt.get('password', '')
            settings['now_playing_topic'] = mqtt.get('now_playing_topic', '')
            settings['online_topic'] = mqtt.get('online_topic', '')

        return settings

    def _get_default_mqtt_settings(self):
        return {
                'enabled': False,
                'host': '',
                'port': 0,
                'username': '',
                'password': '',
                'now_playing_topic': '',
                'online_topic': '' }
