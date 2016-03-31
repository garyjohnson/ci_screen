#!/usr/bin/env python

import os
import sys
import signal
import logging

import pqaut.server as pqaut
from PyQt5.Qt import QApplication, qmlRegisterType
from freezegun import freeze_time

import ci_screen.widgets.now_playing as now_playing
import ci_screen.widgets.marquee as marquee
import ci_screen.screens.status_screen as status_screen
import ci_screen.main_window as main_window
import ci_screen.model as model
import ci_screen.service.mqtt_service as mqtt_service


def exit_on_ctrl_c():
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    exit_on_ctrl_c()

    if '--automation_server' in sys.argv:
        pqaut.start_automation_server()

    if 'FREEZETIME' in os.environ:
        freeze_time(os.environ['FREEZETIME'], tz_offset=0).start()

    app = QApplication(sys.argv)

    qmlRegisterType(status_screen.StatusScreen, 'Screens', 1, 0, 'StatusScreen')
    qmlRegisterType(now_playing.NowPlaying, 'Widgets', 1, 0, 'NowPlaying')
    qmlRegisterType(marquee.Marquee, 'Widgets', 1, 0, 'Marquee')
    qmlRegisterType(model.project.Project, 'Model', 1, 0, 'Project')
    qmlRegisterType(model.projects_model.ProjectsModel, 'Model', 1, 0, 'ProjectsModel')

    window = main_window.MainWindow()
    window.showFullScreen()

    mqtt = mqtt_service.MqttService()
    mqtt.start()

    sys.exit(app.exec_())


if __name__ == '__main__':

    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
    }
    log_level_name = os.environ.get('CI_LOG', 'ERROR')
    logging.basicConfig(level=log_levels[log_level_name])
    logging.getLogger().setLevel(log_levels[log_level_name])
    logger = logging.getLogger(__name__)
    logger.debug('ci_screen log level is {}'.format(log_level_name))

    main()
