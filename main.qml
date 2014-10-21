import QtQuick 2.2
import QtQuick.Window 2.1

Loader {

    id: root
    property int parentHeight
    property int parentWidth

    //x: parentWidth / 2 - width / 2 
    //y: parentHeight / 2 - height / 2 
    anchors.centerIn: parent
    parentHeight: parent == null ? 0 : parent.height
    parentWidth: parent == null ? 0 : parent.width
    height: screenRotation % 180 == 0 ? parentHeight : parentWidth
    width: screenRotation % 180 == 0 ? parentWidth : parentHeight

    source: 'screens/status_screen.qml'

    transform: Rotation {
        angle: screenRotation
        origin.x: root.width / 2
        origin.y: root.height / 2
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Regular.ttf'
    }

    FontLoader {
        source: 'assets/open-sans/OpenSans-Bold.ttf'
    }
}

