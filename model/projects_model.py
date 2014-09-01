import PyQt5.Qt as qt

class ProjectsModel(qt.QAbstractListModel):

    NAME_ROLE = qt.Qt.UserRole + 1
    LAST_BUILD_STATUS_ROLE = qt.Qt.UserRole + 2
    LAST_BUILD_LABEL_ROLE = qt.Qt.UserRole + 3
    parent_index = qt.QModelIndex()

    def __init__(self):
        super(ProjectsModel, self).__init__()
        self.projects = []

    def append(self, project):
        self.beginInsertRows(qt.QModelIndex(), len(self.projects), len(self.projects))
        self.projects.append(project)
        self.endInsertRows()

    def remove(self, project):
        self.beginRemoveRows(self.parent_index, self.projects.index(project), self.projects.index(project))
        self.projects.remove(project)
        self.endRemoveRows()

    def update(self, project, last_build_status):
        project.lastBuildStatus = last_build_status
        data_position = self.createIndex(self.projects.index(project), 0, project)
        self.dataChanged.emit(data_position, data_position)

    def roleNames(self):
        roles = {}
        roles[self.NAME_ROLE] = "name"
        roles[self.LAST_BUILD_STATUS_ROLE] = "lastBuildStatus"
        roles[self.LAST_BUILD_LABEL_ROLE] = "lastBuildLabel"
        return roles

    def rowCount(self, parent=parent_index):
        return len(self.projects)

    def data(self, index, role=NAME_ROLE):
        if index.isValid() is True:
            project = self.projects[index.row()]
            if role == self.NAME_ROLE:
                return qt.QVariant(project.name)
            elif role == self.LAST_BUILD_STATUS_ROLE:
                return qt.QVariant(project.lastBuildStatus)
            elif role == self.LAST_BUILD_LABEL_ROLE:
                return qt.QVariant(project.lastBuildLabel)
        return qt.QVariant()
