from datetime import datetime
from .base import JSONModel

class Sale(JSONModel):
    def __init__(self):
        super().__init__('sales.json')
    
    def create_sale(self, recipe_id: int, recipe_name: str, quantity: float, total_ingredients: list):
        """Crea un nuevo registro de venta"""
        sale_data = {
            'recipe_id': recipe_id,
            'recipe_name': recipe_name,
            'quantity': float(quantity),
            'ingredients_used': total_ingredients,
            'created_at': datetime.utcnow().isoformat()
        }
        return self.create(sale_data)
    
    def get_sales_by_date_range(self, start_date: datetime, end_date: datetime):
        """Obtiene las ventas en un rango de fechas"""
        sales = self.get_all()
        filtered_sales = []
        
        for sale in sales:
            if not isinstance(sale, dict):
                continue
                
            try:
                sale_date = datetime.fromisoformat(sale.get('created_at', ''))
                if start_date <= sale_date <= end_date:
                    filtered_sales.append(sale)
            except (ValueError, TypeError):
                continue
        
        return filtered_sales
    
    def get_total_sales(self, start_date: datetime = None, end_date: datetime = None):
        """Obtiene el total de ventas, opcionalmente filtrado por fecha"""
        if start_date and end_date:
            sales = self.get_sales_by_date_range(start_date, end_date)
        else:
            sales = self.get_all()
        
        total = 0
        for sale in sales:
            if isinstance(sale, dict):
                total += float(sale.get('quantity', 0))
        return total 