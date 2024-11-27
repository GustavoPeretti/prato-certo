// function obterData() {
//     let data = new Date();

//     let ano = data.getFullYear();
//     let mes = String(data.getMonth() + 1).padStart(2, '0');
//     let dia = String(data.getDate()).padStart(2, '0');

//     return `${ano}-${mes}-${dia}`;
// }

// document.querySelector('button').addEventListener('click', async () => {
//     let tipo = 'janta';

//     let resposta = await fetch(`/api/interesse/${obterData()}/${tipo}`);

//     let respostaJSON = await resposta.json();

//     if (!respostaJSON.ok) {
//         Swal.fire({
//             icon: "error",
//             title: "Erro",
//             text: respostaJSON.mensagem
//         });
        
//         return;
//     }

//     console.log(respostaJSON.resultado);
// });

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


const tipoSelect = document.getElementById('tipo-select');
const tipoRefeicao = document.getElementById('tipo-refeicao');
tipoSelect.addEventListener('change', () => {
    tipoRefeicao.textContent = tipoSelect.options[tipoSelect.selectedIndex].text;
});


