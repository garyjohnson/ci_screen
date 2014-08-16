import PyQt5.Qt as qt
import sip
import service.ci_server_poller as ci_poller
import pubsub.pub as pub
import xmltodict
import pprint
import json
import model.project

class StatusScreen(qt.QQuickItem):

    projects_changed = qt.pyqtSignal()
    on_status_updated = qt.pyqtSignal(list, object)

    def __init__(self, *args, **kwargs):
        super(StatusScreen, self).__init__(*args, **kwargs)
        self._projects = []
        sip.transferto(self, self.window())

    @qt.pyqtProperty(qt.QQmlListProperty, notify=projects_changed)
    def projects(self):
        return qt.QQmlListProperty(model.project.Project, self, self._projects)

    def componentComplete(self):
        super(StatusScreen, self).componentComplete()
        self.on_status_updated.connect(self.on_status_update_on_ui_thread)
        pub.subscribe(self.on_status_update, "CI_UPDATE")
        self.poller = ci_poller.CIServerPoller()
        self.poller.start_polling_async()

    @qt.pyqtSlot(list, object)
    def on_status_update_on_ui_thread(self, responses, error):
        del self._projects[:]
        for response in responses:
            statuses = xmltodict.parse(response.text)
            response_projects = statuses.get('Projects').get('Project')
            for response_project in response_projects:
                name = response_project.get('@name')
                activity = response_project.get('@activity')
                last_build_status = response_project.get('@lastBuildStatus')
                last_build_time = response_project.get('@lastBuildTime')
                project = model.project.Project(name, activity, last_build_status, last_build_time)
                sip.transferto(project, self.window())
                self._projects.append(project)

        self.projects_changed.emit()

    def on_status_update(self, responses, error):
        self.on_status_updated.emit(responses, error)

