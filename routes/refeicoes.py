from flask import Blueprint, render_template

refeicoes = Blueprint('refeicoes', __name__)

@refeicoes.route('/')
def refeicoes_handler():
    return render_template('refeicoes.html')
