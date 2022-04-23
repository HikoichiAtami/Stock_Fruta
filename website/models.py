from werkzeug.wrappers.user_agent import UserAgentMixin
from . import db
from flask_login import UserMixin
from sqlalchemy import func

# Tabla de usuario para login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String)

# Tabla con las frutas
class Fruit(db.Model):
    fruit = db.Column(db.String(150))
    fruit_id = db.Column(db.Integer, primary_key=True)
    stocks = db.relationship('Stock')
    sale_details = db.relationship('Sale_detail')

# Tabla que mantiene el stock
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kilo = db.Column(db.Integer)
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.fruit_id'))
    center = db.Column(db.String(150))

# Tabla con las ventas
class Sale(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True)
    neto = db.Column(db.Integer)
    iva = db.Column(db.Integer)
    total = db.Column(db.Integer)
    date = db.Column(db.String(150))
    sales_details = db.relationship('Sale_detail')
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

# Tabla con el detalle de ventas
class Sale_detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.sale_id'))
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.fruit_id'))
    kilo = db.Column(db.Integer)
    totalFruit = db.Column(db.Integer)

# Tabla que mantiene los precios
class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.fruit_id'))

# Tabla de clientes
class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    address = db.Column(db.String(150))
    sale_id = db.relationship('Sale')



