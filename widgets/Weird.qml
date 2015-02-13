import QtQuick 2.2
import QtQuick.Particles 2.0

Item {
    id: root

    property string automation_id: 'weird'

    ParticleSystem { id: particles }

    ImageParticle {
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
        emitRate: 10
        lifeSpan: 7000
        enabled: true
        velocity: PointDirection{ y:0; yVariation: 100; x:0; xVariation: 100; }
        acceleration: PointDirection{ y:30; yVariation: 100; x:30; xVariation: 100; }
        size: 100
        sizeVariation: 100
        anchors.fill: parent
    }
}
