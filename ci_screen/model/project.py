import datetime

import dateutil.parser as date_parser
import pytz
import PyQt5.Qt as qt


class Project(qt.QObject):

    name_changed=qt.pyqtSignal()
    activity_changed=qt.pyqtSignal()
    last_build_status_changed=qt.pyqtSignal()
    last_build_time_changed=qt.pyqtSignal()
    last_build_label_changed=qt.pyqtSignal()

    def __init__(self, name, activity, last_build_status, last_build_time, ci_server):
        super(Project, self).__init__()
        self.ci_server = ci_server
        self._name = name
        self._activity = activity
        self._last_build_status = last_build_status
        self._last_build_time = last_build_time
        self._last_build_label = ''
        self.update_last_build_label()
    
    @qt.pyqtProperty(str, notify=name_changed)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit()

    @qt.pyqtProperty(str, notify=activity_changed)
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, value):
        self._activity = value
        self.activity_changed.emit()

    @qt.pyqtProperty(str, notify=last_build_status_changed)
    def lastBuildStatus(self):
        return self._last_build_status

    @lastBuildStatus.setter
    def lastBuildStatus(self, value):
        self._last_build_status = value
        self.last_build_status_changed.emit()

    @qt.pyqtProperty(str, notify=last_build_time_changed)
    def lastBuildTime(self):
        return self._last_build_time

    @lastBuildTime.setter
    def lastBuildTime(self, value):
        self._last_build_time = value
        self.last_build_time_changed.emit()
        self.update_last_build_label()

    @qt.pyqtProperty(str, notify=last_build_label_changed)
    def lastBuildLabel(self):
        return self._last_build_label

    @lastBuildLabel.setter
    def lastBuildLabel(self, value):
        self._last_build_label = value
        self.last_build_label_changed.emit()

    def is_failed(self):
        return self.lastBuildStatus == 'Failure' or self.lastBuildStatus == 'Exception'

    def update_last_build_label(self):
        last_build_datetime = date_parser.parse(self._last_build_time).replace(tzinfo = pytz.utc)
        now = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)

        built_ago = last_build_datetime - now
        minutes_ago = int(abs(int(built_ago.total_seconds())) / 60)
        hours_ago = int(minutes_ago / 60)
        days_ago = int(hours_ago / 24)

        if days_ago > 0:
            self.lastBuildLabel = "{num} day{s} ago".format(num=days_ago, s='s' if days_ago > 1 else '' )
        elif hours_ago > 0:
            self.lastBuildLabel = "{num} hour{s} ago".format(num=hours_ago, s='s' if hours_ago > 1 else '')
        elif minutes_ago > 0:
            self.lastBuildLabel = "{num} minute{s} ago".format(num=minutes_ago, s='s' if minutes_ago > 1 else '')
        else:
            self.lastBuildLabel = "Just Now"
