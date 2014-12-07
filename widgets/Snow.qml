import QtQuick 2.2
import QtQuick.Particles 2.0

Item {
    id: root

    property string automation_id: 'snow'
    property bool isSnowing
    property date startDate: "2014-11-15"
    property date endDate: "2014-12-25"

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
        enabled: root.isSnowing
        velocity: PointDirection{ y:80; yVariation: 40; }
        acceleration: PointDirection{ y: 4 }
        size: 20
        sizeVariation: 10
        anchors.fill: parent
    }
}
