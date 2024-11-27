from flask import Blueprint
from .item_cardapio import item_cardapio
from .cardapio import cardapio

api = Blueprint('api', __name__)

api.register_blueprint(item_cardapio, url_prefix='/item-cardapio')
api.register_blueprint(cardapio, url_prefix='/cardapio')
