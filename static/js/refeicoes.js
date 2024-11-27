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
    let interesses = {};

    for (let dia of days) {
        let interessesDia = {};

        let bloco = document.querySelector(`.bloco-${dia.toLowerCase()}`);

        let checkboxes = bloco.querySelectorAll('input[type=checkbox]');

        for (let checkbox of checkboxes) {
            interessesDia[Array.from(checkbox.classList).filter(e => e.substring(0, 6) == 'botao-')[0].substring(6)] = checkbox.checked;
        }

        interesses[diasDaSemana()[dia.toLowerCase()]] = interessesDia;
    }
    
    let erro = false;

    for (let interesse of Object.keys(interesses)) {

        for (let tipo of Object.keys(interesses[interesse])) {
            console.log(interesses[interesse][tipo]);

            let resposta = await fetch('/api/interesse', {
                method: interesses[interesse][tipo] ? 'POST' : 'DELETE',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'dia': interesse,
                    'tipo': tipo
                })
            });

            if (resposta.status == 404) {
                continue;
            }

            let respostaJSON = await resposta.json();

            if (!respostaJSON.ok) {
                erro = true;
            } 
        }    
    }

    Swal.fire({
        icon: erro ? "error" : "success",
        title: erro ? "Erro" : "Refeições salvas",
        text: erro ? "Ocorreu um erro durante o envio das refeições." : "Suas refeições foram enviadas e salvas com sucesso."
    });
});