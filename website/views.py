from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Fruit, Stock, Sale, Sale_detail, User, Prices, Client
from . import db
from sqlalchemy import func


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
    data = db.session.query(Fruit,Prices,Stock).join(Prices, Prices.fruit_id == Fruit.fruit_id).join(Stock, Stock.fruit_id == Fruit.fruit_id).all()
    return render_template("sales.html", user=current_user, data = data)

# Función que guarda las ventas
@views.route('/new_sale', methods=['POST'])
@login_required
def new_sale():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        date = request.form.get('date')
        phone = request.form.get('phone')
        data = request.form.get('saleData')
        neto = request.form.get('getNeto')
        iva = request.form.get('getIva')
        total = request.form.get('getTotal')
        list = data.split(',')
        for i in list:
            kilo,fruit_id,stock_id,subtotal = i.split('+')
            rows_updated =  db.session.query(Stock).filter(Stock.id == int(stock_id)).update({Stock.kilo : Stock.kilo - int(kilo)})
            db.session.commit()
        if rows_updated > 0:
            getClient1 = db.session.query(Client).filter(Client.name == name, Client.phone == phone, Client.address == address).first()
            if not getClient1:
                cliente = Client(name = name, phone = phone, address = address)
                db.session.add(cliente)
                db.session.commit()
            getClient = db.session.query(Client).filter(Client.name == name, Client.phone == phone, Client.address == address).first()
            sale = Sale(client_id = getClient.client_id, neto = neto, iva = iva, total = total, date = date)
            db.session.add(sale)
            db.session.commit()
            getSale = db.session.query(Sale).filter(Sale.client_id == getClient.client_id, Sale.neto == neto, Sale.iva == iva, Sale.total == total, Sale.date == date).first()
            print(list)
            for sales in list:
                kilos,id_fruit,id_stock,subtotals = sales.split('+')
                sale_detail = Sale_detail(sale_id = getSale.sale_id, fruit_id = id_fruit, kilo = kilos, totalFruit = subtotals)
                db.session.add(sale_detail)
                db.session.commit()
            flash("Venta guardada correctamente")
        else:
            flash("No ha sido posible guardar la venta")
    data = db.session.query(Fruit,Prices,Stock).join(Prices, Prices.fruit_id == Fruit.fruit_id).join(Stock, Stock.fruit_id == Fruit.fruit_id).all()
    return render_template("sales.html", user=current_user, data = data)

# Función que busca el stock
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

# Funcion que obtiene los clientes
def list_clients():
    return db.session.query(Client).all()

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

# Función que muestra la página de busqueda de centro de distribución
@views.route('/search_center')
@login_required
def search_center():
    data = []
    return render_template("search.html", user=current_user, data = data)

# Función que muestra la pagina de busqueda de ventas
@views.route('/search_sale')
@login_required
def search_sale():
    data = []
    return render_template("sale.html", user=current_user, data = data)

# Función que realiza la busqueda de centro de distribución
@views.route('/center_search', methods=['GET'])
@login_required
def center_search():
    center = request.args.get('search').title()
    data = db.session.query(Fruit,Stock).join(Stock, Stock.fruit_id == Fruit.fruit_id).filter(Stock.center == center).all()
    if not data:
        flash("No se han encontrado registros para el centro de distribución especificado")
    return render_template("search.html", user=current_user, data = data)

# Función que obtiene los precios de las frutas
@views.route('/get_prices', methods=['GET'])
@login_required
def get_prices():
    data = db.session.query(Fruit,Prices).join(Prices, Prices.fruit_id == Fruit.fruit_id).all() 
    return render_template("price.html", user=current_user, data = data)

# Función que edita los precios de las frutas
@views.route('/edit_price', methods=['POST'])
@login_required
def edit_price():
    fruit_id = request.form.get('price_id')
    price = request.form.get('precio')
    rows_updated = db.session.query(Prices).filter(Prices.fruit_id == fruit_id).update({Prices.price : price})
    db.session.commit()
    if rows_updated > 0:
        flash("Precio modificado correctamente")
    else:
        flash("No ha sido posible modificar el precio")
    data = db.session.query(Fruit,Prices).join(Prices, Prices.fruit_id == Fruit.fruit_id).all() 
    return render_template("price.html", user=current_user, data = data)

# Funcion que realiza la busqueda de ventas
@views.route('/sale_search', methods=['GET'])
@login_required
def sale_search():
    name = request.args.get('name')
    data = db.session.query(Client,Sale).join(Sale, Sale.client_id == Client.client_id).filter(Client.name.contains(name)).all()
    if not data:
        flash("No se han encontrado datos")
    return render_template("sale.html", user=current_user,data = data)

# Función que obtiene los datos de la venta escogida
@views.route('/getsales', methods=['GET'])
@login_required
def get_sales():
    client_id = request.args.get('client_id')
    id_sale = request.args.get('sale_id')
    date = request.args.get('sale_date')
    neto = request.args.get('neto')
    iva = request.args.get('19')
    total = request.args.get('total')
    client = Client.query.filter(Client.client_id == client_id).first()
    saledata = db.session.query(Sale,Sale_detail,Fruit,Prices).join(Sale_detail, Sale_detail.sale_id == Sale.sale_id).join(Fruit, Fruit.fruit_id == Sale_detail.fruit_id).join(Prices, Prices.fruit_id == Fruit.fruit_id).filter(Sale.sale_id == id_sale).all()
    return render_template("sale.html", user=current_user, cliente = client, saledata = saledata, date = date, neto = neto, iva = iva, total = total)

# Función inventario que obtiene y suma el total de kilos vendidos por fruta
@views.route('/inventory', methods=['GET'])
@login_required
def inventory():
    saledata = db.session.query(Sale_detail,Fruit, func.sum(Sale_detail.kilo)).join(Fruit, Fruit.fruit_id == Sale_detail.fruit_id).group_by(Fruit.fruit).all()
    if not saledata:
        flash("No se han encontrado ventas")
    return render_template("inventory.html", user=current_user, saledata = saledata)