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

@interesse.route('/', methods=['POST'])
def cadastrar_interesse():
    dados = request.json

    parametros = {
        'dia': lambda x: isinstance(x, str),
        'tipo': lambda x: isinstance(x, str) and x in ['cafe', 'almoco', 'lanche', 'janta'],
        'usuario': lambda x: isinstance(x, str)
    }

    for parametro in parametros:
        if parametro not in dados:
            return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não informado.'}), 400
        argumento = dados[parametro]
        if not parametros[parametro](argumento):
            return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400
    
    try:
        interesse = db.query('SELECT * FROM interesses WHERE dia = %s AND tipo = %s AND usuario = %s;', dados['dia'], dados['tipo'], dados['usuario'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Erro ao tentar validar o item.'}), 400
    
    if interesse:
        return jsonify({'ok': False, 'mensagem': 'Interesse já declarado.'}), 400
    
    try:
        db.query('INSERT INTO interesses VALUES (%s, %s, %s);', dados['dia'], dados['tipo'], dados['usuario'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Erro ao tentar cadastrar o interesse.'}), 400
    
    return jsonify({'ok': True, 'mensagem': 'Interesse cadastrado.'}), 200

@interesse.route('/', methods=['DELETE'])
def deletar_interesse():
    dados = request.json

    parametros = {
        'dia': lambda x: isinstance(x, str),
        'tipo': lambda x: isinstance(x, str) and x in ['cafe', 'almoco', 'lanche', 'janta'],
        'usuario': lambda x: isinstance(x, str)
    }

    for parametro in parametros:
        if parametro not in dados:
            return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não informado.'}), 400
        argumento = dados[parametro]
        if not parametros[parametro](argumento):
            return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400
    
    try:
        item = db.query('SELECT * FROM interesses WHERE dia = %s AND tipo = %s AND usuario = %s;', dados['dia'], dados['tipo'], dados['usuario'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Erro ao tentar validar o interesse.'}), 400
    
    if not item:
        return jsonify({'ok': False, 'mensagem': 'Interesse não existente.'}), 404
    
    try:
        db.query('DELETE FROM interesses WHERE dia = %s AND tipo = %s AND usuario = %s;', dados['dia'], dados['tipo'], dados['usuario'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Houve um erro ao tentar deletar o interesse.'}), 400

    return jsonify({'ok': True, 'mensagem': 'Interesse deletado.'}), 200


