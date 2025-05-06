from datetime import datetime
from .base import JSONModel

class Product(JSONModel):
    def __init__(self):
        super().__init__('products.json')
    
    def get_by_name(self, name: str):
        """Obtiene un producto por su nombre"""
        products = self.get_all()
        for product in products:
            if product['name'].lower() == name.lower():
                return product
        return None
    
    def create_product(self, name: str, description: str, quantity: float, unit: str, min_quantity: float):
        """Crea un nuevo producto"""
        product_data = {
            'name': name,
            'description': description,
            'quantity': float(quantity),
            'unit': unit,
            'min_quantity': float(min_quantity),
            'updated_at': datetime.utcnow().isoformat()
        }
        return self.create(product_data)
    
    def update_stock(self, id: int, quantity: float):
        """Actualiza el stock de un producto"""
        product = self.get_by_id(id)
        if product:
            product['quantity'] = float(quantity)
            product['updated_at'] = datetime.utcnow().isoformat()
            return self.update(id, product)
        return False

class Recipe(JSONModel):
    def __init__(self):
        super().__init__('recipes.json')
    
    def get_by_name(self, name: str):
        """Obtiene una receta por su nombre"""
        recipes = self.get_all()
        for recipe in recipes:
            if recipe['name'].lower() == name.lower():
                return recipe
        return None
    
    def create_recipe(self, name: str, description: str, instructions: str, image=None):
        """Crea una nueva receta"""
        recipe_data = {
            'name': name,
            'description': description,
            'instructions': instructions,
            'image': image,
            'ingredients': [],
            'updated_at': datetime.utcnow().isoformat()
        }
        return self.create(recipe_data)
    
    def add_ingredient(self, recipe_id: int, product_id: int, quantity: float):
        """Agrega un ingrediente a una receta"""
        recipe = self.get_by_id(recipe_id)
        if recipe:
            # Obtener información del producto
            product = Product().get_by_id(product_id)
            if not product:
                return False
                
            # Crear el ingrediente con toda la información necesaria
            ingredient = {
                'product_id': int(product_id),
                'product_name': product['name'],
                'quantity': float(quantity),
                'unit': product['unit']
            }
            
            # Agregar el ingrediente a la receta
            if 'ingredients' not in recipe:
                recipe['ingredients'] = []
            recipe['ingredients'].append(ingredient)
            recipe['updated_at'] = datetime.utcnow().isoformat()
            return self.update(recipe_id, recipe)
        return False
    
    def remove_ingredient(self, recipe_id: int, product_id: int):
        """Elimina un ingrediente de una receta"""
        recipe = self.get_by_id(recipe_id)
        if recipe:
            recipe['ingredients'] = [
                ing for ing in recipe['ingredients']
                if ing['product_id'] != int(product_id)
            ]
            recipe['updated_at'] = datetime.utcnow().isoformat()
            return self.update(recipe_id, recipe)
        return False 