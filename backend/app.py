import sqlite3
from flask import Flask, request, jsonify

# Create a Flask application instance
app = Flask(__name__)

# --- Database Connection ---
# Establishes a connection to the SQLite database.
# Using sqlite3.Row as the row_factory allows accessing columns by name.
def get_db_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect('trackwise_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# --- API Endpoint for User Login ---
@app.route('/api/login', methods=['POST'])
def login():
    """
    Handles user login attempts.
    Expects a JSON payload with 'username' and 'password'.
    """
    # 1. Receive JSON data from the request
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400
            
    except Exception as e:
        # Handle cases where the request is not JSON or is malformed
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 2. Query the Employee table for the given username
        cursor.execute("SELECT * FROM Employee WHERE Username = ?", (username,))
        employee = cursor.fetchone() # Fetch one record

        # 3. Check if user exists and if the password matches
        # NOTE: This is a simple, direct password comparison as requested.
        # In a real-world application, ALWAYS use hashed passwords (e.g., with Werkzeug or passlib).
        if employee and employee['PasswordHash'] == password:
            # 4. Successful login
            return jsonify({"success": True}), 200
        else:
            # 5. Invalid username or password
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

    except Exception as e:
        # General error handling for database issues
        return jsonify({"success": False, "message": f"An internal error occurred: {e}"}), 500
        
    finally:
        # 6. Always close the database connection
        conn.close()

# --- Main entry point to run the Flask app ---
if __name__ == '__main__':
    # Runs the app on port 5000 in debug mode for development
    app.run(debug=True)
    
    # ==============================================================================
# TrackWise Inventory Management System - Flask API
# ==============================================================================

# --- Imports ---
# Flask for web server functionality.
# jsonify for creating JSON responses.
# request to access incoming request data (like JSON payloads).
# sqlite3 to interact with the SQLite database.
from flask import Flask, jsonify, request
import sqlite3

# --- Application Setup ---
# 1. Create a Flask application instance.
app = Flask(__name__)

# 2. Define the path to the SQLite database file.
DATABASE = 'trackwise.db'


# --- Database Utility Function ---
# 3. A function to create and return a database connection.
#    This helps avoid redundant code and manages connections cleanly.
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The connection is configured to return rows as dictionary-like objects
    (sqlite3.Row), which allows accessing columns by name.
    """

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This is a crucial line for convenient data access
    return conn


# --- API ROUTES WILL GO HERE ---
# 4. Placeholder for all your future API endpoints.
#    Example: @app.route('/api/products', methods=['GET'])

@app.route('/')
def index():
    """A simple route to confirm the server is running."""
    return "TrackWise API is running!"


# --- Main Execution Block ---
# 5. The standard Python entry point.
#    This block runs the Flask development server when the script is executed directly.
#    debug=True enables auto-reloading on code changes and provides helpful error pages.
if __name__ == '__main__':
    app.run(debug=True)
    
    # ==============================================================================
# TrackWise Inventory Management System - Flask API
# ==============================================================================

# --- Imports ---
from flask import Flask, jsonify, request
import sqlite3

# --- Application Setup ---
app = Flask(__name__)
DATABASE = 'trackwise.db'


# --- Database Utility Function ---
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The connection is configured to return rows as dictionary-like objects.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --- API ROUTES WILL GO HERE ---
# ==============================================================================
# TrackWise Inventory Management System - Flask API
# ==============================================================================

# --- Imports ---
from flask import Flask, jsonify, request
import sqlite3

# --- Application Setup ---
app = Flask(__name__)
DATABASE = 'trackwise.db'


# --- Database Utility Function ---
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The connection is configured to return rows as dictionary-like objects.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --- API ROUTES WILL GO HERE ---

@app.route('/')
def index():
    """A simple route to confirm the server is running."""
    return "TrackWise API is running!"

# ======================= User Login Endpoint =======================
@app.route('/api/login', methods=['POST'])
def login():
    """
    Handles user login by validating credentials against the Employee table.
    Expects a JSON payload with 'username' and 'password'.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400
    except:
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Employee WHERE Username = ? AND PasswordHash = ?",
            (username, password)
        )
        employee = cursor.fetchone()

        if employee:
            return jsonify({"success": True})
        else:
            return jsonify({"success": false, "message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"success": False, "message": "An internal server error occurred"}), 500
    finally:
        conn.close()


# ======================= Low Stock Products Endpoint =======================
@app.route('/api/products/lowstock', methods=['GET'])
def get_low_stock_products():
    """
    Retrieves a list of all products where the stock quantity is 10 or less.
    """
    conn = get_db_connection()
    try:
        # 1. Query the Product table for items with QuantityInStock <= 10.
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product WHERE QuantityInStock <= 10 ORDER BY QuantityInStock ASC")
        rows = cursor.fetchall()

        # 2. Convert the list of database rows into a list of dictionaries.
        #    This is the standard way to prepare data for JSON serialization.
        low_stock_products = [dict(row) for row in rows]

        # 3. Return the list as a JSON response with a 200 OK status.
        return jsonify(low_stock_products)

    except Exception as e:
        # Handle any potential database errors.
        print(f"Database error: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

    finally:
        # Ensure the database connection is always closed.
        conn.close()


# --- Main Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/')
def index():
    """A simple route to confirm the server is running."""
    return "TrackWise API is running!"

# ======================= User Login Endpoint =======================
@app.route('/api/login', methods=['POST'])
def login():
    """
    Handles user login by validating credentials against the Employee table.
    Expects a JSON payload with 'username' and 'password'.
    """
    # 1. Get the JSON data from the incoming request.
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Basic validation to ensure fields are not empty
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400

    except:
        # Handle cases where the request body is not valid JSON
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    conn = get_db_connection()
    try:
        # 2. Query the Employee table for a matching username and password.
        #    Using parameterized queries (?) prevents SQL injection vulnerabilities.
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Employee WHERE Username = ? AND PasswordHash = ?",
            (username, password)
        )
        employee = cursor.fetchone()

        # 3. Check if a user was found
        if employee:
            # 4. If successful, return a success response.
            return jsonify({"success": True})
        else:
            # 5. If it fails, return a 401 Unauthorized status and an error message.
            return jsonify({"success": false, "message": "Invalid credentials"}), 401

    except Exception as e:
        # Catch any potential database errors
        print(f"Database error: {e}")
        return jsonify({"success": False, "message": "An internal server error occurred"}), 500

    finally:
        # Ensure the database connection is always closed
        conn.close()


# --- Main Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)
    
    # ==============================================================================
# TrackWise Inventory Management System - Flask API
# ==============================================================================

# --- Imports ---
from flask import Flask, jsonify, request
import sqlite3

# --- Application Setup ---
app = Flask(__name__)
DATABASE = 'trackwise.db'


# --- Database Utility Function ---
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The connection is configured to return rows as dictionary-like objects.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --- API ROUTES WILL GO HERE ---

@app.route('/')
def index():
    """A simple route to confirm the server is running."""
    return "TrackWise API is running!"

# ======================= User Login Endpoint =======================
"""@app.route('/api/login', methods=['POST'])

def login():
    
    Handles user login by validating credentials against the Employee table.
    Expects a JSON payload with 'username' and 'password'.
    
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400
    except:
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Employee WHERE Username = ? AND PasswordHash = ?",
            (username, password)
        )
        employee = cursor.fetchone()

        if employee:
            return jsonify({"success": True})
        else:
            return jsonify({"success": false, "message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"success": False, "message": "An internal server error occurred"}), 500
    finally:
        conn.close()
"""

# ======================= Low Stock Products Endpoint =======================
@app.route('/api/products/lowstock', methods=['GET'])
def get_low_stock_products():
    """
    Retrieves a list of all products where the stock quantity is 10 or less.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product WHERE QuantityInStock <= 10 ORDER BY QuantityInStock ASC")
        rows = cursor.fetchall()

        low_stock_products = [dict(row) for row in rows]
        return jsonify(low_stock_products)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
    finally:
        conn.close()


# ======================= Recent Sales Endpoint =======================
@app.route('/api/sales/recent', methods=['GET'])
def get_recent_sales():
    """
    Retrieves the 5 most recent sales from the Sale table.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 1. Query the Sale table, ordering by SaleDate in descending order
        #    and limiting the result set to 5 records.
        cursor.execute("SELECT * FROM Sale ORDER BY SaleDate DESC LIMIT 5")
        rows = cursor.fetchall()

        # 2. Convert the database rows into a list of dictionaries.
        recent_sales = [dict(row) for row in rows]

        # 3. Return the list as a JSON response.
        return jsonify(recent_sales)
        
    except Exception as e:
        # Handle any potential database errors.
        print(f"Database error: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
        
    finally:
        # Ensure the database connection is always closed.
        conn.close()


# --- Main Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)
    
    # ==============================================================================
# TrackWise Inventory Management System - Flask API
# ==============================================================================

# --- Imports ---
from flask import Flask, jsonify, request
import sqlite3

# --- Application Setup ---
app = Flask(__name__)
DATABASE = 'trackwise.db'


# --- Database Utility Function ---
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The connection is configured to return rows as dictionary-like objects.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --- API ROUTES WILL GO HERE ---

@app.route('/')
def index():
    """A simple route to confirm the server is running."""
    return "TrackWise API is running!"

# ======================= User Login Endpoint =======================
@app.route('/api/login', methods=['POST'])
def login():
    """
    Handles user login by validating credentials against the Employee table.
    Expects a JSON payload with 'username' and 'password'.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400
    except:
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Employee WHERE Username = ? AND PasswordHash = ?",
            (username, password)
        )
        employee = cursor.fetchone()

        if employee:
            return jsonify({"success": True})
        else:
            return jsonify({"success": false, "message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"success": False, "message": "An internal server error occurred"}), 500
    finally:
        conn.close()


# ======================= Low Stock Products Endpoint =======================
@app.route('/api/products/lowstock', methods=['GET'])
def get_low_stock_products():
    """
    Retrieves a list of all products where the stock quantity is 10 or less.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product WHERE QuantityInStock <= 10 ORDER BY QuantityInStock ASC")
        rows = cursor.fetchall()

        low_stock_products = [dict(row) for row in rows]
        return jsonify(low_stock_products)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
    finally:
        conn.close()


# ======================= Recent Sales Endpoint =======================
@app.route('/api/sales/recent', methods=['GET'])
def get_recent_sales():
    """
    Retrieves the 5 most recent sales from the Sale table.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sale ORDER BY SaleDate DESC LIMIT 5")
        rows = cursor.fetchall()

        recent_sales = [dict(row) for row in rows]
        return jsonify(recent_sales)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
    finally:
        conn.close()


# ======================= Dashboard KPIs Endpoint =======================
@app.route('/api/kpi/dashboard', methods=['GET'])
def get_dashboard_kpis():
    """
    Calculates and returns key performance indicators for the dashboard.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Calculate total sales for the current day.
        #    date('now') is an SQLite function to get the current date.
        cursor.execute("SELECT SUM(TotalAmount) FROM Sale WHERE date(SaleDate) = date('now')")
        total_sales_today = cursor.fetchone()[0] or 0.0

        # 2. Calculate the total number of items currently in stock.
        cursor.execute("SELECT SUM(QuantityInStock) FROM Product")
        total_items_in_stock = cursor.fetchone()[0] or 0

        # 3. Calculate the total value of the inventory (based on purchase price).
        cursor.execute("SELECT SUM(PurchasePrice * QuantityInStock) FROM Product")
        total_inventory_value = cursor.fetchone()[0] or 0.0

        # 4. Assemble the results into a single JSON object.
        kpis = {
            "totalSalesToday": round(total_sales_today, 2),
            "totalItemsInStock": total_items_in_stock,
            "totalInventoryValue": round(total_inventory_value, 2)
        }
        return jsonify(kpis)

    except Exception as e:
        # Handle any potential database errors.
        print(f"Database error: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

    finally:
        # Ensure the database connection is always closed.
        conn.close()


# --- Main Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)
    
    # ==============================================================================
# TrackWise Inventory Management System - Flask API
# ==============================================================================

# --- Imports ---
from flask import Flask, jsonify, request
import sqlite3

# --- Application Setup ---
app = Flask(__name__)
DATABASE = 'trackwise.db'


# --- Database Utility Function ---
def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    The connection is configured to return rows as dictionary-like objects.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --- API ROUTES ---

@app.route('/')
def index():
    """A simple route to confirm the server is running."""
    return "TrackWise API is running!"

# ... [Previous endpoints: /api/login, /api/products/lowstock, /api/sales/recent, /api/kpi/dashboard] ...
# (Keeping them collapsed for brevity, they are still part of the file)


# ======================= Add New Product Endpoint =======================
@app.route('/api/products', methods=['POST'])
def add_product():
    """
    Adds a new product to the Product table.
    Expects a JSON payload with all necessary product details.
    """
    # 1. Get the JSON data from the request body.
    try:
        data = request.get_json()
    except:
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    # 2. Extract product details from the JSON data.
    #    The form in the UI had more fields, but we only use what's in the DB schema.
    product_name = data.get('productName')
    description = data.get('description')
    quantity = data.get('initialQuantity')
    sale_price = data.get('salePrice')
    purchase_price = data.get('purchasePrice')
    supplier_id = data.get('supplierId') # Ensure the front-end sends this ID

    # 3. Validate that all required fields are present.
    required_fields = [product_name, quantity, sale_price, purchase_price]
    if not all(field is not None for field in required_fields):
        return jsonify({"success": False, "message": "Missing required product fields"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 4. Create the SQL INSERT statement with placeholders.
        sql = """
            INSERT INTO Product (ProductName, Description, QuantityInStock, SalePrice, PurchasePrice, SupplierID)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        # 5. Execute the statement with the product data.
        cursor.execute(sql, (product_name, description, quantity, sale_price, purchase_price, supplier_id))
        
        # 6. Commit the changes to the database.
        conn.commit()
        
        # 7. Get the ID of the newly created product.
        new_product_id = cursor.lastrowid

        # 8. Return a success response with the new product's ID.
        #    HTTP status 201 Created is appropriate for successful resource creation.
        return jsonify({
            "success": True,
            "message": "Product added successfully",
            "productId": new_product_id
        }), 201

    except sqlite3.IntegrityError as e:
        # This could happen if a foreign key (like SupplierID) is invalid.
        return jsonify({"success": False, "message": f"Database integrity error: {e}"}), 400
    except Exception as e:
        # Handle other potential database errors.
        print(f"Database error: {e}")
        return jsonify({"success": False, "message": "An internal server error occurred"}), 500
    finally:
        # Ensure the database connection is always closed.
        conn.close()


# --- Main Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)
    
    
    