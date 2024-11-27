from flask import Blueprint
from .cardapio import cardapio
from .interesse import interesse

api = Blueprint('api', __name__)

api.register_blueprint(cardapio, url_prefix='/cardapio')
api.register_blueprint(interesse, url_prefix='/interesse')
