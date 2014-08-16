import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1

RowLayout {

    id:root

    property var model: undefined

    Text {
        Layout.fillWidth: true
        Layout.fillHeight: true
        text: root.model.name
    }
    Text {
        Layout.preferredWidth: 300
        Layout.fillHeight: true
        text: root.model.lastBuildStatus
    }
    Text {
        Layout.preferredWidth: 300
        Layout.fillHeight: true
        text: root.model.lastBuildTime
    }
}
