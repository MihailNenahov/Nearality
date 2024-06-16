from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import psycopg2
from config import host, user, password, db_name

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Database connection function
def get_db_connection():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    return connection

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id_user_info FROM user_info WHERE name = %s AND password = %s", (name, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get all locations
    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()
    
    selected_location = None
    if request.method == 'POST':
        selected_location = request.form['location']
    
    # Get people who smiled at the logged-in user
    user_id = session['user_id']
    
    if selected_location:
        cursor.execute("""
            SELECT u.id_user_info, u.name 
            FROM user_info u
            JOIN smilies s ON u.id_user_info = s.id_sender
            WHERE s.id_received = %s AND u.id_location = %s
        """, (user_id, selected_location))
    else:
        cursor.execute("""
            SELECT u.id_user_info, u.name 
            FROM user_info u
            JOIN smilies s ON u.id_user_info = s.id_sender
            WHERE s.id_received = %s
        """, (user_id,))
    
    people_who_smiled = cursor.fetchall()
    
    # Get all users in the selected location
    if selected_location:
        cursor.execute("SELECT * FROM user_info WHERE id_location = %s", (selected_location,))
        people_in_location = cursor.fetchall()
    else:
        people_in_location = []
    
    return render_template('index.html', locations=locations, people_who_smiled=people_who_smiled, people_in_location=people_in_location, selected_location=selected_location)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('chat message')
def handle_message(msg):
    emit('chat message', msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
