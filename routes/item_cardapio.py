from flask import Blueprint, jsonify, session, request
from ..database.db import db

item_cardapio = Blueprint('item_cardapio', __name__)

@item_cardapio.route('/')
def buscar_itens():
    resultado = db.query('SELECT * FROM itens_cardapio;')

    if not resultado:
        return jsonify({'ok': False, 'mensagem': 'Nenhum recurso foi encontrado.'}), 404

    return jsonify({'ok': True, 'resultado': resultado}), 200

@item_cardapio.route('/', methods=['POST'])
def cadastrar_item():
    if 'usuario' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401

    dados = request.json

    if 'nome' not in dados:
        return jsonify({'ok': False, 'mensagem': 'Parâmetro obrigatório não especificado.'}), 400 

    itens_cadastrados_com_mesmo_nome = db.query('SELECT * FROM itens_cardapio WHERE nome = %s;', dados['nome'])

    if itens_cadastrados_com_mesmo_nome:
        return jsonify({'ok': False, 'mensagem': 'Conflito com recurso já existente.'}), 409

    try:
        db.query('INSERT INTO itens_cardapio VALUES (%s);', dados['nome'])
    except:
        return jsonify({'ok': False, 'mensagem': 'Não foi possível processar os dados.'}), 400
    
    return jsonify({'ok': True, 'mensagem': 'Recurso criado.'}), 201

@item_cardapio.route('/<nome>', methods=['DELETE'])
def deletar_item(nome):
    if 'usuario' not in session:
        return jsonify({'ok': False, 'mensagem': 'Não autorizado.'}), 401
    
    try:
        item = db.query('SELECT * FROM itens_cardapio WHERE nome = %s;', nome)
    except:
        return jsonify({'ok': False, 'mensagem': 'Não foi possível processar os dados.'}), 400
    
    if not item:
        return jsonify({'status': False, 'mensagem': 'Recurso não foi encontrado.'}), 404
    
    try:
        db.query('DELETE FROM itens_cardapio WHERE nome = %s;', nome)
    except:
        return jsonify({'status': False, 'mensagem': 'Não foi possível processar os dados.'}), 400

    return jsonify({'status': True, 'mensagem': 'Recurso deletado.'}), 200
