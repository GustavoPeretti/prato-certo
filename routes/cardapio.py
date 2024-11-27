from flask import Blueprint, jsonify, session, request
import datetime
from ..database.db import db

cardapio = Blueprint('cardapio', __name__)

@cardapio.route('/<data>/<tipo>')
def buscar_cardapios(data, tipo):
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
        'SELECT * FROM itens_cardapios_dias' +
        ' WHERE tipo = %s ' +
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
    dados = request.json

    parametros = {
        'dia': lambda x: isinstance(x, str),
        'tipo': lambda x: isinstance(x, str) and x in ['cafe', 'almoco', 'lanche', 'janta'],
        'itens': lambda x: isinstance(x, list) and x
    }

    for parametro in parametros:
        if parametro not in dados:
            return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não informado.'}), 400
        argumento = dados[parametro]
        if not parametros[parametro](argumento):
            return jsonify({'ok': False, 'mensagem': 'Argumento em formato inválido.'}), 400
    
    lista_itens = dados['itens']

    for item in lista_itens:
        try:
            db.query('INSERT INTO itens_cardapios_dias VALUES (%s, %s, %s);',
                dados['dia'],
                dados['tipo'],
                item
            )
        except:
            return jsonify({'ok': False, 'mensagem': 'Erro ao tentar cadastrar os itens.'}), 400
    
    return jsonify({'ok': True, 'mensagem': 'Itens cadastrados.'}), 200

@cardapio.route('/', methods=['DELETE'])
def deletar_cardapio():
    dados = request.json

    parametros = {
        'dia': lambda x: isinstance(x, str),
        'tipo': lambda x: isinstance(x, str) and x in ['cafe', 'almoco', 'lanche', 'janta'],
        'item': lambda x: isinstance(x, str)
    }

    
