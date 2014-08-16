import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import Screens 1.0
import '../widgets'

StatusScreen {

    id:root
    anchors.fill: parent

    ListView {
        anchors.fill: parent
        model: root.projects

        delegate: Project {
            height: 100
            width: root.width
            projectName: name
            buildStatus: lastBuildStatus
        }
    }
}
