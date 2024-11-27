from flask import Flask
from .routes.home import home
from .routes.login import login
from .routes.refeicoes import refeicoes
from .routes.admin import admin
from .routes.api import api 
import os

app = Flask(__name__)

app.register_blueprint(home)
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(refeicoes, url_prefix='/refeicoes')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')

app.secret_key = os.environ.get('SECRET_KEY')
