let city = document.getElementById('city');
let route = document.getElementById('route');
let button = document.getElementById('selectButton');
let mapElement = document.getElementById('map-container');
let modalContainer = document.getElementById('modal-container');
let modalLink = document.getElementById('modal__link');

let lon;
let lat;
let map;
let marker;
let intervalRefresh;

let url = `ws://${window.location.host}/ws/socket-server/`;
const socket = new WebSocket(url);
socket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    if (data['finished']) {
        clearInterval(intervalRefresh);
        modalContainer.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
    else {
        lon = data['lon'];
        lat = data['lat'];
    }
}


city.addEventListener("change", (e) => {

    route.innerHTML = `<option value="0">Selecciona una opción</option>`;

    if (city.value == '1') {
        route.innerHTML += `
            <option value="1">Magangué-Pinillos</option>
            <option value="2">Magangué-Yati</option>
            <option value="3">Terminal noroccidental-Terminal fluvial</option>
            <option value="4">Barrio Cristo prado-Clínica de los ríos</option>
            <option value="5">Barrio San Pablo-Parque Santa Rita</option>
        `;
    }
    else if (city.value == '2') {
        route.innerHTML += `
            <option value="1">Universidad de Sucre - Terminal de transporte</option>
            <option value="2">Terminal de transportes - Parque Santander</option>
            <option value="3">Barrio El Cortijo - Gobernación</option>
            <option value="4">Altos del rosario - Plaza cultural de Majagual</option>
        `;
    }
});



button.addEventListener("click", (e) => {
    e.preventDefault();
    modalLink.href = modalLink.href.substring(0, modalLink.href.length - 1) + city.value;
    if (route.value != '0') {
        socket.send(JSON.stringify({
            'city': city.value,
            'route': route.value
        }))
        startMap();
        mapElement.classList.remove('hidden');
    }
})

function startMap() {
    let coords;

    if (city.value == '1') {
        coords = { lat: 9.2347399083158, lng: -74.74300089441398 }
    }
    else {
        coords = { lat: 9.300184, lng: -75.395335 }
    }

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: coords
    });

    marker = new google.maps.Marker({
        'map': null
    });

    intervalRefresh = setInterval(() => {
        updateMap();
    }, 500);
}

function updateMap() {
    marker.setMap(null);
    marker = new google.maps.Marker({
        position: { lat: lat * 1, lng: lon * 1 },
        map: map
    })
}