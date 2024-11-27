function obterData() {
    let data = new Date();

    let ano = data.getFullYear();
    let mes = String(data.getMonth() + 1).padStart(2, '0');
    let dia = String(data.getDate()).padStart(2, '0');

    return `${ano}-${mes}-${dia}`;
}

let traducaoTipo = {
    'cafe': 'cafés',
    'almoco': 'almoços',
    'lanche': 'lanches',
    'janta': 'jantas'
}

async function atualizarRefeicoes() {
    let tipo = document.querySelector('#tipo-select').value;

    let resposta = await fetch(`/api/interesse/${obterData()}/${tipo}`);

    let respostaJSON = await resposta.json();

    if (!respostaJSON.ok) {
        Swal.fire({
            icon: "error",
            title: "Erro",
            text: respostaJSON.mensagem
        });
        
        return;
    }

    document.querySelector('#qtd-refeicao').innerHTML = `${respostaJSON.resultado}<span id="tipo-refeicao"> ${traducaoTipo[tipo]}</span>`;
}

atualizarRefeicoes()

setInterval(atualizarRefeicoes, 10000);

document.querySelector('#tipo-select').addEventListener('click', atualizarRefeicoes)

document.getElementById("add-cardapio-btn").addEventListener("click", function () {
    const mainElement = document.getElementById("main-admin");
    const formElement = document.getElementById("container-add-cardapio");

    mainElement.style.display = "none"
    formElement.style.display = "flex";
});

document.getElementById("btn-close-cardapio").addEventListener("click", function () {
    const mainElement = document.getElementById("main-admin");
    const formElement = document.getElementById("container-add-cardapio");

    mainElement.style.display = "flex"
    formElement.style.display = "none";
});

document.getElementById("close-modal").addEventListener("click", function () {
    const modalElement = document.querySelector("#modal-cardapio-container");
    modalElement.style.display = "none";
    
});

document.getElementById("ver-cardapio-btn").addEventListener("click", function () {
    const modalElement = document.querySelector("#modal-cardapio-container");
    modalElement.style.display = "flex";
    
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

function adicionarItem(tipo, nome) {
    let item = document.createElement('div');
    item.classList.add('item-refeicao-acordeao');

    let span = document.createElement('span');
    span.textContent = nome;

    let icone = document.createElement('span');
    icone.classList.add('material-symbols-outlined')
    icone.textContent = 'delete';
    icone.addEventListener('click', () => {
        item.remove();
    })

    item.appendChild(span);
    item.appendChild(icone);

    let acordeao = document.querySelector(`.acordeao-${tipo}`);

    acordeao.querySelector('.accordion-body').insertBefore(item, acordeao.querySelector('.botao-cadastrar'));
}

document.querySelectorAll('.accordion-body input').forEach(e => {
    e.addEventListener("keyup", ({key}) => {
        if (key === "Enter") {
            let tipo = Array.from(e.parentElement.parentElement.parentElement.parentElement.classList).filter(e => e.substring(0, 9) == 'acordeao-')[0].substring(9);
            adicionarItem(tipo, e.value);
            e.value = '';
        }
    });
});

document.querySelectorAll('.accordion-body button').forEach(e => {
    e.addEventListener("click", () => {
        let tipo = Array.from(e.parentElement.parentElement.parentElement.parentElement.classList).filter(e => e.substring(0, 9) == 'acordeao-')[0].substring(9);
        adicionarItem(tipo, e.previousElementSibling.value);
        e.value = '';
    });
});

