#!/usr/bin/env python

import sys

import PyQt5.Qt as Qt


if __name__ == '__main__':

    app = Qt.QApplication(sys.argv)
    engine = Qt.QQmlEngine()

    component = Qt.QQmlComponent(engine)
    component.loadUrl(Qt.QUrl('main.qml'))

    window = component.create()
    window.setVisibility(Qt.QWindow.Maximized)
    window.showFullScreen()

    sys.exit(app.exec_())
