import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1


Item {

    id:root
    property string projectName: ''
    property string buildStatus: ''

    Rectangle {
        id: background
        anchors.fill: parent
    }

    Text {
        anchors.fill: parent
        color: 'white'
        font.bold: true
        font.pointSize: 30
        text: root.projectName
    }

    transform: Translate {
        id: translate
        x: -root.width 
    }

    Component.onCompleted: {
        intro.start()
    }

    states: [
        State {
            when: root.buildStatus == 'Success'
            PropertyChanges { target: background; color: 'green' }
        },
        State {
            when: root.buildStatus == 'Failure'
            PropertyChanges { target: background; color: 'red' }
        }
    ]

    SequentialAnimation {
        id: intro
        PauseAnimation {
            duration: Math.floor(Math.random() * 400)
        }
        NumberAnimation { 
            running: false
            target: translate
            property: 'x'
            to: 0
            duration: 1000
            easing.type: Easing.OutBounce
        }
    }
}

