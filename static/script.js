function loadYoloData() {
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
    let totalPerson = 0;
    let available = 12;
    let occupied = 0;

    for(let area in data) {
        const { bicycle, motorcycle, car, truck, person, occupied: isOccupied } = data[area];

        totalBicycle += bicycle;
        totalMotorcycle += motorcycle;
        totalCar += car;
        totalTruck += truck;
        totalPerson += person;

        if(isOccupied){
            available--;
            occupied++;
        }
    }

    updateElements(totalBicycle, totalMotorcycle, totalCar, totalTruck, totalPerson, available, occupied)
}

function updateElements(bicycle, motorcycle, car, truck, person, available, occupied){
    document.getElementById("bicycle").innerText = bicycle.toString();
    document.getElementById("motorcycle").innerText = motorcycle.toString();
    document.getElementById("car").innerText = car.toString();
    document.getElementById("truck").innerText = truck.toString();
    document.getElementById("person").innerText = person.toString();
    document.getElementById("available-text").innerText = "Livres: " + available
    document.getElementById("occupied-text").innerText = "Ocupadas: " + occupied
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

function startVideo() {
    fetch('/process_video')
        .then(() => {
            loadYoloData();
            refreshIntervalId = setInterval(loadYoloData, 1000);
        })
        .catch(error => console.error('Erro ao carregar o vídeo:', error));
}

// Precisa implementar um jeito de usar isso para parar de puxar os dados do yolo quando não tiver tocando o "vídeo"
function stopVideo() {
    clearInterval(refreshIntervalId)
}

window.onload = function() {
    startVideo();
};