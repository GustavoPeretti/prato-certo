from flask import Blueprint, jsonify, session, request
import datetime
from ..database.db import db

cardapio = Blueprint('cardapio', __name__)

@cardapio.route('/<data>')
def buscar_cardapios_por_data(data):
    resultado = db.query('SELECT * FROM itens_cardapios_dias WHERE dia = %s;', data)

    if not resultado:
        return jsonify({'ok': False, 'mensagem': 'Nenhum recurso foi encontrado.'}), 404
    
    itens = {}

    for tipo in ['cafe', 'almoco', 'lanche', 'janta']:
        if tipo not in itens:
            itens[tipo] = []
        for item in resultado:
            if item['tipo'] == tipo:
                itens[tipo].append(item['item'])

    return jsonify({'ok': True, 'resultado': itens}), 200

@cardapio.route('/<data>/<tipo>')
def buscar_cardapios_por_tipo(data, tipo):
    try:
        data = datetime.datetime.strptime(data, '%Y-%m-%d').date()

        inicio_semana = data - datetime.timedelta(days=(data.weekday() + 1) % 7)

        dias = [inicio_semana + datetime.timedelta(days=i) for i in range(7)]

        dias = [dia.strftime('%Y-%m-%d') for dia in dias]
    except:
        return jsonify({'ok': False, 'mensagem': 'Erro ao processar a data.'}), 400

    if tipo not in ['cafe', 'almoco', 'lanche', 'janta']:
        return jsonify({'ok': False, 'mensagem': 'Tipo inválido.'}), 400
    
    resultado = db.query(
        'SELECT * FROM itens_cardapios_dias ' +
        'WHERE tipo = %s ' +
        'AND (dia = %s ' +
        'OR dia = %s ' +
        'OR dia = %s ' +
        'OR dia = %s ' +
        'OR dia = %s ' +
        'OR dia = %s ' +
        'OR dia = %s);',
        tipo,
        *dias
    )

    if not resultado:
        return jsonify({'ok': False, 'mensagem': 'Nenhum recurso foi encontrado.'}), 404
    
    cardapio_semana = {}
    
    for dia in dias:
        itens_dia = []
        for item in resultado:
            if item['dia'].strftime('%Y-%m-%d') == dia:
                itens_dia.append(item['item'])
        cardapio_semana[dia] = itens_dia
    
    return jsonify({'ok': True, 'resultado': cardapio_semana}), 200

@cardapio.route('/', methods=['POST'])
def cadastrar_cardapio():
    if 'usuario' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    if not session['usuario']['administrador']:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401

    dados = request.json

    parametros = {
        'dia': lambda x: isinstance(x, str),
        'tipo': lambda x: isinstance(x, str) and x in ['cafe', 'almoco', 'lanche', 'janta'],
    }

    if 'itens' not in dados:
        return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não informado.'}), 400
    
    if not isinstance(dados['itens'], list):
        return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400

    itens = dados['itens']

    for item_interesse in itens:
        for parametro in parametros:
            if parametro not in item_interesse:
                return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não informado.'}), 400
            argumento = item_interesse[parametro]
            if not parametros[parametro](argumento):
                return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400
            
    try:
        db.query('DELETE FROM itens_cardapios_dias WHERE dia = %s;', itens[0]['dia'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Houve um erro ao tentar cadastrar os itens.'}), 400
    
    try:
        argumentos = []

        for item in itens:
            argumentos.append(item['dia'])
            argumentos.append(item['tipo'])
            argumentos.append(item['item'])

        db.query(
            'INSERT INTO itens_cardapios_dias VALUES ' + ', '.join(['(%s, %s, %s)'] * len(itens)) + ';',
            *argumentos
        )
    except:
        return jsonify({'ok': False, 'mensagem': 'Houve um erro ao tentar cadastrar os itens.'}), 400

    return jsonify({'ok': True, 'mensagem': 'Itens cadastrados.'}), 200
