try:
    import ConfigParser as config
except:
    import configparser as config
import json

import PyQt5.Qt as qt
from pydispatch import dispatcher

import ci_screen.screens.helpers.holiday_chooser as holiday_chooser
from ci_screen.model.project import Project
from ci_screen.model.projects_model import ProjectsModel
from ci_screen.service.ci_server_poller import CIServerPoller


class StatusScreen(qt.QQuickItem):

    holiday_changed = qt.pyqtSignal()
    holiday_source_changed = qt.pyqtSignal()
    projects_changed = qt.pyqtSignal()
    failed_projects_changed = qt.pyqtSignal()
    error_changed = qt.pyqtSignal()

    on_status_updated = qt.pyqtSignal(dict, dict)

    def __init__(self, *args, **kwargs):
        super(StatusScreen, self).__init__(*args, **kwargs)
        self._projects = ProjectsModel()
        self._failed_projects = ProjectsModel()
        self._error = None
        self._holiday_source = None

    def componentComplete(self):
        super(StatusScreen, self).componentComplete()
        self.on_status_updated.connect(self.on_status_update_on_ui_thread)

        dispatcher.connect(self.on_status_update, "CI_UPDATE", sender=dispatcher.Any)

        self.poller = CIServerPoller()
        self.poller.start_polling_async()

    def update_holiday(self):
        self.holidaySource = "../{}".format(holiday_chooser.get_holiday_widget_path())

    @qt.pyqtProperty(ProjectsModel, notify=projects_changed)
    def projects(self):
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = value
        self.projects_changed.emit()

    @qt.pyqtProperty(ProjectsModel, notify=failed_projects_changed)
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

    def _get_projects_from_responses(self, responses):
        projects = []
        for ci_server in responses:
            jobs = responses[ci_server]
            for job in jobs:
                name = job['name']
                activity = job['activity']
                last_build_status = job['last_build_status']
                last_build_time = job['last_build_time']

                project = Project(name, activity, last_build_status, last_build_time, ci_server)
                projects.append(project)
        return projects

    @qt.pyqtSlot(dict, dict)
    def on_status_update_on_ui_thread(self, responses, errors):
        self.update_holiday()

        bad_ci_servers = errors.keys()
        new_projects = [p for p in self._get_projects_from_responses(responses) if p.lastBuildStatus != 'Unknown']

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
        self.holiday_source_changed.emit()

