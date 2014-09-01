import json
import pprint

import sip
import PyQt5.Qt as qt
import xmltodict
import pubsub.pub as pub

import model.project
import model.projects_model
import service.ci_server_poller as ci_poller


class StatusScreen(qt.QQuickItem):

    projects_changed = qt.pyqtSignal()
    failed_projects_changed = qt.pyqtSignal()
    error_changed = qt.pyqtSignal()
    on_status_updated = qt.pyqtSignal(list, object)

    def __init__(self, *args, **kwargs):
        super(StatusScreen, self).__init__(*args, **kwargs)
        self._projects = model.projects_model.ProjectsModel()
        self._failed_projects = model.projects_model.ProjectsModel()
        self._error = None

    def componentComplete(self):
        super(StatusScreen, self).componentComplete()
        self.on_status_updated.connect(self.on_status_update_on_ui_thread)
        pub.subscribe(self.on_status_update, "CI_UPDATE")
        self.poller = ci_poller.CIServerPoller()
        self.poller.start_polling_async()

    @qt.pyqtProperty(model.projects_model.ProjectsModel, notify=projects_changed)
    def projects(self):
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = value
        self.projects_changed.emit()

    @qt.pyqtProperty(model.projects_model.ProjectsModel, notify=failed_projects_changed)
    def failed_projects(self):
        return self._failed_projects

    @failed_projects.setter
    def failed_projects(self, value):
        self._failed_projects = value
        self.failed_projects_changed.emit()

    @qt.pyqtProperty(str, notify=error_changed)
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error
        self.error_changed.emit()

    def get_projects_from_responses(self, responses):
        projects = []
        for response in responses:
            statuses = xmltodict.parse(response.text)
            for response_project in statuses.get('Projects').get('Project'):
                name = response_project.get('@name')
                activity = response_project.get('@activity')
                last_build_status = response_project.get('@lastBuildStatus')
                last_build_time = response_project.get('@lastBuildTime')

                project = model.project.Project(name, activity, last_build_status, last_build_time)
                projects.append(project)
        return projects

    @qt.pyqtSlot(list, object)
    def on_status_update_on_ui_thread(self, responses, error):
        all_projects = self.get_projects_from_responses(responses)
        response_names = [project.name for project in all_projects]
        removed_projects = [project for project in self.projects.projects if project.name not in response_names]
        for removed_project in removed_projects:
            self.projects.remove(removed_project)

        for project in all_projects:
            matching_project = next((p for p in self.projects.projects if p.name == project.name), None)
            if matching_project is None and not project.is_failed():
                self.projects.append(project)
            elif matching_project is not None and project.is_failed():
                self.projects.remove(project)
            elif matching_project is not None:
                self.projects.update(matching_project, project.lastBuildStatus)

        for project in all_projects:
            matching_project = next((p for p in self.failed_projects.projects if p.name == project.name), None)
            if matching_project is None and project.is_failed():
                self.failed_projects.append(project)
            elif matching_project is not None and not project.is_failed():
                self.failed_projects.remove(project)
            elif matching_project is not None:
                self.failed_projects.update(matching_project, project.lastBuildStatus)

    def on_status_update(self, responses, error):
        self.on_status_updated.emit(responses, error)


