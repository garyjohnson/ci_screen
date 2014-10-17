import ConfigParser as config
import service.ci_server_loader as ci_loader
import pubsub.pub as pub
import threading
import requests
import time

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

            error = None
            responses = []
            for ci_server in self.ci_servers:
                url = ci_server.get('url')
                username = ci_server.get('username')
                token = ci_server.get('token')
                auth = None
                if username is not None and token is not None:
                    auth = requests.auth.HTTPBasicAuth(username, token)
                try:
                    response = requests.get('{}/cc.xml'.format(url), auth=auth)
                except Exception as e:
                    print e
                    error = e

                responses.append(response)

            if error is None:
                pub.sendMessage("CI_UPDATE", responses=responses, error=error)
                
            time.sleep(self._poll_rate)

    def get_poll_rate(self):
        config_parser = config.SafeConfigParser(allow_no_value=False)
        config_parser.readfp(open('ci_screen.cfg'))

        return int(config_parser.get('general', 'poll_rate_seconds'))
