#!/usr/bin/env python

import sys
import screens.status_screen as status_screen
import model.project

import PyQt5.Qt as qt


if __name__ == '__main__':

    app = qt.QApplication(sys.argv)
    engine = qt.QQmlEngine()

    qt.qmlRegisterType(status_screen.StatusScreen, 'Screens', 1, 0, 'StatusScreen')
    qt.qmlRegisterType(model.project.Project, 'Model', 1, 0, 'Project')

    component = qt.QQmlComponent(engine)
    component.loadUrl(qt.QUrl('main.qml'))

    window = component.create()
    window.setVisibility(qt.QWindow.Maximized)
    window.showFullScreen()

    sys.exit(app.exec_())
