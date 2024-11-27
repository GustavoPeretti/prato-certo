function obterData() {
    let data = new Date();

    let ano = data.getFullYear();
    let mes = String(data.getMonth() + 1).padStart(2, '0');
    let dia = String(data.getDate()).padStart(2, '0');

    return `${ano}-${mes}-${dia}`;
}

document.addEventListener('DOMContentLoaded', async () => {
    let tipo = document.querySelector('.tipos-select').value;

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

    let tbody = document.querySelector('#cardapio-home');

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
});

document.querySelector('.tipos-select').addEventListener('change', async () => {
    let tipo = document.querySelector('.tipos-select').value;

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

    let tbody = document.querySelector('#cardapio-home');

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
});