import QtQuick 2.2
import QtQuick.Particles 2.0

Item {
    id: root

    property string automation_id: 'weird'

    ParticleSystem { id: particles }

    ImageParticle {
        rotation: 0
        rotationVariation: 360
        rotationVelocity: 2
        rotationVelocityVariation: 100
        system: particles
        sprites: Sprite{
            source: "../assets/Cage.png"
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
        emitRate: 0.05
        lifeSpan: 7000
        enabled: true
        velocity: PointDirection{ y:200; yVariation: 100; }
        acceleration: PointDirection{ y: 4 }
        size: 200
        sizeVariation: 20
        anchors.top: parent.top
        anchors.bottom: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
    }
}
