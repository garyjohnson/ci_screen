import logging
import time
import threading
import ConfigParser as config

import pubsub.pub as pub
import requests

import service.ci_server_loader as ci_loader


logger = logging.getLogger(__name__)

class CIServerPoller(object):

    def __init__(self):
        self._stop = threading.Event()
        self._update = threading.Event()
        self._poll_rate = self.get_poll_rate()
        self.polling_thread = None
        self.ci_servers = ci_loader.get_ci_servers()

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
        while not self._stop.isSet():

            errors = {}
            responses = {}
            for ci_server in self.ci_servers:
                name = ci_server['name']
                url = ci_server['url']
                username = ci_server.get('username')
                token = ci_server.get('token')
                auth = None
                if username is not None and token is not None:
                    auth = requests.auth.HTTPBasicAuth(username, token)
                try:
                    response = requests.get('{}/cc.xml'.format(url), auth=auth)
                    if response.status_code == 200:
                        responses[name] = response
                    else:
                        raise Exception('ci server {} returned {}: {}'.format(url, response, response.text))
                except Exception as ex:
                    logger.warning(ex)
                    errors[name] = ex

            pub.sendMessage("CI_UPDATE", responses=responses, errors=errors)
            time.sleep(self._poll_rate)

    def get_poll_rate(self):
        config_parser = config.SafeConfigParser(allow_no_value=False)
        config_parser.readfp(open('ci_screen.cfg'))

        return int(config_parser.get('general', 'poll_rate_seconds'))
