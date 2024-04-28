function carregarDadosYOLO() {
    fetch('../frontend/dados_yolo.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById("bicycle").innerText = data.bicycle.toString();
            document.getElementById("motorcycle").innerText = data.motorcycle.toString();
            document.getElementById("car").innerText = data.car.toString();
            document.getElementById("truck").innerText = data.truck.toString();
            document.getElementById("person").innerText = data.person.toString();
        })
        .catch(error => console.error('Erro ao carregar os dados do YOLO:', error));
}

window.onload = carregarDadosYOLO;