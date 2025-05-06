from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from werkzeug.urls import url_parse

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_model = User()
        user_data = user_model.get_by_username(username)
        if user_data is None or not user_model.check_password(user_data, password):
            flash('Usuario o contraseña inválidos')
            return redirect(url_for('auth.login'))
        # Crear instancia User para Flask-Login
        user = User()
        user.id = user_data['id']
        user.username = user_data['username']
        user.email = user_data.get('email')
        user.role = user_data.get('role')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user_model = User()
        if user_model.get_by_username(username):
            flash('El nombre de usuario ya está en uso')
            return redirect(url_for('auth.register'))
        
        if user_model.get_by_email(email):
            flash('El email ya está registrado')
            return redirect(url_for('auth.register'))
        
        user = user_model.create_user(username=username, email=email, password=password)
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html') 