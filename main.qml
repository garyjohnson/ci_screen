import QtQuick 2.2
import QtQuick.Window 2.1

Loader {

    id: root
    property int parentHeight
    property int parentWidth

    parentHeight: parent == null ? 0 : parent.height
    parentWidth: parent == null ? 0 : parent.width
    x: parentWidth / 2 - width / 2 
    y: parentHeight / 2 - height / 2 
    height: screenRotation % 180 == 0 ? parentHeight : parentWidth
    width: screenRotation % 180 == 0 ? parentWidth : parentHeight
    source: 'screens/status_screen.qml'

    FontLoader {
        source: 'assets/open-sans/OpenSans-Regular.ttf'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Bold.ttf'
    }

    transform: Rotation {
        angle: screenRotation
        origin.x: root.width / 2
        origin.y: root.height / 2
    }
}

