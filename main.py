#!/usr/bin/env python

import sys
import screens.status_screen as status_screen
import model

import PyQt5.Qt as qt
import pqaut.server as pqaut


if __name__ == '__main__':

    if '--automation_server' in sys.argv:
        pqaut.start_automation_server()

    app = qt.QApplication(sys.argv)

    qt.qmlRegisterType(status_screen.StatusScreen, 'Screens', 1, 0, 'StatusScreen')
    qt.qmlRegisterType(model.project.Project, 'Model', 1, 0, 'Project')
    qt.qmlRegisterType(model.projects_model.ProjectsModel, 'Model', 1, 0, 'ProjectsModel')

    engine = qt.QQmlEngine()
    component = qt.QQmlComponent(engine)
    component.loadUrl(qt.QUrl('main.qml'))

    window = component.create()
    window.setVisibility(qt.QWindow.Maximized)
    window.showFullScreen()

    sys.exit(app.exec_())
