#!/usr/bin/env python

import sys
import signal
import model

import pqaut.server as pqaut
from PyQt5.Qt import QApplication, qmlRegisterType, QUrl, QQuickView, Qt, QWindow

import screens.status_screen as status_screen


def exit_on_ctrl_c():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    exit_on_ctrl_c()

    if '--automation_server' in sys.argv:
        pqaut.start_automation_server()

    app = QApplication(sys.argv)

    qmlRegisterType(status_screen.StatusScreen, 'Screens', 1, 0, 'StatusScreen')
    qmlRegisterType(model.project.Project, 'Model', 1, 0, 'Project')
    qmlRegisterType(model.projects_model.ProjectsModel, 'Model', 1, 0, 'ProjectsModel')

    window = QQuickView(QUrl('main.qml'))
    window.setHeight(window.screen().size().height())
    window.setWidth(window.screen().size().width())

    window.setResizeMode(QQuickView.SizeRootObjectToView)
    window.setFlags(Qt.WindowFullscreenButtonHint)
    window.showFullScreen()

    sys.exit(app.exec_())
