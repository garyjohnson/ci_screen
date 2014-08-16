import PyQt5.Qt as qt

class Project(qt.QObject):

    name_changed=qt.pyqtSignal()
    activity_changed=qt.pyqtSignal()
    last_build_status_changed=qt.pyqtSignal()
    last_build_time_changed=qt.pyqtSignal()

    def __init__(self, name, activity, last_build_status, last_build_time):
        super(Project, self).__init__()
        self._name = name
        self._activity = activity
        self._last_build_status = last_build_status
        self._last_build_time = last_build_time
    
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
