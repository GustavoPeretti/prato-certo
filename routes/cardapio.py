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

    print(resultado)

    if not resultado:
        return jsonify({'ok': False, 'mensagem': 'Nenhum recurso foi encontrado.'}), 404
    
    return jsonify({'ok': True, 'resultado': resultado}), 200
