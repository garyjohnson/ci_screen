import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import Screens 1.0
import '../widgets'


StatusScreen {

    id:root
    anchors.fill: parent

    Rectangle {
        anchors.fill: parent
        color: '#1F2525'
    }

    ColumnLayout {

        anchors.fill: parent

        Item {
            Layout.preferredHeight: headerImage.height + 20
            Layout.fillWidth: true
            z: 1

            Rectangle {
                anchors.fill: parent
                color: '#909D9E'
            }

            Image { 
                id: headerImage
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 20
                source: '../assets/leandog.png'
                fillMode: Image.PreserveAspectFit
                height: 100
                smooth: true
            }
        }

        Item {
            Layout.fillHeight: true
            Layout.fillWidth: true

            ListView {
                id: listview

                anchors.fill: parent
                anchors.topMargin: 25
                anchors.leftMargin: 25
                model: root.projects

                interactive: false

                highlightRangeMode: ListView.StrictlyEnforceRange
                highlightMoveVelocity: 3200
                snapMode: ListView.SnapToItem
                flickableDirection: Flickable.VerticalFlick
                flickDeceleration: 800
                maximumFlickVelocity: 9000
                keyNavigationWraps: true

                spacing: 20

                delegate: Project {
                    height: 75
                    width: root.width
                    projectName: name
                    buildStatus: lastBuildStatus
                    lastBuild: lastBuildLabel
                }

                populate: Transition {
                    id: populateTransition
                    SequentialAnimation {
                        NumberAnimation { property: 'x'; to: root.width; duration: 0 }
                        PauseAnimation { duration: (Math.random() * 500) + (populateTransition.ViewTransition.index * 0) }
                        NumberAnimation { property: 'x'; from: root.width; to: 0; duration: 700; easing.type: Easing.InOutQuad }
                    }
                }

                add: Transition {
                    id: addTransition
                    SequentialAnimation {
                        NumberAnimation { property: 'x'; to: root.width; duration: 0 }
                        PauseAnimation { duration: (Math.random() * 1000) + (addTransition.ViewTransition.index * 0) }
                        NumberAnimation { property: 'x'; from: root.width; to: 0; duration: 500; easing.type: Easing.InOutQuad }
                    }
                }

                remove: Transition {
                    SequentialAnimation {
                        PropertyAction { property: 'ListView.delayRemove'; value: true }
                        NumberAnimation { property: 'x'; from: 0; to: root.width; duration: 500; easing.type: Easing.InOutQuad }
                        PropertyAction { property: 'ListView.delayRemove'; value: false }
                    }
                }

                displaced: Transition {
                    NumberAnimation { property: 'x,y'; duration: 500; easing.type: Easing.InOutQuad }
                }
            }
        }
    }

    SequentialAnimation {
        id: marqueeAnimation
        running: true
        loops: Animation.Infinite

        PauseAnimation { duration: 5000 }
        ScriptAction { script: {
                var itemsPerPage = Math.floor(listview.height / 95)
                var itemsToScroll = itemsPerPage
                var desiredIndex = listview.currentIndex + itemsPerPage
                if (desiredIndex > listview.count - 1) {
                    itemsToScroll = Math.floor(listview.count % itemsPerPage)
                } 

                for (var i = 0; i < itemsToScroll; i++) {
                    listview.incrementCurrentIndex()
                }
            }
        }
    }
}
