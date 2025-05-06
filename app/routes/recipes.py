import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.models.inventory import Recipe, Product
from datetime import datetime

bp = Blueprint('recipes', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_product(product_id):
    """Función auxiliar para obtener un producto por su ID"""
    return Product().get_by_id(product_id)

@bp.route('/recipes')
@login_required
def index():
    recipes = Recipe().get_all()
    # Convertir las fechas de string a datetime
    for recipe in recipes:
        if 'updated_at' in recipe and recipe['updated_at']:
            try:
                recipe['updated_at'] = datetime.fromisoformat(recipe['updated_at'])
            except (ValueError, TypeError):
                recipe['updated_at'] = datetime.now()
    return render_template('recipes/index.html', recipes=recipes)

@bp.route('/recipes/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        
        # Manejar la imagen
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Crear directorio si no existe
                os.makedirs(os.path.join(current_app.static_folder, 'uploads/recipes'), exist_ok=True)
                file.save(os.path.join(current_app.static_folder, 'uploads/recipes', filename))
                image = filename
        
        # Crear la receta
        recipe = Recipe().create_recipe(
            name=name,
            description=description,
            instructions=instructions,
            image=image
        )
        
        # Agregar ingredientes
        ingredients = request.form.getlist('ingredients[]')
        quantities = request.form.getlist('quantities[]')
        
        for i in range(len(ingredients)):
            if ingredients[i] and quantities[i]:
                Recipe().add_ingredient(recipe['id'], int(ingredients[i]), float(quantities[i]))
        
        flash('Receta creada exitosamente', 'success')
        return redirect(url_for('recipes.index'))
    
    products = Product().get_all()
    return render_template('recipes/add.html', products=products)

@bp.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    recipe_model = Recipe()
    recipe = recipe_model.get_by_id(id)
    if not recipe:
        flash('Receta no encontrada', 'error')
        return redirect(url_for('recipes.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        
        # Manejar la imagen
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Eliminar imagen anterior si existe
                if recipe.get('image'):
                    old_image_path = os.path.join(current_app.static_folder, 'uploads/recipes', recipe['image'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                os.makedirs(os.path.join(current_app.static_folder, 'uploads/recipes'), exist_ok=True)
                file.save(os.path.join(current_app.static_folder, 'uploads/recipes', filename))
                recipe['image'] = filename
        
        # Actualizar receta
        recipe_data = {
            'name': name,
            'description': description,
            'instructions': instructions,
            'image': recipe.get('image'),
            'ingredients': [],  # Limpiar ingredientes existentes
            'updated_at': datetime.utcnow().isoformat()
        }
        recipe_model.update(id, recipe_data)
        
        # Agregar nuevos ingredientes
        ingredients = request.form.getlist('ingredients[]')
        quantities = request.form.getlist('quantities[]')
        
        for i in range(len(ingredients)):
            if ingredients[i] and quantities[i]:
                recipe_model.add_ingredient(id, int(ingredients[i]), float(quantities[i]))
        
        flash('Receta actualizada exitosamente', 'success')
        return redirect(url_for('recipes.index'))
    
    products = Product().get_all()
    return render_template('recipes/edit.html', recipe=recipe, products=products)

@bp.route('/recipes/delete/<int:id>')
@login_required
def delete(id):
    recipe_model = Recipe()
    recipe = recipe_model.get_by_id(id)
    if recipe:
        # Eliminar imagen si existe
        if recipe.get('image'):
            image_path = os.path.join(current_app.static_folder, 'uploads/recipes', recipe['image'])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        recipe_model.delete(id)
        flash('Receta eliminada exitosamente', 'success')
    else:
        flash('Receta no encontrada', 'error')
    return redirect(url_for('recipes.index'))

@bp.route('/recipes/view/<int:id>')
@login_required
def view(id):
    recipe = Recipe().get_by_id(id)
    if not recipe:
        flash('Receta no encontrada', 'error')
        return redirect(url_for('recipes.index'))
    
    # Obtener detalles de productos para los ingredientes
    for ingredient in recipe.get('ingredients', []):
        product = Product().get_by_id(ingredient['product_id'])
        if product:
            ingredient['product_name'] = product['name']
            ingredient['unit'] = product['unit']
    
    # Convertir la fecha de string a datetime
    if 'updated_at' in recipe and recipe['updated_at']:
        try:
            recipe['updated_at'] = datetime.fromisoformat(recipe['updated_at'])
        except (ValueError, TypeError):
            recipe['updated_at'] = datetime.now()
    
    return render_template('recipes/view.html', recipe=recipe) 