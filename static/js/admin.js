function obterData() {
    let data = new Date();

    let ano = data.getFullYear();
    let mes = String(data.getMonth() + 1).padStart(2, '0');
    let dia = String(data.getDate()).padStart(2, '0');

    return `${ano}-${mes}-${dia}`;
}

document.querySelector('button').addEventListener('click', async () => {
    let tipo = 'janta';

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

    console.log(respostaJSON.resultado);
});