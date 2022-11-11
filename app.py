import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

CREATE_PRODUCT_TABLE = (
    '''CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            category VARCHAR(255) NOT NULL,
            price INTEGER NOT NULL,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            size INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            img_url VARCHAR(255) NOT NULL,
            cep VARCHAR(8) NOT NULL
        )'''
)

INSERT_PRODUCT_RETURN_ID = (
    '''INSERT INTO products (category, price, name, description, size, rating, quantity, user_id, img_url, cep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'''
)

GET_PRODUCT_BY_ID = (
    '''SELECT * FROM products WHERE id = %s'''
)


load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)



@app.post('/api/add_product')
def create_product():
    data = request.get_json()
    category = data['category']
    price = data['price']
    name = data['name']
    description = data['description']
    size = data['size']
    rating = data['rating']
    quantity = data['quantity']
    user_id = data['user_id']
    img_url = data['img_url']
    cep = data['cep']
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PRODUCT_TABLE)
            cursor.execute(INSERT_PRODUCT_RETURN_ID, (category, price, name, description, size, rating, quantity, user_id, img_url, cep))
            product_id = cursor.fetchone()[0]
            connection.commit()
    return jsonify({'id': product_id}), 201

@app.get('/api/products/<id>')
def get_products(id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_PRODUCT_BY_ID, (id))
            product = cursor.fetchone()
            connection.commit()
    return jsonify({'product': product}), 200