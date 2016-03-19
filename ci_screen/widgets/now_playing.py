import PyQt5.Qt as qt
from pydispatch import dispatcher


class NowPlaying(qt.QQuickItem):

    now_playing_changed = qt.pyqtSignal()
    on_now_playing_updated = qt.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(NowPlaying, self).__init__(*args, **kwargs)
        print('now playing!')
        self._artist = ''
        self._song = ''
        self._album = ''
        self._album_art = None

    def componentComplete(self):
        super(NowPlaying, self).componentComplete()
        print('component complete')
        self.on_now_playing_updated.connect(self.on_now_playing_update_on_ui_thread)
        dispatcher.connect(self.on_now_playing_update, "NOW_PLAYING_UPDATE", sender=dispatcher.Any)

    def on_now_playing_update(self, now_playing):
        self.on_now_playing_updated.emit(now_playing)

    @qt.pyqtSlot(dict)
    def on_now_playing_update_on_ui_thread(self, now_playing):
        print('now playing update ui')
        print(now_playing)
        self._song = now_playing['song']
        self._artist = now_playing['artist']
        self._album = now_playing['album']
        self._album_art = now_playing['albumArt']
        print(self._album_art)
        self.now_playing_changed.emit()
        print('now playing changed emitted')

    @qt.pyqtProperty(str, notify=now_playing_changed)
    def artist(self):
        return self._artist

    @qt.pyqtProperty(str, notify=now_playing_changed)
    def song(self):
        print('get song')
        return self._song

    @qt.pyqtProperty(str, notify=now_playing_changed)
    def album(self):
        return self._album

    @qt.pyqtProperty(qt.QUrl, notify=now_playing_changed)
    def albumArt(self):
        return qt.QUrl(self._album_art)
