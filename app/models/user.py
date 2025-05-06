from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .base import JSONModel
from datetime import datetime

class User(UserMixin, JSONModel):
    def __init__(self):
        super().__init__('users.json')
        self.id = None
        self.username = None
        self.email = None
        self.role = None
    
    def get_by_username(self, username: str):
        """Obtiene un usuario por su nombre de usuario"""
        users = self.get_all()
        for user in users:
            if user['username'].lower() == username.lower():
                return user
        return None
    
    def get_by_email(self, email: str):
        """Obtiene un usuario por su email"""
        users = self.get_all()
        for user in users:
            if user['email'].lower() == email.lower():
                return user
        return None
    
    def create_user(self, username: str, email: str, password: str):
        """Crea un nuevo usuario"""
        user_data = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'role': 'user',  # Rol por defecto
            'created_at': datetime.utcnow().isoformat()
        }
        return self.create(user_data)
    
    def update_user(self, id: int, username: str = None, email: str = None, password: str = None, role: str = None):
        """Actualiza un usuario existente"""
        user = self.get_by_id(id)
        if user:
            if username:
                user['username'] = username
            if email:
                user['email'] = email
            if password:
                user['password'] = generate_password_hash(password)
            if role:
                user['role'] = role
            user['updated_at'] = datetime.utcnow().isoformat()
            return self.update(id, user)
        return False
    
    def check_password(self, user_data: dict, password: str) -> bool:
        """Verifica la contraseña de un usuario"""
        return check_password_hash(user_data['password'], password)
    
    def get_id(self):
        """Implementación requerida por Flask-Login"""
        return str(self.id) if self.id is not None else None 