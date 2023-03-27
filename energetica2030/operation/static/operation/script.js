let lon;
let lat;
var map;
var marker;

let url = `ws://${window.location.host}/ws/socket-server/`;
const socket = new WebSocket(url);
socket.onmessage = function(event){
    let data = JSON.parse(event.data);
    lon = data['lon'];
    lat = data['lat'];
    console.log(data);
}


let city = document.getElementById('city');
let route = document.getElementById('route');
city.addEventListener("change", (e)=>{
    
    if(route.children.length==6){
        for(let i = 1; i<=5; i++){
            route.removeChild(route.children[1]);
        }
    }
    else if(route.children.length==5){
        for(let i = 1; i<=4; i++){
            route.removeChild(route.children[1]);
        }
    }
    if(city.value=='1'){
        /*
            <option value="1">Magangué-Pinillos</option>
            <option value="2">Magangué-Yati</option>
            <option value="3">Terminal noroccidental-Terminal fluvial</option>
            <option value="4">Barrio Cristo prado-Clínica de los ríos</option>
            <option value="5">Barrio San Pablo-Parque Santa Rita</option>
        */

        let fragment = document.createDocumentFragment();
        let routes = ['Magangué-Pinillos', 'Magangué-Yati', 'Terminal noroccidental-Terminal fluvial', 'Barrio Cristo prado-Clínica de los ríos', 'Barrio San Pablo-Parque Santa Rita'];
        for(let i=1; i<=5; i++){
            let option = document.createElement("option");
            option.value = i;
            option.innerHTML = routes[i-1];
            fragment.appendChild(option);
        }
        route.appendChild(fragment);
    }
    else if(city.value=='2'){
        /*
            <option value="1">Universidad de Sucre - Terminal de transporte</option>
            <option value="2">Terminal de transportes - Parque Santander</option>
            <option value="3">Barrio El Cortijo - Gobernación</option>
            <option value="4">Altos del rosario - Plaza cultural de Majagual</option>
        */

        let fragment = document.createDocumentFragment();
        let routes = ['Universidad de Sucre - Terminal de transporte','Terminal de transportes - Parque Santander','Barrio El Cortijo - Gobernación','Altos del rosario - Plaza cultural de Majagual'];
        for(let i=1; i<=4; i++){
            let option = document.createElement("option");
            option.value = i;
            option.innerHTML = routes[i-1];
            fragment.appendChild(option);
        }
        route.appendChild(fragment);
    }
});


let button = document.getElementById('selectButton');
button.addEventListener("click",(e)=>{
    e.preventDefault();
    if(route.value!='0'){
        socket.send(JSON.stringify({
            'city': city.value,
            'route':route.value
        }))
        startMap()
        let mapElement = document.getElementById('map-container');
        mapElement.style.display='block';
    }
})

function startMap(){
    if(city.value=='1'){
        coords = {lat:9.2347399083158, lng:-74.74300089441398}
    }
    else{
        coords = {lat:9.300184, lng:-75.395335}
    }
    map = new google.maps.Map(document.getElementById('map'),{
        zoom:14,
        center:coords
    });

    marker = new google.maps.Marker({
        'map':null
    });
}

function updateMap(){
    marker.setMap(null);
    marker = new google.maps.Marker({
        position: {lat:lat*1, lng:lon*1},
        map: map
    })
}

setInterval(()=>{
    if(map!==undefined){
        updateMap();
    }
}, 500);