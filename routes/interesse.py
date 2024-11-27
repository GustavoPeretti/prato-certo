from flask import Blueprint, jsonify, session, request
from ..database.db import db

interesse = Blueprint('interesse', __name__)

@interesse.route('/<data>/<tipo>')
def buscar_numero_refeicoes(data, tipo):
    if 'usuario' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    if not session['usuario']['administrador']:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    resultado = db.query('SELECT COUNT(*) as interesses FROM interesses WHERE dia = %s AND tipo = %s;', data, tipo)

    if not resultado:
        return jsonify({'ok': False, 'mensagem': 'Nenhum recurso foi encontrado.'}), 404

    return jsonify({'ok': True, 'resultado': resultado[0]['interesses']}), 200

@interesse.route('/')
def buscar_interesses():
    if 'usuario' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    try:
        resultado = db.query('SELECT * FROM interesses WHERE usuario = %s;', session['usuario']['matricula'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Houve um erro ao tentar verificar os interesses.'}), 400
    
    print(resultado)

    interesses = {}

    for interesse in resultado:
        if interesse['dia'].strftime('%Y-%m-%d') not in interesses:
            interesses[interesse['dia'].strftime('%Y-%m-%d')] = []
        print(interesse['tipo'])
        interesses[interesse['dia'].strftime('%Y-%m-%d')].append(interesse['tipo'])

    return jsonify({'ok': True, 'mensagem': 'Interesses obtidos.', 'resultado': interesses}), 200

@interesse.route('/', methods=['POST'])
def cadastrar_interesse():
    if 'usuario' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    dados = request.json

    parametros = {
        'dia': lambda x: isinstance(x, str),
        'tipo': lambda x: isinstance(x, str) and x in ['cafe', 'almoco', 'lanche', 'janta']
    }
    
    if 'interesses' not in dados:
        return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não informado.'}), 400
    
    if not isinstance(dados['interesses'], list):
        return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400

    interesses = dados['interesses']

    for item_interesse in interesses:
        for parametro in parametros:
            if parametro not in item_interesse:
                return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não informado.'}), 400
            argumento = item_interesse[parametro]
            if not parametros[parametro](argumento):
                return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400

    for item_interesse in interesses:
        try:
            db.query('INSERT INTO interesses VALUES (%s, %s, %s);', item_interesse['dia'], item_interesse['tipo'], session['usuario']['matricula'])
        except:
            pass

    try:
        db.query('DELETE FROM interesses WHERE usuario = %s;', session['usuario']['matricula'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Houve um erro ao tentar cadastrar os interesses.'}), 400

    try:
        argumentos = []

        for item_interesse in interesses:
            argumentos.append(item_interesse['dia'])
            argumentos.append(item_interesse['tipo'])
            argumentos.append(session['usuario']['matricula'])

        db.query(
            'INSERT INTO interesses VALUES ' + ', '.join(['(%s, %s, %s)'] * len(interesses)) + ';',
            *argumentos
        )
    except:
        return jsonify({'ok': False, 'mensagem': 'Houve um erro ao tentar cadastrar os interesses.'}), 400

    return jsonify({'ok': True, 'mensagem': 'Interesses cadastrados.'}), 200
