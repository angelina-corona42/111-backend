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


init_db() # Call the function to initialize the database tables
app.run(debug=True) # Run the Flask application in debug mode
