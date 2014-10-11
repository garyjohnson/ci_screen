import bottle
import threading

class FakeCIServer(object):

    def __init__(self, port):
        self.thread = None
        self._host = 'localhost'
        self._app = bottle.Bottle()
        self.port = port
        self.projects = []

        self._app.route('/cc.xml', method='GET', callback=self.cc_xml)

    def cc_xml(self):
        bottle.response.content_type = 'xml/application'

        project_string = ''
        for project in self.projects:
            project_xml = '<Project webUrl="http://www.test.com" name="{name}" lastBuildLabel="71" lastBuildTime="{last_build_time}" lastBuildStatus="{status}" activity="Sleeping"/>'
            project_string += project_xml.format(name=project['name'], 
                    status=project.get('status', 'Success'),
                    last_build_time=project.get('last_build_time', '2014-08-27T16:06:15Z'))

        return '<Projects>{}</Projects>'.format(project_string)

    def start(self):
        self.thread = threading.Thread(target=self._app.run, kwargs={'host':self._host, 'port':self.port, 'quiet':True, 'debug':False})
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        self._app.close()

