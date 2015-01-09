try:
    import ConfigParser as config
except:
    import configparser as config
import json
import collections

import PyQt5.Qt as qt
import xmltodict
import pubsub.pub as pub

import model.project
import model.projects_model
import service.ci_server_poller as ci_poller


class StatusScreen(qt.QQuickItem):

    holiday_changed = qt.pyqtSignal()
    holiday_source_changed = qt.pyqtSignal()
    projects_changed = qt.pyqtSignal()
    failed_projects_changed = qt.pyqtSignal()
    error_changed = qt.pyqtSignal()
    on_status_updated = qt.pyqtSignal(dict, dict)

    def __init__(self, *args, **kwargs):
        super(StatusScreen, self).__init__(*args, **kwargs)
        self._projects = model.projects_model.ProjectsModel()
        self._failed_projects = model.projects_model.ProjectsModel()
        self._error = None
        self._holiday_source = None

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
        for ci_server in responses:
            response = responses[ci_server]
            statuses = xmltodict.parse(response.text, dict_constructor=lambda *args, **kwargs: collections.defaultdict(list, *args, **kwargs))
            for response_projects in statuses['Projects']:
                for response_project in response_projects['Project']:
                    name = response_project.get('@name')
                    activity = response_project.get('@activity')
                    last_build_status = response_project.get('@lastBuildStatus')
                    last_build_time = response_project.get('@lastBuildTime')

                    project = model.project.Project(name, activity, last_build_status, last_build_time, ci_server)
                    projects.append(project)
        return projects

    @qt.pyqtSlot(dict, dict)
    def on_status_update_on_ui_thread(self, responses, errors):
        bad_ci_servers = errors.keys()
        new_projects = [p for p in self.get_projects_from_responses(responses) if p.lastBuildStatus != 'Unknown']

        self._synchronize_projects(self.projects, [p for p in new_projects if not p.is_failed()], bad_ci_servers)
        self._synchronize_projects(self.failed_projects, [p for p in new_projects if p.is_failed()], bad_ci_servers)

    def on_status_update(self, responses, errors):
        self.on_status_updated.emit(responses, errors)

    def _synchronize_projects(self, projects_model, new_projects, bad_ci_servers):
        new_project_names = [p.name for p in new_projects]
        old_project_names = [p.name for p in projects_model.projects]

        for removed_project in [p for p in projects_model.projects if p.name not in new_project_names and p.ci_server not in bad_ci_servers]:
            projects_model.remove(removed_project)

        for added_project in [p for p in new_projects if p.name not in old_project_names]:
            projects_model.append(added_project)

        for updated_project in [p for p in new_projects if p.name in old_project_names]:
            projects_model.update(updated_project)

        projects_model.sort_by_last_build_time()

    @qt.pyqtProperty(bool, notify=holiday_changed)
    def holiday(self):
        config_parser = config.SafeConfigParser(allow_no_value=False)
        with open('ci_screen.cfg') as config_file:
            config_parser.readfp(config_file)
        holiday = True
        if config_parser.has_option('general', 'holiday'):
            holiday = config_parser.getboolean('general', 'holiday')
        return holiday

    @qt.pyqtProperty(str, notify=holiday_source_changed)
    def holidaySource(self):
        return self._holiday_source

    @holidaySource.setter
    def holidaySource(self, value):
        self._holiday_source = value
        self._holiday_source_changed.emit()

