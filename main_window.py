try:
    import ConfigParser as config
except:
    import configparser as config

from PyQt5.Qt import QUrl, QQuickView, Qt, QWindow, QVariant, pyqtProperty, pyqtSignal


class MainWindow(QQuickView):

    rotation_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QQuickView, self).__init__()
        self._rotation = self.get_rotation()
        self.engine().rootContext().setContextProperty('screenRotation', QVariant(self.rotation))
        self.setSource(QUrl('main.qml'))

        self.setHeight(self.screen().size().height())
        self.setWidth(self.screen().size().width())
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.setFlags(Qt.WindowFullscreenButtonHint)

    @pyqtProperty(int, notify=rotation_changed)
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self.rotation_changed.emit()

    def get_rotation(self):
        config_parser = config.SafeConfigParser(allow_no_value=False)
        with open('ci_screen.cfg') as config_file:
            config_parser.readfp(config_file)
        return int(config_parser.get('general', 'rotation'))

