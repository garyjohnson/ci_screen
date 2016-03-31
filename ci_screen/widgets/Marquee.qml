import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import Widgets 1.0


Marquee {

    id: root

    Rectangle  {
        id: marquee
        anchors.fill: parent
        visible: root.marquee_visible
        color: '#BB000000'

        AnimatedImage {
            property string automation_id: root.marquee_image_url
            source: root.marquee_image_url
            anchors.fill: parent
            anchors.margins: 100
            fillMode: Image.PreserveAspectFit
            onStatusChanged: {
                playing = (status == AnimatedImage.Ready);
                root.onMarqueeStatusChanged(status);
            }
        }
    }
}
