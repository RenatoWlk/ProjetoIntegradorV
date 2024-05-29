const TOTAL_PARKING_SPOTS = 19;
const UPDATE_INTERVAL_YOLO_DATA = 3000; // Tempo em ms
const UPDATE_INTERVAL_CHART_DATA = 5000; // Tempo em ms
const ctx = document.getElementById('occupancyChart').getContext('2d');

function startVideo(){
    fetch('/process_video')
        .then(() => {
            loadYoloData();
            fetchOccupancyData();
            setInterval(loadYoloData, UPDATE_INTERVAL_YOLO_DATA);
            setInterval(fetchOccupancyData, UPDATE_INTERVAL_CHART_DATA);
        })
        .catch(error => console.error('Erro ao carregar o vídeo: ', error));
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
        clearConsole("Nenhum veículo no momento.");
    } else {
        consoleDataTxt.innerText = consoleData.join("\n");
    }
}

function clearConsole(message){
    document.getElementById("console-data-txt").innerText = message.toString();
}

window.onload = startVideo;

let occupancyChart;
let labels = [];
let data = [];

function fetchOccupancyData() {
    fetch('/occupancy')
        .then(response => response.json())
        .then(data => {
            labels = [];
            occupied = [];
            const startIndex = Math.max(data.timestamps.length - 25, 0);
            for (let i = startIndex; i < data.timestamps.length; i++) {
                labels.push(new Date(data.timestamps[i]));
                occupied.push(data.occupied_spaces[i]);
            }
            drawChart(labels, occupied);
        })
        .catch(error => console.error('Erro ao carregar dados: ', error));
}

function drawChart(labels, data) {
    const canvas = document.getElementById('occupancyChart');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const maxDataPoint = Math.max(...data, TOTAL_PARKING_SPOTS);
    const padding = 40;
    
    const xStep = labels.length > 0 ? (canvas.width - 2 * padding) / (labels.length - 1) : 0; 
    const yStep = (canvas.height - 2 * padding) / maxDataPoint;

    // Grid
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1;
    for (let i = 0; i <= maxDataPoint; i++) {
        const y = canvas.height - padding - i * yStep;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(canvas.width - padding, y);
        ctx.stroke();
    }
    for (let i = 0; i < labels.length; i++) {
        const x = padding + i * xStep;
        ctx.beginPath();
        ctx.moveTo(x, padding);
        ctx.lineTo(x, canvas.height - padding);
        ctx.stroke();
    }

    // Axes
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();

    // Line
    ctx.beginPath();
    ctx.moveTo(padding, canvas.height - padding - data[0] * yStep);
    for (let i = 1; i < data.length; i++) {
        const x = padding + i * xStep;
        const y = canvas.height - padding - data[i] * yStep;
        ctx.lineTo(x, y);
    }
    ctx.strokeStyle = 'rgba(75, 192, 192, 1)';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Points
    ctx.fillStyle = 'rgba(75, 192, 192, 1)';
    for (let i = 0; i < data.length; i++) {
        const x = padding + i * xStep;
        const y = canvas.height - padding - data[i] * yStep;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
    }

    // Labels
    const labelStep = Math.ceil(labels.length / 10);
    ctx.fillStyle = '#000';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    for (let i = 0; i < labels.length; i += labelStep) {
        const x = padding + i * xStep;
        const y = canvas.height - padding + 5;
        ctx.save();
        ctx.translate(x, y);
        ctx.fillText(labels[i].toLocaleTimeString(), 0, 0);
        ctx.restore();
    }

    // Y-axis labels
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    for (let i = 0; i <= maxDataPoint; i++) {
        const y = canvas.height - padding - i * yStep;
        ctx.fillText(i.toString(), padding - 5, y);
    }

    // Title
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    ctx.font = '16px Montserrat';
    ctx.fillText('Vagas Ocupadas ao Longo do Tempo', canvas.width / 2, padding - 10);
}