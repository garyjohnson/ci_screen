#!/usr/bin/env python

import sys
import screens.status_screen as status_screen
import model

import pqaut.server as pqaut
from PyQt5.Qt import QApplication, qmlRegisterType, QUrl, QQuickView, Qt, QWindow


if __name__ == '__main__':

    if '--automation_server' in sys.argv:
        pqaut.start_automation_server()

    app = QApplication(sys.argv)

    qmlRegisterType(status_screen.StatusScreen, 'Screens', 1, 0, 'StatusScreen')
    qmlRegisterType(model.project.Project, 'Model', 1, 0, 'Project')
    qmlRegisterType(model.projects_model.ProjectsModel, 'Model', 1, 0, 'ProjectsModel')

    window = QQuickView(QUrl('main.qml'))
    window.setResizeMode(QQuickView.SizeViewToRootObject)
    window.setFlags(Qt.WindowFullscreenButtonHint)
    window.showFullScreen()

    sys.exit(app.exec_())
