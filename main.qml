import QtQuick 2.2
import QtQuick.Window 2.2

Loader {
    width: Screen.width
    height: Screen.height
    source: 'screens/status_screen.qml'
    asynchronous: true

    FontLoader {
        source: 'assets/open-sans/OpenSans-Regular.ttf'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Bold.ttf'
    }
}

