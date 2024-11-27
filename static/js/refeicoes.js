function obterData() {
    let data = new Date();

    let ano = data.getFullYear();
    let mes = String(data.getMonth() + 1).padStart(2, '0');
    let dia = String(data.getDate()).padStart(2, '0');

    return `${ano}-${mes}-${dia}`;
}

const days = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"];
const nome = ['Café', 'Almoço', 'Lanche', 'Janta'];

const container = document.querySelector(".controll_days");

days.forEach(day => {
    const card = document.createElement("div");
    card.classList.add("fundo");
    card.classList.add(`bloco-${day.toLowerCase()}`);

    const title = document.createElement("h2");
    title.classList.add("title_day");
    title.textContent = day;
    card.appendChild(title);

    const checkboxContainer = document.createElement("div");
    checkboxContainer.classList.add("checkbox");

    nome.forEach(item => {
        const checkLabel = document.createElement("div");
        checkLabel.classList.add("check_label");

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.classList.add("btn-ch");
        checkbox.classList.add(`botao-${item.toLowerCase().replaceAll('ç', 'c').replaceAll('é', 'e')}`);

        const label = document.createElement("label");
        label.textContent = item;

        checkLabel.appendChild(checkbox);
        checkLabel.appendChild(label);
        checkboxContainer.appendChild(checkLabel);
    });

    card.appendChild(checkboxContainer);

    const todosButton = document.createElement("h2");
    todosButton.classList.add("title_day");
    todosButton.id = "todos";
    todosButton.textContent = "Marcar todos";

    todosButton.addEventListener("click", function () {
        const checkboxes = card.querySelectorAll(".checkbox input[type='checkbox']");
        const allChecked = Array.from(checkboxes).every((checkbox) => checkbox.checked);

        checkboxes.forEach((checkbox) => {
            checkbox.checked = !allChecked;
        });

        this.textContent = allChecked ? "Marcar todos" : "Desmarcar todos";
    });

    card.appendChild(todosButton);
    container.appendChild(card);
});

document.getElementById("close-modal").addEventListener("click", function () {
    const modalElement = document.querySelector("#modal-cardapio-container");
    modalElement.style.display = "none";
    
});

document.getElementById("ver-cardapio-btn").addEventListener("click", function () {
    const modalElement = document.querySelector("#modal-cardapio-container");
    modalElement.style.display = "flex";
    
});

function diasDaSemana() {
    let dicionarioDias = {};

    let data = new Date();
    
    const diaDaSemana = data.getDay();
    data.setDate(data.getDate() - diaDaSemana);
    
    for (let i = 0; i < 7; i++) {
        let diaFormatado = `${data.getFullYear()}-${String(data.getMonth() + 1).padStart(2, '0')}-${String(data.getDate()).padStart(2, '0')}`;
        dicionarioDias[days[i].toLowerCase()] = diaFormatado;
        
        data.setDate(data.getDate() + 1);
    }

    return dicionarioDias;
}

document.querySelector('#submit').addEventListener('click', async () => {
    let interesses = [];

    for (let dia of days) {
        let bloco = document.querySelector(`.bloco-${dia.toLowerCase()}`);

        let checkboxes = bloco.querySelectorAll('input[type=checkbox]');

        for (let checkbox of checkboxes) {
            if (checkbox.checked) {
                interesses.push({
                    dia: diasDaSemana()[dia.toLowerCase()],
                    tipo: Array.from(checkbox.classList).filter(e => e.substring(0, 6) == 'botao-')[0].substring(6)
                });
            }
        }
    }

    let resposta = await fetch('/api/interesse', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'interesses': interesses
        })
    });

    let respostaJSON = await resposta.json();

    if (!respostaJSON.ok) {
        Swal.fire({
            icon: "error",
            title: "Erro",
            text: respostaJSON.mensagem
        });

        return;
    }

    Swal.fire({
        icon: "success",
        title: "Refeições salvas",
        text: "Suas refeições foram enviadas e salvas com sucesso."
    });
});

async function atualizarTabela() {
    let tipo = document.querySelector('.tipos-select-modal').value

    let resposta = await fetch(`/api/cardapio/${obterData()}/${tipo}`);

    let respostaJSON = await resposta.json();

    if (!respostaJSON.ok) {
        Swal.fire({
            icon: "error",
            title: "Erro",
            text: respostaJSON.mensagem
        });
        return;
    }

    let cardapio = respostaJSON.resultado;

    let tbody = document.querySelector('tbody');

    tbody.innerHTML = '';

    let dias = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

    dias = dias.reverse();

    for (let dia of Object.keys(cardapio).sort()) {
        let tr = document.createElement('tr');

        let th = document.createElement('th');
        th.textContent = dias.pop();

        let td = document.createElement('td');
        td.textContent = cardapio[dia].toString().replaceAll(',', ', ');

        tr.appendChild(th);
        tr.appendChild(td);

        tbody.appendChild(tr);
    }
}

document.querySelector('#ver-cardapio-btn').addEventListener('click', () => {
    atualizarTabela();
});

document.querySelector('.tipos-select-modal').addEventListener('change', () => {
    atualizarTabela();
});