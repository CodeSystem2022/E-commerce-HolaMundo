from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for, Response, make_response, flash, session
import requests
import json
from . import funciones as f
from main.utils import images_paths



app = Blueprint('app', __name__, url_prefix='/')

# Declaro una lista global
global products_in_cart
products_in_cart = []
global products_final
products_final = []

#registro usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        address = request.form.get('address')
        phone = request.form.get('phone')

        if username != None or email != None or password != None or repeat_password != None or address != None or phone != None:    
            response = f.registro(username, email, phone, address, password, repeat_password)
            if response.status_code == 201:
                flash("Usuario creado correctamente")
                return redirect(url_for('app.login'))
            else:
                error = response.text
                return render_template('register.html', error = error)
        else:
            flash("Error al crear el usuario")
            return redirect(url_for('app.register'))
    else:
        return render_template('register.html')
    
#login usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email != None or password != None:    
            response = f.login(email, password)
            if response.status_code == 200:
                flash("Usuario logueado correctamente")
                token = str(response.json()["access_token"])
                user_id = str(response.json()["id"])
                resp = make_response(redirect(url_for('app.index')))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                return resp
            else:
                error = response.text
                return render_template('login.html', error = error)
        else:
            flash("Error al loguear el usuario")
            return redirect(url_for('app.login'))
    else:
        return render_template('login.html')
    
#logout usuario
@app.route('/logout')
def logout():
    response = make_response(redirect('login'))
    response.set_cookie("access_token", "", expires = 0)
    return response

@app.route('/index')
def index():
    jwt = f.get_jwt()
    if jwt:
        return render_template('index.html', jwt = jwt)
    return render_template('index.html')


@app.route('/nosotros')
def nosotros():
    jwt = f.get_jwt()
    if jwt:
        return render_template('nosotros.html', jwt = jwt)
    return render_template('nosotros.html')

@app.route('/trabajo')
def trabajo():
    jwt = f.get_jwt()
    if jwt:
        return render_template('trabajo.html', jwt = jwt)
    return render_template('trabajo.html')

@app.route('/productos', methods=['GET'])
def food():
    jwt = f.get_jwt()
    if jwt:
        response = f.get_food(auth = True)
        if response.status_code == 200:
            try:
                foods = response.json()
                return render_template('producto.html', jwt=jwt, foods=foods, images_paths=images_paths)
            except ValueError as e:
                return f"Error al cargar la respuesta JSON: {e}"
        else:
            return render_template('producto.html', jwt=jwt)
    else:
        return redirect(url_for('app.producto_public'))


@app.route('/public/productos')
def producto_public():
    response = f.get_food(auth=True)
    if response.status_code == 200:
        try:
            foods = response.json()
            return render_template('producto_public.html', foods=foods, images_paths=images_paths)
        except ValueError as e:
            return f"Error al cargar la respuesta JSON: {e}"
    else:
        return render_template('producto_public.html')
    

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    jwt = f.get_jwt()
    if jwt:
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_price = request.form.get('product_price')
        product_description = request.form.get('product_description')
        if product_id and product_name and product_price and product_description:
            product = {
                "id": product_id,
                "name": product_name,
                "price": product_price,
                "description": product_description,
                "category": "Sin categoría",
            }
            
            products_in_cart.append(product)  # Agrega el producto a la lista en la sesión
            return redirect(url_for('app.carrito'))

@app.route('/carrito')
def carrito():
    jwt = f.get_jwt()
    if jwt:
        total_price = 0.0
        for product in products_in_cart:
            total_price += float(product["price"])
        return render_template('carrito.html', jwt=jwt, products_in_cart=products_in_cart, total_price=total_price)
    return render_template('login.html')

@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    jwt = f.get_jwt()
    if jwt:
        product_id = request.form.get('product_id')
        for product in products_in_cart:
            if product["id"] == product_id:
                products_in_cart.remove(product)
        return redirect(url_for('app.carrito'))
    
@app.route('/pagar', methods=['POST'])
def pagar():
    jwt = f.get_jwt()
    if jwt:
        product = request.form.get('product')
        total_price = request.form.get('total_price')
        description = request.form.get('description')
        for product in products_in_cart:
            products_final.append(product)
        return render_template('pago.html', jwt = jwt, products_final = products_final, description = description, total_price = total_price)
    return render_template('pago.html')
        
@app.route('/order', methods=['POST', 'GET'])
def order():
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            products = products_in_cart  # Obtener la lista de productos del carrito

            if products:
                user_id = f.get_id()
                status = "Pagado"
                description = request.form.get('description', default="Sin descripción")
                total_price = request.form.get('total_price')
                
                # Crear la orden
                response_order = f.create_order(user_id, status, description)
                
                if response_order and response_order.status_code == 201:
                    order_id = response_order.json().get('id')  # Obtener el ID de la orden creada

                    # Crear las relaciones entre la orden y los productos
                    product_responses = []
                    for product in products:
                        product_id = product.get('id')


                        response_product = f.create_product_relation(order_id, product_id)
                        response_product = response_product.json()
                        product_responses.append(response_product)

                    order = f.get_order(order_id)
                    order_data = order.json()


                    user = f.get_user(user_id)
                    user_data = user.json() if user else None 
                    print("ESTO ES USER: ", user)
                    return render_template('order.html', jwt=jwt, order=order_data, user=user_data,products=products, total_price=total_price)
                else:
                    error = "Error al crear la orden."
                    return render_template('order.html', jwt=jwt, error=error)
            else:
                error = "No hay productos en el carrito para crear la orden."
                return render_template('order.html', jwt=jwt, error=error)
        else:
            error = "Método no permitido para esta operación."
            return render_template('order.html', jwt=jwt, error=error)
    else:
        error = "Error de autenticación."
        return redirect(url_for('app.login'),error=error)



