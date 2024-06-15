from flask import Flask, render_template, request
import psycopg2
from config import host, user, password, db_name  # Make sure config.py has your database credentials

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    conn.autocommit = True
    return conn

# Route for homepage
@app.route('/')
def index():
    try:
        # Connect to the database
        connection = get_db_connection()
        
        # Fetch all locations
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM locations")
            locations = cursor.fetchall()
        
        return render_template('index.html', locations=locations)
    
    except Exception as ex:
        return f"Error: {ex}"
    
    finally:
        if connection:
            connection.close()

# Route for displaying users in a selected location
@app.route('/location/<int:location_id>')
def location_users(location_id):
    try:
        # Connect to the database
        connection = get_db_connection()
        
        # Fetch location name
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM locations WHERE id_location = %s", (location_id,))
            location_name = cursor.fetchone()[0]
        
        # Fetch users in the selected location
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_info WHERE id_location = %s", (location_id,))
            users = cursor.fetchall()
        
        return render_template('location_users.html', location_name=location_name, users=users)
    
    except Exception as ex:
        return f"Error: {ex}"
    
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
