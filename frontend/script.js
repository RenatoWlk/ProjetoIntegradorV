function carregarDadosYOLO() {
    fetch('D:\\Documents\\ProjetoIntegradorV\\frontend\\dados_yolo.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById("carro").innerText = data.carro.toString();
        })
        .catch(error => console.error('Erro ao carregar os dados do YOLO:', error));
}

window.onload = carregarDadosYOLO;