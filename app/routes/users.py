from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User

bp = Blueprint('users', __name__)

@bp.route('/users')
@login_required
def index():
    if current_user.role != 'admin':
        flash('No tienes permisos para acceder a la gestión de usuarios.', 'danger')
        return redirect(url_for('main.index'))
    
    users = User().get_all()
    return render_template('users/index.html', users=users)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.role != 'admin':
        flash('No tienes permisos para acceder a esta página')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        user_model = User()
        if user_model.get_by_username(username):
            flash('El nombre de usuario ya está en uso')
            return redirect(url_for('users.add'))
        
        if user_model.get_by_email(email):
            flash('El email ya está registrado')
            return redirect(url_for('users.add'))
        
        user_model.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        
        flash('Usuario creado exitosamente')
        return redirect(url_for('users.index'))
    
    return render_template('users/add.html')

@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.role != 'admin':
        flash('No tienes permisos para acceder a esta página')
        return redirect(url_for('main.index'))
    
    user_model = User()
    user = user_model.get_by_id(id)
    if not user:
        flash('Usuario no encontrado')
        return redirect(url_for('users.index'))
    
    if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        
        # Verificar si el email ya está en uso por otro usuario
        existing_user = user_model.get_by_email(email)
        if existing_user and existing_user['id'] != id:
            flash('El email ya está registrado')
            return redirect(url_for('users.edit', id=id))
        
        # Actualizar usuario
        user_model.update(id, {
            'email': email,
            'role': role
        })
        
        # Si se proporcionó una nueva contraseña, actualizarla
        if request.form.get('password'):
            user_model.update(id, {
                'password_hash': user_model.generate_password_hash(request.form['password'])
            })
        
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('users.index'))
    
    return render_template('users/edit.html', user=user)

@bp.route('/users/delete/<int:id>')
@login_required
def delete(id):
    if current_user.role != 'admin':
        flash('No tienes permisos para acceder a esta página')
        return redirect(url_for('main.index'))
    
    if id == current_user.id:
        flash('No puedes eliminar tu propio usuario')
        return redirect(url_for('users.index'))
    
    user_model = User()
    if user_model.delete(id):
        flash('Usuario eliminado exitosamente')
    else:
        flash('Error al eliminar el usuario')
    return redirect(url_for('users.index')) 