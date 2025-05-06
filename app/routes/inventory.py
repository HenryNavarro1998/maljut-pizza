from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.inventory import Product
from datetime import datetime

bp = Blueprint('inventory', __name__)

@bp.route('/inventory')
@login_required
def index():
    products = Product().get_all()
    # Convertir las fechas de string a datetime
    for product in products:
        if 'updated_at' in product and product['updated_at']:
            try:
                product['updated_at'] = datetime.fromisoformat(product['updated_at'])
            except (ValueError, TypeError):
                product['updated_at'] = datetime.now()
    return render_template('inventory/index.html', products=products)

@bp.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit')
        min_quantity = request.form.get('min_quantity')
        
        # Validar que todos los campos requeridos estén presentes
        if not all([name, description, quantity, unit, min_quantity]):
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('inventory.add'))
        
        try:
            # Convertir a float y validar que sean números positivos
            quantity = float(quantity)
            min_quantity = float(min_quantity)
            if quantity < 0 or min_quantity < 0:
                raise ValueError("Las cantidades deben ser positivas")
            
            # Crear el producto
            product = Product().create_product(
                name=name,
                description=description,
                quantity=quantity,
                unit=unit,
                min_quantity=min_quantity
            )
            
            flash('Producto agregado exitosamente', 'success')
            return redirect(url_for('inventory.index'))
            
        except ValueError as e:
            flash(f'Error en los datos: {str(e)}', 'error')
            return redirect(url_for('inventory.add'))
    
    return render_template('inventory/add.html')

@bp.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product_model = Product()
    product = product_model.get_by_id(id)
    
    if not product:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('inventory.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit')
        min_quantity = request.form.get('min_quantity')
        
        # Validar que todos los campos requeridos estén presentes
        if not all([name, description, quantity, unit, min_quantity]):
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('inventory.edit', id=id))
        
        try:
            # Convertir a float y validar que sean números positivos
            quantity = float(quantity)
            min_quantity = float(min_quantity)
            if quantity < 0 or min_quantity < 0:
                raise ValueError("Las cantidades deben ser positivas")
            
            # Actualizar el producto
            product['name'] = name
            product['description'] = description
            product['quantity'] = quantity
            product['unit'] = unit
            product['min_quantity'] = min_quantity
            product['updated_at'] = datetime.utcnow().isoformat()
            
            if product_model.update(id, product):
                flash('Producto actualizado exitosamente', 'success')
            else:
                flash('Error al actualizar el producto', 'error')
            
            return redirect(url_for('inventory.index'))
            
        except ValueError as e:
            flash(f'Error en los datos: {str(e)}', 'error')
            return redirect(url_for('inventory.edit', id=id))
    
    return render_template('inventory/edit.html', product=product)

@bp.route('/inventory/delete/<int:id>')
@login_required
def delete(id):
    if Product().delete(id):
        flash('Producto eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el producto', 'error')
    return redirect(url_for('inventory.index'))

@bp.route('/inventory/update_stock/<int:id>', methods=['POST'])
@login_required
def update_stock(id):
    try:
        quantity = float(request.form.get('quantity', 0))
        if quantity < 0:
            raise ValueError("La cantidad debe ser positiva")
        
        if Product().update_stock(id, quantity):
            flash('Stock actualizado exitosamente', 'success')
        else:
            flash('Error al actualizar el stock', 'error')
    except ValueError as e:
        flash(f'Error en los datos: {str(e)}', 'error')
    
    return redirect(url_for('inventory.index')) 