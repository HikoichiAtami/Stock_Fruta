from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Fruit, Stock, Sale, Sale_detail, User
from . import db


# Registro de la vista
views = Blueprint('views', __name__)

# Pagina Stock que sera accesible luego de logearse
@views.route('/stock', methods=['GET'])
@login_required
def stock():
    data = db.session.query(Fruit,Stock).filter(Fruit.fruit_id == Stock.fruit_id).all()
    return render_template("stock.html", user=current_user, data = data)

# Pagina para modificar stock que sera accesible luego de logearse
@views.route('/get_fruits')
@login_required
def get_fruits():
    fruit = list_fruits()
    data = []
    return render_template("modify_stock.html", user=current_user, fruit = fruit, data = data)

# Pagina para mostrar pagina ventas
@views.route('/sales')
@login_required
def sales():
    return render_template("sales.html", user=current_user)

@views.route('/new_sale', methods=['POST'])
@login_required
def new_sale():
    if request.method == 'POST':
        flash("Ingreso correcto")

    return render_template("sales.html", user=current_user)

@views.route('/search_stock', methods=['GET'])
@login_required
def search_stock():
    fruit_id = request.args.get('fruit')
    data = db.session.query(Fruit, Stock).join(Stock, Stock.fruit_id == fruit_id).filter(Fruit.fruit_id == fruit_id).all()
    fruit = list_fruits()
    if not data:
        flash("No se ha encontrado stock para la fruta seleccionada")
    return render_template("modify_stock.html", user=current_user, fruit = fruit, data = data)

# Funcion que redirige a la pagina para agregar registros
@views.route('/add_stock')
@login_required
def add_stock():
    fruit = list_fruits()
    return render_template("new_stock.html", user=current_user, fruit=fruit)

# Funcion que crea un nuevo registro
@views.route('/new_stock', methods=['POST'])
@login_required
def new_stock():
    fruit_id = request.form.get('fruit')
    stock = request.form.get('stock')
    center = request.form.get('center').title()
    get_stock = db.session.query(Stock).filter(Stock.fruit_id == fruit_id, Stock.center == center).first()
    fruit = list_fruits()
    if get_stock:
        flash("Ya existe un registro para la fruta indicada en " + center)
    else:
        new_stock = Stock(kilo = stock, center = center, fruit_id = fruit_id)
        db.session.add(new_stock)
        db.session.commit()
        flash("Registro añadido correctamente")
    return render_template("new_stock.html", user=current_user, fruit=fruit)

# Funcion que elimina los registros
@views.route('/delete_stock', methods=['POST'])
@login_required
def delete_stock():
    stock_id = request.form.get('id_stock')
    stock = Stock.query.get(stock_id)
    db.session.delete(stock)
    db.session.commit()
    flash("Registro eliminado correctamente")
    data = db.session.query(Fruit,Stock).filter(Fruit.fruit_id == Stock.fruit_id).all()
    return render_template("stock.html", user=current_user, data = data)

# Funcion que obtiene la lista de frutas
def list_fruits():
    return db.session.query(Fruit).all()

# Funcion que actualiza los registros
@views.route('/edit_stock', methods=['POST'])
@login_required
def edit_stock():
    stock_id = request.form.get('id_stock')
    kilo = request.form.get('kilos')
    rows_updated = db.session.query(Stock).filter(Stock.id == stock_id).update({Stock.kilo : kilo})
    db.session.commit()
    if rows_updated > 0:
        flash("Stock modificado correctamente")
    else:
        flash("No ha sido posible modificar el stock")
    data = db.session.query(Fruit,Stock).filter(Fruit.fruit_id == Stock.fruit_id).all()
    return render_template("stock.html", user=current_user, data = data)

@views.route('/search_center')
@login_required
def search_center():
    data = []
    return render_template("search.html", user=current_user, data = data)

@views.route('/center_search', methods=['GET'])
@login_required
def center_search():
    center = request.args.get('search').title()
    data = db.session.query(Fruit,Stock).join(Stock, Stock.fruit_id == Fruit.fruit_id).filter(Stock.center == center).all()
    if not data:
        flash("No se han encontrado registros para el centro de distribución especificado")
    return render_template("search.html", user=current_user, data = data)