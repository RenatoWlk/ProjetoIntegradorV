let refreshIntervalId;

function loadYoloData() {
    fetch('/dados_yolo')
        .then(response => response.json())
        .then(data => {
            let totalBicycle = 0;
            let totalMotorcycle = 0;
            let totalCar = 0;
            let totalTruck = 0;
            let totalPerson = 0;

            for(let area in data) {
                if(data.hasOwnProperty(area)) {
                    totalBicycle += data[area].bicycle;
                    totalMotorcycle += data[area].motorcycle;
                    totalCar += data[area].car;
                    totalTruck += data[area].truck;
                    totalPerson += data[area].person;
                }
            }

            document.getElementById("bicycle").innerText = totalBicycle.toString();
            document.getElementById("motorcycle").innerText = totalMotorcycle.toString();
            document.getElementById("car").innerText = totalCar.toString();
            document.getElementById("truck").innerText = totalTruck.toString();
            document.getElementById("person").innerText = totalPerson.toString();
        })
        .catch(error => console.error('Erro ao carregar os dados do YOLO:', error));
}

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