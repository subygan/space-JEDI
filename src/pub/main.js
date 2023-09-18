import * as THREE from './three1.js'

// Earth radius in km
// https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
const EARTH_RADIUS = 6378.137;

// debris data
const debrisData = [];

// create Earth globle
const world = Globe()
    .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
    .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
    //.showGraticules(true)
    .showAtmosphere(true)
    (document.getElementById('earthGlobe'));

// custom globe material
const globeMaterial = world.globeMaterial();
globeMaterial.bumpScale = 10;
// Create the Geometry passing the size
// var geometry = new THREE.BoxGeometry( 1, 1, 1 );
let tl = new THREE.TextureLoader().load('https://unpkg.com/three-globe/example/img/earth-water.png', texture => {
    globeMaterial.specularMap = texture;
    globeMaterial.specular = new THREE.Color('grey');
    globeMaterial.shininess = 15;
    const directionalLight = world.scene().children.find(obj3d => obj3d.type === 'DirectionalLight');
    directionalLight && directionalLight.position.set(1, 1, 1);
});

// funtion to update position of debris
(function moveDebris() {
    debrisData.forEach(d => {
        var curTime = new Date();

        var positionEci = satellite.propagate(d.satrec, curTime).position;
        var gmst = satellite.gstime(curTime);
        var positionGd = satellite.eciToGeodetic(positionEci, gmst);

        var altitude = positionGd.height / EARTH_RADIUS;
        var longitudeDeg = satellite.degreesLong(positionGd.longitude);
        var latitudeDeg = satellite.degreesLat(positionGd.latitude);

        d.lat = latitudeDeg;
        d.lng = longitudeDeg;
        d.alt = altitude;
    });

    world.customLayerData(world.customLayerData());
    requestAnimationFrame(moveDebris);
})();

// function to start auto-rotation
function startAutorotation() {
    try {
        var controls = world.controls();
        controls.autoRotateSpeed = 0.5;
        controls.autoRotate = true;
    } catch (e) {
        //console.error(e);
    }
}

//Calling autorotate for globe model
startAutorotation();

// function to stop auto-rotation
function stopAutorotation() {
    try {
        world.controls().autoRotate = false;
    } catch (e) {
        //console.error(e);
    }
}

// element to show status
var elStatus = document.getElementById('elStatus');

var updatingDebris = false;

// function to load/update debris data
function updateDebris() {
    if (updatingDebris) return;

    updatingDebris = true;
    elStatus.innerText = 'Downloading data...';

    try {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open('GET', 'api/latest.json', true);
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
                updatingDebris = false;
                if (xmlhttp.status == 200) {
                    try {
                        elStatus.innerText = 'Deserializing data...';

                        var obj = JSON.parse(xmlhttp.responseText);
                        //console.log(obj);

                        if (obj.i && obj.i.t > 0) {
                            elStatus.innerText = 'Calculating positions...';

                            debrisData.splice(0, debrisData.length);

                            for (var i in obj.l) {
                                var tleName = obj.l[i][0];
                                var tleLine1 = obj.l[i][1];
                                var tleLine2 = obj.l[i][2];
                                var tleLine3 = obj.l[i][3]; // color
                                var tleLine4 = obj.l[i][4]; //size

                                if (tleLine3 === 'green') {
                                    debrisData.push({
                                        name: '',
                                        lat: parseFloat(tleName),
                                        lng: parseFloat(tleLine1),
                                        alt: parseFloat(tleLine2),
                                        // we have not radius data, so we use a (adecuate) random value
                                        radius: 0.5,
                                        color: tleLine3,
                                    });
                                    continue;
                                }

                                var satrec = satellite.twoline2satrec(tleLine1, tleLine2);

                                if (satrec.error) {
                                    ///throw new Exception('Can't create a valid satrec.');
                                    continue;
                                }

                                var curTime = new Date();

                                var positionEci = satellite.propagate(satrec, curTime).position;

                                if (!positionEci) {
                                    //throw new Exception('Can't create a ECI position.');
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
                                    // we have not radius data, so we use a (adecuate) random value
                                    radius: Math.random() * 0.1 + parseFloat(tleLine4),
                                    color: tleLine3,
                                    satrec: satrec
                                });

                                console.log(debrisData);
                            }

                            elStatus.innerText = 'Drawing elements...';

                            // update custom layer
                            world
                                .customLayerData(debrisData)
                                .customThreeObject(d => new THREE.Mesh(
                                    new THREE.SphereGeometry(d.radius),
                                    new THREE.MeshLambertMaterial({ color: d.color })
                                ))
                                .customThreeObjectUpdate((obj, d) => {
                                    Object.assign(obj.position, world.getCoords(d.lat, d.lng, d.alt));
                                })
                                .onCustomLayerClick((obj, event) => {
                                    //console.log(obj);
                                });
                        } else {
                            console.log('No debris data in response.');
                        }
                    } catch (ex) {
                        console.log(ex);
                        ;
                    }
                } else {
                    console.log('Unknow error.');
                }

                elStatus.innerText = 'Live.';
            }
        };
        xmlhttp.send(null);
    } catch (e) {
        console.error(e);

        elStatus.innerText = 'Live.';
        updatingDebris = false;
    }
}

// get debris data
// setInterval(() =>updateDebris(), 1000 * 5);
updateDebris();


// show about modal
function about() {
    modalAbout.style.display = 'block';
}

// modal about
var modalAbout = document.getElementById('modalAbout');

// btn close (modal)
var btnCloseModal = document.getElementsByClassName('close')[0];

btnCloseModal.onclick = function () {
    modalAbout.style.display = 'none';
}


// pwa
let deferredPrompt;
const addBtn = document.querySelector('.add-pwa-button');
addBtn.style.display = 'none';

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    addBtn.style.display = 'block';

    addBtn.addEventListener('click', (e) => {
        addBtn.style.display = 'none';
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                //console.log('User accepted the A2HS prompt');
            } else {
                //console.log('User dismissed the A2HS prompt');
            }
            deferredPrompt = null;
        });
    });
});