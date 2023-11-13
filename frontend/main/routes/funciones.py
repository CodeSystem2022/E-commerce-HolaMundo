from flask import *
import requests, json
from datetime import datetime

def registro(username, email, phone, address, password, repeat_password):
    if password == repeat_password:
        url = set_url("/auth/register")
        data = {
            "username": username,
            "email": email,
            "phone": phone,
            "address": address,
            "password": password,
            "role": "user"
        }
        headers = get_headers(without_token = True)
        response = requests.post(url, json = data, headers = headers)
        return response
    else:
        return "Las contraseñas no coinciden"
    
def login(email, password):
    url = set_url("/auth/login")
    data = {
        "email": email,
        "password": password
    }
    headers = get_headers(without_token = True)
    response = requests.post(url, json = data, headers = headers)

    return response


def get_jwt():
    return request.cookies.get("access_token")

def get_id():
    return request.cookies.get("id")
    
def set_url(endpoint):
    api_url = current_app.config["API_URL"]
    url = api_url + endpoint
    return url

def get_headers(without_token = False):
    jwt = get_jwt()
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
    else:
        return {"Content-Type" : "application/json"}
    
def get_food(auth = False):
    url = set_url("/foods")
    if auth == True:
        headers = get_headers()
    else:
        headers = get_headers(without_token = True)
    response = requests.get(url, headers = headers)
    return response

def create_order(user_id, status, description):
    url = set_url("/orders")

    if description == "":
        description = "Sin descripción"
    data = {
        "user_id": user_id,
        "status": status,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    headers = get_headers()
    response = requests.post(url, json=data, headers=headers)
    return response

def create_product_relation(order_id, food_id):
    url = set_url("/products")
    data = {
        "order_id": order_id,
        "food_id": food_id
    }
    headers = get_headers()
    response = requests.post(url, json=data, headers=headers)
    return response

def get_order(order_id):
    url = set_url(f"/order/{order_id}")
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response

def get_user(user_id):
    url = set_url(f"/user/{user_id}")
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response


