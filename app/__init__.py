from flask import Flask
from flask_login import LoginManager
from config import Config
from app.models.user import User
from app.filters import nl2br

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    user_model = User()
    user_data = user_model.get_by_id(int(user_id))
    if user_data:
        user = User()
        user.id = user_data['id']
        user.username = user_data['username']
        user.email = user_data['email']
        user.role = user_data['role']
        return user
    return None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login_manager.init_app(app)
    
    # Registrar filtros personalizados
    app.jinja_env.filters['nl2br'] = nl2br
    
    # Crear usuario administrador al iniciar
    with app.app_context():
        user_model = User()
        admin = user_model.get_by_username('admin')
        if not admin:
            user_model.create(username='admin', password='Admin123', role='admin')

    from app.routes import main, auth, inventory, recipes, users, sales
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(recipes.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(sales.bp)
    
    return app 