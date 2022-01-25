from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Declaracion de la DB
db = SQLAlchemy()

# Nombre de la DB
db_name = 'fruta.db'

# Funcion que ejecuta la aplicacion
def create_app():
    app = Flask(__name__)
    
    # Clave secreta
    app.config['SECRET_KEY'] = 'programa fruta freddy'

    # Ubicacion de la DB
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

    # Inicializacion de la DB en la App
    db.init_app(app)

    # Se importan los archivos
    from .views import views
    from .auth import auth

    # Registro de paginas
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Fruit, Sale, Sale_detail, Stock

    create_database(app)

    # Acceso a vista cuando el usuario esta logeado
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Funcion que carga y obtiene el id del usuario logeado
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Funcion que verifica si existe la DB y la crea si no existe
def create_database(app):
    if not path.exists('website/' + db_name):
        db.create_all(app=app)
        print('Created Dabatase!')
