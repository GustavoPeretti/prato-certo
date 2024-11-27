from flask import Blueprint, render_template, session, redirect, url_for

admin = Blueprint('admin', __name__)

@admin.route('/')
def admin_handler():
    if 'usuario' not in session:
        return redirect(url_for('login.login_handler'))
    
    if not session['usuario']['administrador']:
        return redirect(url_for('login.login_handler'))
    
    return render_template('admin.html')