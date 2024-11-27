document.querySelector('#botao-login').addEventListener('click', async () => {
    let matricula = document.getElementsByName('matricula')[0].value; 
    let senha = document.getElementsByName('senha')[0].value; 

    if (matricula == '' || senha == '') {
        Swal.fire({
            icon: "error",
            title: "Campos vazios",
            text: "Preencha os campos corretamente."
        });

        return;
    }

    let resposta = await fetch('/login', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'matricula': matricula,
            'senha': senha
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

    window.location.href = respostaJSON.administrador ? '/admin' : '/refeicoes';
});