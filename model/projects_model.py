import logging

import PyQt5.Qt as qt


logger = logging.getLogger(__name__)

class ProjectsModel(qt.QAbstractListModel):

    NAME_ROLE = qt.Qt.UserRole + 1
    LAST_BUILD_STATUS_ROLE = qt.Qt.UserRole + 2
    LAST_BUILD_LABEL_ROLE = qt.Qt.UserRole + 3
    LAST_BUILD_TIME_ROLE = qt.Qt.UserRole + 4
    ACTIVITY_ROLE = qt.Qt.UserRole + 5
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

    def update(self, updated_project):
        project_to_update = next((p for p in self.projects if p.name == updated_project.name), None)
        if project_to_update is not None:
            project_to_update.lastBuildLabel = updated_project.lastBuildLabel
            project_to_update.lastBuildTime = updated_project.lastBuildTime
            project_to_update.lastBuildStatus = updated_project.lastBuildStatus
            project_to_update.activity = updated_project.activity
            data_position = self.createIndex(self.projects.index(project_to_update), 0, project_to_update)
            self.dataChanged.emit(data_position, data_position)

    def sort_by_last_build_time(self):
        unsorted_projects = list(self.projects)
        
        for project in unsorted_projects:
            project_index = self.projects.index(project)
            desired_index = project_index
            while desired_index - 1 >= 0:
                project_in_the_way = self.projects[desired_index - 1]
                if project.lastBuildTime <= project_in_the_way.lastBuildTime:
                    break
                desired_index -= 1

            if desired_index != project_index:
                self.beginMoveRows(self.parent_index, project_index, project_index, self.parent_index, desired_index)
                self.projects.insert(desired_index, self.projects.pop(project_index))
                self.endMoveRows()

    def roleNames(self):
        roles = {}
        roles[self.NAME_ROLE] = "name"
        roles[self.LAST_BUILD_STATUS_ROLE] = "lastBuildStatus"
        roles[self.LAST_BUILD_LABEL_ROLE] = "lastBuildLabel"
        roles[self.LAST_BUILD_TIME_ROLE] = "lastBuildTime"
        roles[self.ACTIVITY_ROLE] = "activity"
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
            elif role == self.LAST_BUILD_TIME_ROLE:
                return qt.QVariant(project.lastBuildTime)
            elif role == self.ACTIVITY_ROLE:
                return qt.QVariant(project.activity)
        return qt.QVariant()
