from flask import Flask, render_template, request, jsonify
import psycopg2
from config import host, user, password, db_name

# Initialize the Flask application
app = Flask(__name__)

# Function to establish a connection to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    conn.autocommit = True  # Enable autocommit to avoid having to manually commit transactions
    return conn

# Define the route for the homepage
@app.route('/')
def index():
    try:
        # Establish a connection to the database
        connection = get_db_connection()
        # Create a cursor object to interact with the database
        with connection.cursor() as cursor:
            # Execute a query to fetch all locations
            cursor.execute("SELECT * FROM locations")
            locations = cursor.fetchall()  # Fetch all rows from the result set
        # Render the index.html template with the fetched locations
        return render_template('index.html', locations=locations)
    except Exception as ex:
        # Return an error message if an exception occurs
        return f"Error: {ex}"
    finally:
        # Ensure the database connection is closed
        if connection:
            connection.close()

# Define the route to get users in a selected location
@app.route('/get_users', methods=['POST'])
def get_users():
    location_id = request.form['location_id']
    try:
        # Establish a connection to the database
        connection = get_db_connection()
        # Create a cursor object to interact with the database
        with connection.cursor() as cursor:
            # Fetch the users associated with the selected location
            cursor.execute("SELECT * FROM user_info WHERE id_location = %s", (location_id,))
            users = cursor.fetchall()  # Fetch all rows from the result set
        # Return the users as a JSON response
        return jsonify(users)
    except Exception as ex:
        # Return an error message if an exception occurs
        return jsonify({"error": str(ex)})
    finally:
        # Ensure the database connection is closed
        if connection:
            connection.close()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for detailed error messages and auto-reloading
