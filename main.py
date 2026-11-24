from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__) # Instance of the Flask 

DB_NAME = 'online-store.db' # Database name, all caps is a convention to indicate that this variable is a constant

# SQL DATA TYPES: TEXT, INTEGER, REAL, BLOB, NULL
# INTEGER: Whole numbers, TEXT: String of characters, REAL: Floating point numbers (decimals), BLOB: Binary data, NULL: Represents missing or undefined values


# ---- TABLES ----- 
def init_db():
    # Initialize the database tables here
    connection = sqlite3.connect(DB_NAME) # Step 1: Opens the connection to the D.B named 'online-store.db'
    cursor = connection.cursor() # Step 2: Create a cursor/tool object to execute SQL commands
    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            code TEXT UNIQUE NOT NULL,
            discount INTEGER NOT NULL,
            description TEXT
        )
    ''') # Step 3: Execute the SQL command to create the 'coupons' table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT UNIQUE NOT NULL, 
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image TEXT NOT NULL
        )
""")

    # Id will always be PRIMARY KEY and AUTOINCREMENT, meaning it will be unique and automatically incremented for each new entry
    connection.commit() # Step 3: Saves the changes to the database
    connection.close() # Step 4: Closes the connection to the database


# GET /api/health -> Make sure the API is running and healthy
@app.get('/api/health')
def health_check():
    return jsonify({'status': 'Okay'}), 200     # Return a JSON response indicating the health status


# ----- COUPONS END POINTS -----

# POST /api/coupons -> Create/add a coupon to the DB 
@app.post('/api/coupons')
def create_coupon():
    new_coupon = request.get_json() # Get the JSON data from the request body
    code = new_coupon["code"] 
    discount = new_coupon["discount"]

    connection = sqlite3.connect(DB_NAME) # 1. Open a connection to the database
    cursor = connection.cursor() # 2. Create a cursor to execute SQL commands
    cursor.execute("""
        INSERT INTO coupons (code, discount) 
        VALUES (?, ?)""", 
        (code, discount)) # 3. Execute the SQL command to insert a new coupon into the 'coupons' table
    connection.commit() # 4. Saves the changes to the database
    connection.close() # 5. Close the connection to the database

    return jsonify({
        'success': True,
        'message': 'Coupon created successfully'
    }), 201 # CREATED


# GET /api/coupons -> Get all records in the coupons table
@app.get('/api/coupons')
def get_coupons():
    connection = sqlite3.connect(DB_NAME)

    # Makes each row behave like a dictionary
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM coupons")

    # Fetchall retrieves all the rows from the result of the query
    coupon_db = cursor.fetchall()

    connection.close()

    coupons_list = []

    for coupon in coupon_db:
        print(coupon)
        coupons_list.append(dict(coupon))

    return jsonify({
        "Success": True,
        "Message": "Coupons retrieved successfully",
        "Data": coupons_list
    })


# GET /api/coupons/<2> -> Retrive a single coupon by id using a path parameter
@app.get("/api/coupons/<int:coupon_id>")
def get_coupon_by_id(coupon_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id))
    coupon_db = cursor.fetchone
    connection.close()

    print(coupon_db)
    coupon = dict(coupon_db)

    return jsonify({
        "Success" : True, 
        "Message" : "Coupon retrieved successfully",
        "Data" : coupon
    }), 200


# DELETE /api/coupons 
@app.delete("/api/coupons/<int:coupon_id>")
def delete_coupon_by_id(coupon_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id,))
    coupon_db = cursor.fetchone()

    if not coupon_db:
        connection.close()
        return jsonify({
            "Success": False,
            "Message": "Coupon not found"
        }), 404

    cursor.execute("DELETE FROM coupons WHERE id = ?", (coupon_id,))
    connection.commit()
    connection.close()

    return jsonify({
        "Success": True, 
        "Message" : "Coupon deleted successfully"
    }), 200

# PUT /api/coupons/<3>
@app.put("/api/coupons/<int:coupon_id>")
def update_coupon_by_id(coupon_id):
    updated_coupon = request.get_json()

    code = updated_coupon["code"]
    discount = updated_coupon["discount"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id,))
    coupon_db = cursor.fetchone()

    if not coupon_db:
        connection.close()
        return jsonify({
            "success": False, 
            "message": "Coupon not found"
        }), 404

    cursor.execute("""
        UPDATE coupons
        SET code = ?, discount = ?
        WHERE id = ?
    """, (code, discount, coupon_id))

    connection.commit()
    connection.close()

    return jsonify({
        "Success": True,
        "Message": "Coupon has been updated successfully"
    }), 200

# ---- Products ---- 
# POST /api/products 
@app.post("/api/products")
def create_product():
    new_product = request.get_json()

    product_name = new_product["name"]
    product_price = new_product["price"]
    product_category = new_product["category"]
    product_image = new_product["image"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products (name, price, category, image)
        VALUES (?, ?, ?, ?)
    """, (
        product_name,
        product_price,
        product_category,
        product_image
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "Success": True,
        "Message": "Product created successfully"
    }), 201


# GET /api/products -> Return all the products records
@app.get("/api/products")
def get_products():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products_db = cursor.fetchall()
    connection.close()

    product_list = []
    for products in products_db:
        print(products)
        product_list.append(dict(products))

    return jsonify({
        "Success": True, 
        "Message": "Products retrieved successfully",
        "Data": product_list
    }), 200


# GET /api/products/<id> -> Return a product by id
@app.get("/api/products/<int:product_id>")
def get_product_by_id(product_id):

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product_db = cursor.fetchone()

    connection.close()

    print(product_db)

    if product_db is None:
        return jsonify({
            "Success": False,
            "Message": "Product not found"
        }), 404

    product = dict(product_db)

    return jsonify({
        "Success": True,
        "Message": "Product retrieved successfully",
        "Data": product
    }), 200


# DELETE /api/products/<products_id>
@app.delete("/api/products/<int:coupon_id>")
def delete_by_id(product_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM coupons WHERE id = ?", (product_id,))
    coupon_db = cursor.fetchone()

    if not coupon_db:
        connection.close()
        return jsonify({
            "Success": False,
            "Message": "Coupon not found"
        }), 404

    cursor.execute("DELETE FROM coupons WHERE id = ?", (product_id,))
    connection.commit()
    connection.close()

    return jsonify({
        "Success": True, 
        "Message" : "Coupon deleted successfully"
    }), 200


# PUT /api/products/<product_id>
@app.put("/api/products/<int:product_id>")
def update_product_by_id(product_id):
    updated_product_name = request.get_json()
    updated_product_price = request.get_json()
    updated_product_category = request.get_json()
    updated_product_image = request.get_json()

    name = updated_product_name["name"]
    price = updated_product_price["price"]
    category = updated_product_category["category"]
    image = updated_product_image["image"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM coupons WHERE id = ?", (product_id,))
    coupon_db = cursor.fetchone()

    if not coupon_db:
        connection.close()
        return jsonify({
            "success": False, 
            "message": "Coupon not found"
        }), 404

    cursor.execute("""
        UPDATE coupons
        SET code = ?, discount = ?
        WHERE id = ?
    """, (name, price, category, image, product_id))

    connection.commit()
    connection.close()

    return jsonify({
        "Success": True,
        "Message": "Coupon has been updated successfully"
    }), 200


init_db() # Call the function to initialize the database tables
app.run(debug=True) # Run the Flask application in debug mode