import QtQuick 2.2
import QtQuick.Particles 2.0

Item {
    id: root

    property string automation_id: 'hearts'

    ParticleSystem { id: particles }

    ImageParticle {
        system: particles
        sprites: Sprite{
            source: "../assets/Heart.png"
            frameCount: 1
        }
    }
    Wander { 
        id: wanderer
        system: particles
        anchors.fill: parent
        xVariance: 360/(affectedParameter+1);
        pace: 100*(affectedParameter+1);
    }
    Emitter {
        system: particles
        emitRate: 3
        lifeSpan: 7000
        enabled: true
        velocity: PointDirection{ y:-80; yVariation: 40; }
        acceleration: PointDirection{ y: -4 }
        size: 60
        sizeVariation: 20
        anchors.top: parent.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
    }
}
