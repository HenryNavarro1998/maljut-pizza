from flask import Blueprint, render_template
from flask_login import login_required
from app.models.inventory import Product, Recipe
from app.models.sales import Sale
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # Obtener datos para el dashboard de inventario
    products = Product().get_all()
    low_stock_products = [
        product for product in products 
        if product['quantity'] <= product['min_quantity']
    ]
    total_products = len(products)
    total_low_stock = len(low_stock_products)
    
    # Obtener datos para el dashboard de recetas
    recipes = Recipe().get_all()
    total_recipes = len(recipes)
    recipes_with_ingredients = [
        recipe for recipe in recipes 
        if recipe.get('ingredients') and len(recipe['ingredients']) > 0
    ]
    total_recipes_with_ingredients = len(recipes_with_ingredients)
    
    # Obtener datos para el dashboard de reportes
    today = datetime.now()
    last_month = today - timedelta(days=30)
    sales_model = Sale()
    sales_last_month = sales_model.get_sales_by_date_range(last_month, today)
    total_sales = sales_model.get_total_sales(last_month, today)

    # Si no hay ventas en el último mes, mostrar el total histórico
    if not sales_last_month:
        sales_last_month = sales_model.get_all()
        total_sales = sales_model.get_total_sales()

    # Calcular recetas más vendidas
    recipe_sales = {}
    for sale in sales_last_month:
        recipe_id = sale.get('recipe_id')
        if recipe_id not in recipe_sales:
            recipe_sales[recipe_id] = 0
        recipe_sales[recipe_id] += sale.get('quantity', 0)
    
    # Ordenar recetas por cantidad vendida
    top_recipes = []
    for recipe_id, quantity in sorted(recipe_sales.items(), key=lambda x: x[1], reverse=True)[:5]:
        recipe = Recipe().get_by_id(recipe_id)
        if recipe:
            top_recipes.append({
                'name': recipe['name'],
                'quantity': quantity
            })
    
    return render_template('main/index.html',
                         # Datos de inventario
                         total_products=total_products,
                         total_low_stock=total_low_stock,
                         low_stock_products=low_stock_products,
                         # Datos de recetas
                         total_recipes=total_recipes,
                         total_recipes_with_ingredients=total_recipes_with_ingredients,
                         # Datos de reportes
                         total_sales=total_sales,
                         top_recipes=top_recipes) 