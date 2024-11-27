from flask import Blueprint, request, jsonify, session, render_template
from ..database.db import db

login = Blueprint('login', __name__)

@login.route('/', methods=['GET', 'POST'])
def login_handler():
    if request.method == 'POST':
        dados = request.json

        if ('matricula' not in dados) or ('senha' not in dados):
            return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não especificado.'}), 400 

        resultado = db.query('SELECT * FROM usuarios WHERE matricula = %s;', dados['matricula'])

        if not resultado:
            return jsonify({'ok': False, 'mensagem': 'Matrícula não cadastrada.'}), 400
        
        resultado = db.query('SELECT * FROM usuarios WHERE matricula = %s AND senha = SHA2(%s, 256);', dados['matricula'], dados['senha'])

        if not resultado:
            return jsonify({'ok': False, 'mensagem': 'Senha incorreta.'}), 401
        
        session['usuario'] = {
            'matricula': resultado[0]['matricula'],
            'nome': resultado[0]['nome'],
            'admininstrador': resultado[0]['administrador']
        }
        
        return jsonify({'ok': True, 'mensagem': 'Usuário autenticado.'}), 200

    return render_template('login.html')