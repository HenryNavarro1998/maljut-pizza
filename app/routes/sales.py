from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.inventory import Product, Recipe
from app.models.sales import Sale
from datetime import datetime, timedelta

bp = Blueprint('sales', __name__)

@bp.route('/sales')
@login_required
def index():
    try:
        recipes = Recipe().get_all()
        if not recipes:
            flash('No hay recetas disponibles para vender', 'info')
            return render_template('sales/index.html', recipes=[])
        
        # Convertir las fechas de string a datetime y validar datos
        valid_recipes = []
        for recipe in recipes:
            if not isinstance(recipe, dict):
                continue
                
            # Asegurar que la receta tiene los campos necesarios
            if not all(key in recipe for key in ['id', 'name', 'description']):
                continue
                
            # Convertir fecha de actualización
            if 'updated_at' in recipe and recipe['updated_at']:
                try:
                    recipe['updated_at'] = datetime.fromisoformat(recipe['updated_at'])
                except (ValueError, TypeError):
                    recipe['updated_at'] = datetime.now()
            else:
                recipe['updated_at'] = datetime.now()
            
            # Asegurar que ingredients es una lista y tiene toda la información necesaria
            if 'ingredients' not in recipe:
                recipe['ingredients'] = []
            elif not isinstance(recipe['ingredients'], list):
                recipe['ingredients'] = []
            
            # Actualizar información de ingredientes
            updated_ingredients = []
            for ingredient in recipe['ingredients']:
                if not isinstance(ingredient, dict):
                    continue
                    
                product_id = ingredient.get('product_id')
                if not product_id:
                    continue
                    
                product = Product().get_by_id(product_id)
                if not product:
                    continue
                    
                updated_ingredient = {
                    'product_id': product_id,
                    'product_name': product['name'],
                    'quantity': ingredient.get('quantity', 0),
                    'unit': product['unit']
                }
                updated_ingredients.append(updated_ingredient)
            
            recipe['ingredients'] = updated_ingredients
            valid_recipes.append(recipe)
        
        return render_template('sales/index.html', recipes=valid_recipes)
        
    except Exception as e:
        flash(f'Error al cargar las recetas: {str(e)}', 'error')
        return render_template('sales/index.html', recipes=[])

@bp.route('/sales/process/<int:recipe_id>', methods=['POST'])
@login_required
def process_sale(recipe_id):
    recipe = Recipe().get_by_id(recipe_id)
    if not recipe:
        flash('Receta no encontrada', 'error')
        return redirect(url_for('sales.index'))
    
    try:
        quantity = float(request.form.get('quantity', 0))
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        # Verificar stock de ingredientes
        insufficient_products = []
        total_ingredients = []
        for ingredient in recipe.get('ingredients', []):
            product = Product().get_by_id(ingredient['product_id'])
            if not product:
                continue
            
            required_quantity = ingredient['quantity'] * quantity
            total_ingredients.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'quantity_used': required_quantity,
                'unit': product['unit']
            })
            
            if product['quantity'] < required_quantity:
                insufficient_products.append({
                    'product': product,
                    'required': required_quantity,
                    'available': product['quantity'],
                    'shortage': required_quantity - product['quantity']
                })
        
        if insufficient_products:
            return render_template('sales/insufficient_stock.html',
                                recipe=recipe,
                                quantity=quantity,
                                insufficient_products=insufficient_products)
        
        # Procesar la venta y actualizar el inventario
        for ingredient in recipe.get('ingredients', []):
            product = Product().get_by_id(ingredient['product_id'])
            if product:
                new_quantity = product['quantity'] - (ingredient['quantity'] * quantity)
                # Mantener todos los campos del producto al actualizar
                product_data = {
                    'name': product['name'],
                    'description': product['description'],
                    'quantity': new_quantity,
                    'unit': product['unit'],
                    'min_quantity': product['min_quantity'],
                    'updated_at': datetime.utcnow().isoformat()
                }
                Product().update(product['id'], product_data)
        
        # Registrar la venta en el historial
        Sale().create_sale(
            recipe_id=recipe['id'],
            recipe_name=recipe['name'],
            quantity=quantity,
            total_ingredients=total_ingredients
        )
        
        flash('Venta procesada exitosamente', 'success')
        return redirect(url_for('sales.index'))
        
    except ValueError as e:
        flash(f'Error en los datos: {str(e)}', 'error')
        return redirect(url_for('sales.index'))

@bp.route('/sales/history')
@login_required
def history():
    # Obtener el rango de fechas del query string
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    try:
        sales_model = Sale()
        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
                sales = sales_model.get_sales_by_date_range(start_date, end_date)
                total_sales = sales_model.get_total_sales(start_date, end_date)
            except ValueError:
                flash('Formato de fecha inválido. Mostrando todas las ventas.', 'warning')
                sales = sales_model.get_all()
                total_sales = sales_model.get_total_sales()
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
        else:
            sales = sales_model.get_all()
            total_sales = sales_model.get_total_sales()
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)

        # Convertir las fechas de string a datetime para la vista
        for sale in sales:
            if 'created_at' in sale and sale['created_at']:
                try:
                    sale['created_at'] = datetime.fromisoformat(sale['created_at'])
                except (ValueError, TypeError):
                    sale['created_at'] = datetime.now()
        
        return render_template('sales/history.html',
                             sales=sales,
                             total_sales=total_sales,
                             start_date=start_date.strftime('%Y-%m-%d'),
                             end_date=end_date.strftime('%Y-%m-%d'))
                             
    except Exception as e:
        flash(f'Error al cargar el historial: {str(e)}', 'error')
        return redirect(url_for('sales.index')) 