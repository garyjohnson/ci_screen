import logging

import PyQt5.Qt as qt
from pydispatch import dispatcher


IMAGE_READY = 1
IMAGE_ERROR = 3


class Marquee(qt.QQuickItem):

    marquee_visible_changed = qt.pyqtSignal()
    marquee_image_url_changed = qt.pyqtSignal()

    on_show_marquee = qt.pyqtSignal(int, str)

    def __init__(self, *args, **kwargs):
        super(Marquee, self).__init__(*args, **kwargs)
        self._marquee_visible = False
        self._marquee_image_url = ''
        self._marquee_duration = 0
        self._marquee_timer = None

    def componentComplete(self):
        super(Marquee, self).componentComplete()
        self.on_show_marquee.connect(self.on_show_marquee_on_ui_thread)

        dispatcher.connect(self.on_marquee, "SHOW_MARQUEE", sender=dispatcher.Any)

    @qt.pyqtProperty(bool, notify=marquee_visible_changed)
    def marquee_visible(self):
        return self._marquee_visible

    @marquee_visible.setter
    def marquee_visible(self, value):
        self._marquee_visible = value
        self.marquee_visible_changed.emit()

    @qt.pyqtProperty(str, notify=marquee_image_url_changed)
    def marquee_image_url(self):
        return self._marquee_image_url

    @marquee_image_url.setter
    def marquee_image_url(self, value):
        self._marquee_image_url = value
        self.marquee_image_url_changed.emit()

    @qt.pyqtSlot(int, str)
    def on_show_marquee_on_ui_thread(self, duration, image_url):
        self.marquee_duration = duration
        self.marquee_image_url = ''
        self.marquee_image_url = image_url

    @qt.pyqtSlot(int)
    def onMarqueeStatusChanged(self, value):
        if value == IMAGE_READY:
            self.marquee_visible = True

            if self._marquee_timer:
                self._marquee_timer.stop()
            self._marquee_timer = qt.QTimer.singleShot(self.marquee_duration, self._on_marquee_duration_finished)
        elif value == IMAGE_ERROR:
            if self._marquee_timer:
                self._marquee_timer.stop()
                self._marquee_timer = None
            self.marquee_visible = False
            self.marquee_image_url = ''
            self.marquee_duration = 0

    @qt.pyqtSlot()
    def _on_marquee_duration_finished(self):
        self._marquee_timer = None
        self.marquee_visible = False
        self.marquee_image_url = ''
        self.marquee_duration = 0

    def on_marquee(self, duration, image_url):
        self.on_show_marquee.emit(duration, image_url)
