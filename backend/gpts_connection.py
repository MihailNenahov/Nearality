from flask import Flask, render_template, request
import psycopg2
from config import host, user, password, db_name

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    conn.autocommit = True
    return conn

@app.route('/')
def index():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM locations")
            locations = cursor.fetchall()
        return render_template('index.html', locations=locations)
    except Exception as ex:
        return f"Error: {ex}"
    finally:
        if connection:
            connection.close()

@app.route('/location/<int:location_id>')
def location_users(location_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM locations WHERE id_location = %s", (location_id,))
            location_name = cursor.fetchone()[0]
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
