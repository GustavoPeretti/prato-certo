from flask import Blueprint
from .item_cardapio import item_cardapio

api = Blueprint('api', __name__)

api.register_blueprint(item_cardapio, url_prefix = 'item-cardapio')
