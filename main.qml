import QtQuick 2.2
import QtQuick.Window 2.1

Loader {
    id: root
    height: parent == null ? 0 : parent.width
    width: parent == null ? 0 : parent.height
    source: 'screens/status_screen.qml'

    FontLoader {
        source: 'assets/open-sans/OpenSans-Regular.ttf'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Bold.ttf'
    }

    transform: Rotation {
        angle: 270
        origin.x: root.width / 2
        origin.y: root.width / 2
    }
}

