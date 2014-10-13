import QtQuick 2.2
import QtQuick.Window 2.1

Loader {
    height: parent == null ? 0 : parent.height
    width: parent == null ? 0 : parent.width
    source: 'screens/status_screen.qml'

    FontLoader {
        source: 'assets/open-sans/OpenSans-Regular.ttf'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Bold.ttf'
    }
}

