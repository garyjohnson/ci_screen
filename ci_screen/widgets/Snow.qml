import QtQuick 2.2
import QtQuick.Particles 2.0

Item {
    id: root

    property string automation_id: 'snow'

    ParticleSystem { id: particles }

    ImageParticle {
        system: particles
        sprites: Sprite{
            source: "../assets/Snowflake.png"
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
        emitRate: 20
        lifeSpan: 7000
        enabled: true
        velocity: PointDirection{ y:80; yVariation: 40; }
        acceleration: PointDirection{ y: 4 }
        size: 20
        sizeVariation: 10
        anchors.fill: parent
    }
}
