import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtGraphicalEffects 1.0
import Widgets 1.0


NowPlaying {

    id:root

    GridLayout {
        anchors.fill: parent
        columnSpacing: 20
        columns: 2
        rows: 1

        GridLayout {
            anchors.fill: parent
            rows: 2
            columns: 1

            Text {
                property string automation_id: root.song
                property string automation_type: 'song'
                Layout.fillWidth: true
                Layout.topMargin: 8
                color: 'white'
                font.family: 'Open Sans'
                font.weight: Font.Black
                font.pointSize: 35
                text: root.song
                elide: Text.ElideRight
                horizontalAlignment: Text.AlignRight
                verticalAlignment: Text.AlignVCenter
            }

            Text {
                property string automation_id: root.artist
                property string automation_type: 'artist'
                Layout.fillWidth: true
                Layout.topMargin: -8
                Layout.bottomMargin: 8
                color: 'white'
                font.family: 'Open Sans'
                font.weight: Font.Light
                font.pointSize: 25
                text: root.artist
                elide: Text.ElideRight
                horizontalAlignment: Text.AlignRight
                verticalAlignment: Text.AlignVCenter
            }
        }

        Image { 
            property string automation_id: root.albumArt
            property string automation_type: 'albumArt'
            id: albumArt
            source: root.albumArt
            fillMode: Image.PreserveAspectFit
            height: root.height - 20
            sourceSize.height: root.height - 20
            smooth: true
        }
    }
}
