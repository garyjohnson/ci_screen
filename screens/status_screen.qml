import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import Screens 1.0
import '../widgets'


StatusScreen {

    id:root

    property real itemHeight: 75
    property real itemSpacing: 20

    anchors.fill: parent

    Rectangle {
        anchors.fill: parent
        color: '#1F2525'
    }

    ColumnLayout {

        anchors.fill: parent

        Item {
            z: 1

            Layout.preferredHeight: headerImage.height + 20
            Layout.fillWidth: true

            Rectangle {
                anchors.fill: parent
                color: '#CCCCCC'
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
            z: 2

            Layout.preferredHeight: (root.itemHeight + root.itemSpacing) * failedList.count
            Layout.fillWidth: true

            Rectangle {
                anchors.fill: parent
                color: '#1F2525'
            }

            ListView {
                id: failedList

                anchors.fill: parent
                anchors.topMargin: 25
                anchors.leftMargin: 25

                interactive: false
                spacing: root.itemSpacing

                model: root.failed_projects
                delegate: projectTemplate

                populate: populateTransition
                add: addTransition
                remove: removeTransition
                displaced: displacedTransition
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

                interactive: false

                snapMode: ListView.SnapToItem
                keyNavigationWraps: true

                spacing: root.itemSpacing

                model: root.projects
                delegate: projectTemplate

                populate: populateTransition
                add: addTransition
                remove: removeTransition
                displaced: displacedTransition
            }
        }
    }

    Component {
        id: projectTemplate
        Project {
            height: root.itemHeight
            width: root.width
            projectName: name
            buildStatus: lastBuildStatus
            lastBuild: lastBuildLabel
        }
    }

    Transition {
        id: populateTransition
        SequentialAnimation {
            NumberAnimation { property: 'x'; to: root.width; duration: 0 }
            PauseAnimation { duration: (Math.random() * 500) + (populateTransition.ViewTransition.index * 0) }
            NumberAnimation { property: 'x'; from: root.width; to: 0; duration: 300; easing.type: Easing.InOutQuad }
        }
    }

    Transition {
        id: addTransition
        SequentialAnimation {
            NumberAnimation { property: 'x'; to: root.width; duration: 0 }
            PauseAnimation { duration: (Math.random() * 1000) + (addTransition.ViewTransition.index * 0) }
            NumberAnimation { property: 'x'; from: root.width; to: 0; duration: 300; easing.type: Easing.InOutQuad }
        }
    }

    Transition {
        id: removeTransition
        SequentialAnimation {
            PropertyAction { property: 'ListView.delayRemove'; value: true }
            NumberAnimation { property: 'x'; from: 0; to: root.width; duration: 300; easing.type: Easing.InOutQuad }
            PropertyAction { property: 'ListView.delayRemove'; value: false }
        }
    }

    Transition {
        id: displacedTransition
        NumberAnimation { property: 'x,y'; duration: 300; easing.type: Easing.InOutQuad }
    }

    SequentialAnimation {
        id: marqueeAnimation
        running: true
        loops: Animation.Infinite

        PauseAnimation { duration: 5000 }
        ScriptAction { script: {
                var itemsPerPage = Math.floor(listview.height / (root.itemHeight + root.itemSpacing))
                var desiredIndex = listview.currentIndex + itemsPerPage
                if (desiredIndex > listview.count - 1) {
                    desiredIndex = 0
                } 

                var currentY = listview.contentY;
                var destinationY
                listview.currentIndex = desiredIndex
                listview.positionViewAtIndex(desiredIndex, ListView.Beginning);
                destinationY = listview.contentY;
                scrollAnimation.from = currentY;
                scrollAnimation.to = destinationY;
                scrollAnimation.running = true
            }
        }
    }

    NumberAnimation { id: scrollAnimation; target: listview; property: "contentY"; duration: 500; easing.type: Easing.InOutQuad }
}
