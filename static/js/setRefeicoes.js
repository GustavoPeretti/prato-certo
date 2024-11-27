const days = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"];
const nome = ['Café', 'Almoço', 'Lanche', 'Janta'];

const container = document.querySelector(".controll_days");

days.forEach(day => {
    const card = document.createElement("div");
    card.classList.add("fundo");

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
