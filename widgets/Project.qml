import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1


Item {

    id:root
    property string projectName: ''
    property string buildStatus: 'Unknown'
    property string lastBuild: ''

    transformOrigin: Item.Right

    SequentialAnimation {
        id: failAnimation
        loops: Animation.Infinite
        PauseAnimation { duration: 3000 }
        NumberAnimation { target: root; properties: "scale"; to: 0.97; duration: 100; easing.type: Easing.OutQuad }
        NumberAnimation { target: root; properties: "scale"; to: 1.03; duration: 100; easing.type: Easing.InOutQuad }
        NumberAnimation { target: root; properties: "scale"; to: 1; duration: 75; easing.type: Easing.InOutQuad }
        NumberAnimation { target: root; properties: "scale"; to: 1.03; duration: 100; easing.type: Easing.InOutQuad }
        NumberAnimation { target: root; properties: "scale"; to: 1; duration: 60; easing.type: Easing.InQuad }
        PauseAnimation { duration: 4000 }
    }

    Rectangle {
        id: background
        anchors.fill: parent
    }

    Rectangle {
        id: accent
        height: 5
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
    }

    RowLayout {

        anchors.fill: parent
        anchors.leftMargin: 25
        anchors.rightMargin: 50
        anchors.topMargin: 5

        spacing: 50

        Text {
            id: label
            Layout.fillWidth: true
            color: 'white'
            font.family: 'Open Sans'
            font.pointSize: 30
            text: root.projectName
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            id: lastBuildLabel
            color: 'white'
            font.family: 'Open Sans'
            font.bold: true
            font.pointSize: 30
            text: root.lastBuild
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignRight
        }
    }

    state: buildStatus
    states: [
        State {
            name: 'Success'
            PropertyChanges { target: background; color: '#55c55f' }
            PropertyChanges { target: accent; color: '#36833e' }
            PropertyChanges { target: label; color: '#1F2525'; font.bold: false }
            PropertyChanges { target: lastBuildLabel; color: '#1F2525'; visible: false }
            PropertyChanges { target: failAnimation; running: false }
        },
        /*
        State {
            name: 'Success'
            PropertyChanges { target: background; color: '#94c093' }
            PropertyChanges { target: accent; color: '#688868' }
            PropertyChanges { target: label; color: '#1F2525'; font.bold: false }
            PropertyChanges { target: lastBuildLabel; color: '#1F2525'; visible: false }
            PropertyChanges { target: failAnimation; running: false }
        },
        */
        /*
        State {
            name: 'Success'
            PropertyChanges { target: background; color: '#7A8C89' }
            PropertyChanges { target: accent; color: '#909D9E' }
            PropertyChanges { target: label; color: '#1F2525'; font.bold: false }
            PropertyChanges { target: lastBuildLabel; color: '#1F2525'; visible: false }
            PropertyChanges { target: failAnimation; running: false }
        },
        */
        State {
            name: 'Failure'
            PropertyChanges { target: background; color: '#FF0D51' }
            PropertyChanges { target: accent; color: '#d42043' }
            PropertyChanges { target: label; color: 'white'; font.bold: true }
            PropertyChanges { target: lastBuildLabel; color: 'white' }
            PropertyChanges { target: failAnimation; running: true }
        },
        State {
            name: 'Exception'
            PropertyChanges { target: background; color: '#FF0D51' }
            PropertyChanges { target: accent; color: '#d42043' }
            PropertyChanges { target: label; color: 'white'; font.bold: true }
            PropertyChanges { target: lastBuildLabel; color: 'white' }
            PropertyChanges { target: failAnimation; running: true }
        },
        State {
            name: 'Unknown'
            PropertyChanges { target: background; color: '#909D9E' }
            PropertyChanges { target: accent; color: '#7A8C89' }
            PropertyChanges { target: label; color: '#1F2525'; font.bold: false }
            PropertyChanges { target: lastBuildLabel; color: '#1F2525' }
            PropertyChanges { target: failAnimation; running: false }
        }
    ]
}

