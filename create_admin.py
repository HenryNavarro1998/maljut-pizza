from app import create_app
from app.models.user import User

def create_admin_user():
    app = create_app()
    with app.app_context():
        user_model = User()
        # Verificar si ya existe un usuario admin
        admin = user_model.get_by_username('admin')
        if not admin:
            user_model.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin'
            )
            print("Usuario administrador creado exitosamente")
        else:
            print("El usuario administrador ya existe")

if __name__ == '__main__':
    create_admin_user() 