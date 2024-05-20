function loadYoloData(){
    fetch('/dados_yolo')
        .then(response => response.json())
        .then(data => processData(data))
        .catch(error => console.error('Erro ao carregar os dados do YOLO:', error));
}

function processData(data){
    let totalBicycle = 0;
    let totalMotorcycle = 0;
    let totalCar = 0;
    let totalTruck = 0;
    let available = 12;
    let occupied = 0;
    let consoleData = [];

    for(let area in data) {
        const { bicycle, motorcycle, car, truck, occupied: isOccupied } = data[area];

        totalBicycle += bicycle;
        totalMotorcycle += motorcycle;
        totalCar += car;
        totalTruck += truck;

        if(isOccupied){
            available--;
            occupied++;

            vehicle = getVehicle(bicycle, motorcycle, car)
            areaNumber = area.substring(4)
            consoleData.push(`O veículo ${vehicle} ocupou a vaga ${areaNumber}`);
        }
    }

    updateElements(totalBicycle, totalMotorcycle, totalCar, totalTruck, available, occupied)
    updateConsole(consoleData);
}

function getVehicle(bicycle, motorcycle, car){
    if(car === 1){
        return "Carro"
    }
    else if(motorcycle === 1){
        return "Moto"
    }
    else if(bicycle === 1){
        return "Bicicleta"
    }
    else{
        return "Caminhão"
    }
}

function updateElements(bicycle, motorcycle, car, truck, available, occupied){
    document.getElementById("bicycle").innerText = bicycle.toString();
    document.getElementById("motorcycle").innerText = motorcycle.toString();
    document.getElementById("car").innerText = car.toString();
    document.getElementById("truck").innerText = truck.toString();
    document.getElementById("available-text").innerText = "Livres: " + available
    document.getElementById("occupied-text").innerText = "Ocupadas: " + occupied
}

function updateConsole(consoleData){
    if(consoleData.length === 0){
        clearConsole("Não há veículos estacionados no momento.")
        return 
    }
    else{
        const consoleDataTxt = document.getElementById("console-data-txt");
        consoleDataTxt.innerText = consoleData.join("\n");
    }
}

function clearConsole(message){
    const consoleDataTxt = document.getElementById("console-data-txt");
    consoleDataTxt.innerText = message.toString()
}

/*
function loadYoloData() {
    fetch('/dados_yolo')
        .then(response => response.json())
        .then(data => {
            document.getElementById("bicycle").innerText = data.bicycle.toString();
            document.getElementById("motorcycle").innerText = data.motorcycle.toString();
            document.getElementById("car").innerText = data.car.toString();
            document.getElementById("truck").innerText = data.truck.toString();
            document.getElementById("person").innerText = data.person.toString();
        })
        .catch(error => console.error('Erro ao carregar dados do YOLO:', error))
}
*/

let refreshIntervalId;

function startVideo(){
    fetch('/process_video')
        .then(() => {
            loadYoloData();
            refreshIntervalId = setInterval(loadYoloData, 1000);
        })
        .catch(error => console.error('Erro ao carregar o vídeo:', error));
}

// Precisa implementar um jeito de usar isso para parar de puxar os dados do yolo quando não tiver tocando o "vídeo"
function stopVideo(){
    clearInterval(refreshIntervalId)
}

window.onload = function(){
    startVideo();
};