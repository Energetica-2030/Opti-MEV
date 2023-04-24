let vehicleListElement = document.getElementById('vehicleList');

let nominalEnergyInput = document.getElementById('nominalEnergyInput');
let nominalAutonomyInput = document.getElementById('nominalAutonomyInput');
let chargingPowerInput = document.getElementById('chargingPowerInput');
let chargingTimeInput = document.getElementById('chargingTimeInput');
let fuelAutonomyInput = document.getElementById('fuelAutonomyInput');
let tankCapacityInput = document.getElementById('tankCapacityInput');

vehicleListElement.addEventListener("change", () => {
    if(vehicleListElement.selectedIndex!=0){
        vehicleName = vehicleListElement.options[vehicleListElement.selectedIndex].innerText;
        getData(vehicleName)
        .then((value) => {
            displayData(value);
        })
        .catch((err) => {
            console.log(err);
        });
    }
    else{
        displayInputs();
    }
});

function getData(vehicleName){
    const url = `getVehicleData/${vehicleName}`;
    const request = new XMLHttpRequest();

    let promise = new Promise((resolve, reject) => {
        request.addEventListener("readystatechange", () => {
            let isCompleted = request.readyState == 4;
            let isOk = request.status == 200;
            if (isCompleted && isOk) resolve(JSON.parse(request.responseText));
            else if (isCompleted && !isOk) reject('Los datos no han sido obtenidos correctamente.');
        });
        request.open('GET', url);
        request.send();
    })
    return promise;
}

function displayData(data){
    nominalEnergyInput.value = data['nominal_energy'];
    nominalAutonomyInput.value = data['nominal_autonomy'];
    chargingPowerInput.value = data['charging_power'];
    chargingTimeInput.value = data['charging_time'];

    nominalEnergyInput.setAttribute('readonly', true);
    nominalAutonomyInput.setAttribute('readonly', true);
    chargingPowerInput.setAttribute('readonly', true);
    chargingTimeInput.setAttribute('readonly', true);

    nominalEnergyInput.classList.add('disabled');
    nominalAutonomyInput.classList.add('disabled');
    chargingPowerInput.classList.add('disabled');
    chargingTimeInput.classList.add('disabled');

    if(window.location.href[window.location.href.length-1]=='2'){
        fuelAutonomyInput.value = data['fuel_autonomy'];
        tankCapacityInput.value = data['tank_capacity'];

        fuelAutonomyInput.setAttribute('readonly', true);
        tankCapacityInput.setAttribute('readonly', true);
        
        fuelAutonomyInput.classList.add('disabled');
        tankCapacityInput.classList.add('disabled');
    }
}

function displayInputs(){
    nominalEnergyInput.value = '';
    nominalAutonomyInput.value = '';
    chargingPowerInput.value = '';
    chargingTimeInput.value = '';

    nominalEnergyInput.removeAttribute('readonly');
    nominalAutonomyInput.removeAttribute('readonly');
    chargingPowerInput.removeAttribute('readonly');
    chargingTimeInput.removeAttribute('readonly');

    nominalEnergyInput.classList.remove('disabled');
    nominalAutonomyInput.classList.remove('disabled');
    chargingPowerInput.classList.remove('disabled');
    chargingTimeInput.classList.remove('disabled');

    if(window.location.href[window.location.href.length-1]=='2'){
        fuelAutonomyInput.value = '';
        tankCapacityInput.value = '';

        fuelAutonomyInput.removeAttribute('readonly');
        tankCapacityInput.removeAttribute('readonly');

        fuelAutonomyInput.classList.remove('disabled');
        tankCapacityInput.classList.remove('disabled');
    }
}