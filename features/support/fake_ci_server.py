import bottle
import threading

class FakeCIServer(object):

    def __init__(self, port):
        self.thread = None
        self._host = 'localhost'
        self._port = port
        self._app = bottle.Bottle()
        self._projects = []

        self._app.route('/cc.xml', method='GET', callback=self.cc_xml)

    def cc_xml(self):
        bottle.response.content_type = 'xml/application'

        project_string = ''
        for project in self._projects:
            project_string += '<Project webUrl="http://www.test.com" name="{name}" lastBuildLabel="71" lastBuildTime="2014-08-27T16:06:15Z" lastBuildStatus="Success" activity="Sleeping"/>'.format(name=project['name'])

        return '<Projects>{}</Projects>'.format(project_string)

    def add_project(self, project):
        self._projects.append(project)

    def start(self):
        self.thread = threading.Thread(target=self._app.run, kwargs={'host':self._host, 'port':self._port})
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        self._app.close()
        if self.thread is not None:
            self.thread.join()

