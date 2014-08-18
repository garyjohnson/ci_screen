import QtQuick 2.2
import QtQuick.Window 2.1

Window {
    id: root

    Loader {
        height: root.height
        width: root.width
        source: 'screens/status_screen.qml'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Regular.ttf'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Bold.ttf'
    }

}
