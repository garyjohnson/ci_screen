try:
    import ConfigParser as config
except:
    import configparser as config
import logging
import time
import threading
import collections

from pydispatch import dispatcher
import xmltodict
import requests

import ci_screen.service.ci_server_loader as ci_server_loader


logger = logging.getLogger(__name__)

class CIServerPoller(object):

    def __init__(self):
        self._stop = threading.Event()
        self._update = threading.Event()
        self._poll_rate = self._get_poll_rate()
        self.polling_thread = None
        self.ci_servers = ci_server_loader.get_ci_servers()

    def __del__(self):
        self.stop_polling()

    def start_polling_async(self):
        self._stop.clear()
        self._update.clear()
        self.polling_thread = threading.Thread(target=self._poll_for_changes)
        self.polling_thread.daemon = True
        self.polling_thread.start()

    def stop_polling(self):
        self.unsubscribe_all()
        self._stop.set()
        self.polling_thread = None
    
    def _poll_for_changes(self):
        while not self._stop.isSet():

            errors = {}
            responses = {}
            for server in self.ci_servers:
                name = server['name']
                url = server['url']

                auth = self._get_auth(server.get('username'), server.get('token'))
                (response, error) = self._get_jobs(name, url, auth)

                if response is not None:
                    responses[name] = response
                if error is not None:
                    errors[name] = error

            dispatcher.send(signal="CI_UPDATE", sender=self, responses=responses, errors=errors)
            time.sleep(self._poll_rate)

    def _get_auth(self, username, token):
        if username is not None and token is not None:
            return requests.auth.HTTPBasicAuth(username, token)

        return None

    def _get_jobs(self, name, url, auth):
        jobs = None
        error = None

        try:
            response = requests.get('{}/cc.xml'.format(url), auth=auth)
            if response.status_code == 200:
                jobs = self._convert_xml_jobs_to_dict(response.text)
            else:
                raise Exception('ci server {} returned {}: {}'.format(url, response, response.text))
        except Exception as ex:
            logger.warning(ex)
            error = ex

        return (jobs, error)

    def _convert_xml_jobs_to_dict(self, jobs_xml):
        jobs = []

        statuses = xmltodict.parse(jobs_xml, dict_constructor=lambda *args, **kwargs: collections.defaultdict(list, *args, **kwargs))
        for response_jobs in statuses['Projects']:
            for response_job in response_jobs['Project']:
                job = {
                        'name': response_job.get('@name'),
                        'activity': response_job.get('@activity'),
                        'last_build_status': response_job.get('@lastBuildStatus'),
                        'last_build_time': response_job.get('@lastBuildTime') }
                jobs.append(job)

        return jobs

    def _get_poll_rate(self):
        config_parser = config.SafeConfigParser(allow_no_value=False)
        with open('ci_screen.cfg') as config_file:
            config_parser.readfp(config_file)

        return int(config_parser.get('general', 'poll_rate_seconds'))
