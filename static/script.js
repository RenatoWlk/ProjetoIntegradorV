const TOTAL_PARKING_SPOTS = 12;
const UPDATE_INTERVAL = 1000; // Tempo em ms
let refreshIntervalId;

function startVideo(){
    fetch('/process_video')
        .then(() => {
            loadYoloData();
            refreshIntervalId = setInterval(loadYoloData, UPDATE_INTERVAL);
        })
        .catch(error => console.error('Erro ao carregar o vídeo: ', error));
}

function stopVideo(){
    clearInterval(refreshIntervalId)
}

function loadYoloData(){
    fetch('/dados_yolo')
        .then(response => response.json())
        .then(processData)
        .catch(error => console.error('Erro ao carregar os dados do YOLO: ', error));
}

function processData(data){
    let totalBicycle = 0;
    let totalMotorcycle = 0;
    let totalCar = 0;
    let totalTruck = 0;
    let available = TOTAL_PARKING_SPOTS;
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

            const vehicle = getVehicle(bicycle, motorcycle, car)
            const areaNumber = area.substring(4)
            consoleData.push(`O veículo ${vehicle} ocupou a vaga ${areaNumber}`);
        }
    }

    updateElements(totalBicycle, totalMotorcycle, totalCar, totalTruck, available, occupied)
    updateConsole(consoleData);
}

function getVehicle(bicycle, motorcycle, car){
    if (car === 1) return "Carro";
    if (motorcycle === 1) return "Moto";
    if (bicycle === 1) return "Bicicleta";
    return "Caminhão";
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
    const consoleDataTxt = document.getElementById("console-data-txt");
    if (consoleData.length === 0) {
        clearConsole("Não há veículos estacionados no momento.");
    } else {
        consoleDataTxt.innerText = consoleData.join("\n \n");
    }
}

function clearConsole(message){
    document.getElementById("console-data-txt").innerText = message.toString();
}

window.onload = startVideo;

/* FUNÇÃO loadYoloData PARA SOMENTE UMA ÁREA NO ESTACIONAMENTO
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