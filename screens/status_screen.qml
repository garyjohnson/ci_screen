import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1
import Screens 1.0
import '../widgets'

StatusScreen {

    id:root
    anchors.fill: parent

    ColumnLayout {
        anchors.fill: parent

        Repeater {
            model: root.projects

            Project {
                Layout.fillWidth: true
                Layout.fillHeight: true
                model: modelData
            }
        }
    }
}
