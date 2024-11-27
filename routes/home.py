from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')
def home_handler():
    return render_template('home.html')