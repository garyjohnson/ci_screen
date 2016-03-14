import logging
import time
import threading
try:
    import ConfigParser as config
except:
    import configparser as config

import paho.mqtt.client as mqtt
import pubsub.pub as pub
import requests

import service.ci_server_loader as ci_loader


logger = logging.getLogger(__name__)

class MqttService(object):

    def __init__(self):
        self._stop = threading.Event()
        self._update = threading.Event()
        self.polling_thread = None
        self.settings = self.get_mqtt_settings()

    def __del__(self):
        self.stop_polling()

    def start_polling_async(self):
        self._stop.clear()
        self._update.clear()
        self.polling_thread = threading.Thread(target=self.poll_for_changes)
        self.polling_thread.daemon = True
        self.polling_thread.start()

    def stop_polling(self):
        self.unsubscribe_all()
        self._stop.set()
        self.polling_thread = None
    
    def poll_for_changes(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(self.settings['username'], self.settings['password'])
        while not self._stop.isSet():
            self.client.loop()

    def on_connect(client, userdata, rc):
        pass

    def on_disconnect(client, userdata, rc):
        pass

    def on_message(client, userdata, rc):
        pub.sendMessage("NOW_PLAYING_UPDATE", now_playing=now_playing)

    def get_mqtt_settings(self):
        config_parser = config.SafeConfigParser(allow_no_value=False)
        with open('ci_screen.cfg') as config_file:
            config_parser.readfp(config_file)

        mqtt_enabled = config_parser.getboolean('general', 'mqtt', fallback=False)

        mqtt_settings = None
        if mqtt_enabled and 'mqtt' in config_parser.sections():
            mqtt = config_parser['mqtt']
            mqtt_settings = {
                    'server': mqtt.get('server', ''),
                    'port': mqtt.getint('port', 0),
                    'username': mqtt.get('username', ''),
                    'password': mqtt.get('password', ''),
                    'now_playing_topic': mqtt.get('now_playing_topic', ''),
            }

        return mqtt_settings
