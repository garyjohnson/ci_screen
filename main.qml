import QtQuick 2.2
import QtQuick.Window 2.1

Loader {
    anchors.fill: parent
    source: 'screens/status_screen.qml'
    asynchronous: true

    FontLoader {
        source: 'assets/open-sans/OpenSans-Regular.ttf'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Bold.ttf'
    }
}

