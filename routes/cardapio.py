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
