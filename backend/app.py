from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import psycopg2
from config import host, user, password, db_name
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)
logger = logging.getLogger(__name__)

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
        
        cursor.execute("SELECT id_user_info, name FROM user_info WHERE name = %s AND password = %s", (name, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]  # Store the user's name in the session
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

    # Get people who smiled at the logged-in user
    user_id = session['user_id']
    user_name = session['user_name']  # Retrieve the user's name from the session
    
    selected_location = None
    if request.method == 'POST' and 'location' in request.form:
        selected_location = request.form['location']
    else:
        selected_location = locations[0]
        cursor.execute("""
            update user_info set id_location = %s where id_user_info = %s
        """, (selected_location[0], user_id))
    
    
    cursor.execute("""
        SELECT u.id_user_info, u.name 
        FROM user_info u
        JOIN smilies s ON u.id_user_info = s.id_sender
        WHERE s.id_received = %s AND u.id_location = %s and u.id_user_info <> %s
    """, (user_id, selected_location[0], user_id))
    
    
    people_who_smiled = cursor.fetchall()

    # Get all users in the selected location who have not been smiled at by the logged-in user
    people_in_location = None
    if selected_location:
        cursor.execute("""
            SELECT * FROM user_info 
            WHERE id_location = %s  and id_user_info <> %s
        """, (selected_location[0], user_id))
        people_in_location = cursor.fetchall()
    else:
        people_in_location = []
    
    return render_template('index.html', locations=locations, people_who_smiled=people_who_smiled, people_in_location=people_in_location, selected_location=selected_location, user_name=user_name)

@app.route('/give_smile/<int:receiver_id>', methods=['POST'])
def give_smile(receiver_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    sender_id = session['user_id']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO smilies (id_sender, id_received) VALUES (%s, %s)", (sender_id, receiver_id))

    return jsonify({'message': 'Smile given successfully', 'receiver_id': receiver_id}), 200

@socketio.on('chat message')
def handle_chat_message(msg):
    emit('chat message', msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

