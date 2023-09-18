var satellite = require('satellite.js');
var fs = require('fs');
var updatingDebris = false;

const debrisData = [];
const EARTH_RADIUS = 6378.137;

// Function to load/update debris data
function updateDebris() {
    if (updatingDebris) return;

    updatingDebris = true;

    try {
        // Read the contents of the local 'latest.json' file
        // var path = document.location.pathname;
        // var directory = path.substring(path.indexOf('/'), path.lastIndexOf('/'));
        // console.error('yash - ', directory);
        var latestData = fs.readFileSync('latest.json', 'utf8');
        var obj = JSON.parse(latestData);
        //console.log(obj);

        if (obj.i && obj.i.t > 0) {
            debrisData.splice(0, debrisData.length);

            for (var i in obj.l) {
                var tleName = obj.l[i][0];
                var tleLine1 = obj.l[i][1];
                var tleLine2 = obj.l[i][2];
                var tleLine3 = obj.l[i][3]; // color
                var tleLine4 = obj.l[i][4]; // size

                var satrec = satellite.twoline2satrec(tleLine1, tleLine2);

                if (satrec.error) {
                    ///throw new Exception('Can't create a valid satrec.');
                    continue;
                }

                var curTime = new Date();

                var positionEci = satellite.propagate(satrec, curTime).position;

                if (!positionEci) {
                    //throw an Exception('Can't create an ECI position.');
                    continue;
                }

                var gmst = satellite.gstime(curTime);

                var positionGd = satellite.eciToGeodetic(positionEci, gmst);

                var altitude = positionGd.height / EARTH_RADIUS;
                var longitudeDeg = satellite.degreesLong(positionGd.longitude);
                var latitudeDeg = satellite.degreesLat(positionGd.latitude);

                debrisData.push({
                    name: tleName,
                    lat: latitudeDeg,
                    lng: longitudeDeg,
                    alt: altitude,
                    // we have not radius data, so we use an (adequate) random value
                    radius: Math.random() * 0.1 + parseFloat(tleLine4),
                    color: tleLine3,
                    satrec: satrec
                });

                console.log(debrisData);
            }
            return debrisData;
        } else {
            console.log('No debris data in response.');
        }
    } catch (ex) {
        console.log(ex);
    } finally {
        updatingDebris = false;
    }
}
