import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1


Item {

    id:root
    property string projectName: ''
    property string buildStatus: 'Unknown'
    property string lastBuild: ''

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

    Text {
        id: label
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        anchors.leftMargin: 25
        anchors.topMargin: 5
        color: 'white'
        font.bold: true
        font.pointSize: 30
        text: root.projectName
        verticalAlignment: Text.AlignVCenter
    }

    Text {
        id: last_build_label
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        anchors.rightMargin: 50
        anchors.topMargin: 5
        color: 'white'
        font.bold: true
        font.pointSize: 30
        text: root.lastBuild
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignRight
    }

    state: buildStatus
    states: [
        State {
            name: 'Success'
            PropertyChanges { target: background; color: '#7A8C89' }
            PropertyChanges { target: accent; color: '#909D9E' }
            PropertyChanges { target: label; color: '#1F2525' }
            PropertyChanges { target: last_build_label; color: '#1F2525'; visible: false }
        },
        State {
            name: 'Failure'
            PropertyChanges { target: background; color: '#FF0D51' }
            PropertyChanges { target: accent; color: '#d42043' }
            PropertyChanges { target: label; color: 'white' }
            PropertyChanges { target: last_build_label; color: 'white' }
        },
        State {
            name: 'Exception'
            PropertyChanges { target: background; color: '#FF0D51' }
            PropertyChanges { target: accent; color: '#d42043' }
            PropertyChanges { target: label; color: 'white' }
            PropertyChanges { target: last_build_label; color: 'white' }
        },
        State {
            name: 'Unknown'
            PropertyChanges { target: background; color: '#909D9E' }
            PropertyChanges { target: accent; color: '#7A8C89' }
            PropertyChanges { target: label; color: '#1F2525' }
            PropertyChanges { target: last_build_label; color: '#1F2525' }
        }
    ]
}

