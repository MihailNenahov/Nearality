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
    
    selected_location = None
    if request.method == 'POST' and 'location' in request.form:
        selected_location = request.form['location']
    
    # Get people who smiled at the logged-in user
    user_id = session['user_id']
    user_name = session['user_name']  # Retrieve the user's name from the session
    
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
    
    # Get people who the logged-in user smiled at
    cursor.execute("SELECT id_received FROM smilies WHERE id_sender = %s", (user_id,))
    smiled_people_ids = [row[0] for row in cursor.fetchall()]
    
    # Get all users in the selected location who have not been smiled at by the logged-in user
    if selected_location:
        cursor.execute("""
            SELECT * FROM user_info 
            WHERE id_location = %s AND id_user_info NOT IN %s
        """, (selected_location, tuple(smiled_people_ids) or (None,)))
        people_in_location = cursor.fetchall()
    else:
        people_in_location = []
    
    # Fetch chat history
    cursor.execute("""
        SELECT c.message, u.name
        FROM chat c
        JOIN user_info u ON c.id_user_info = u.id_user_info
        LIMIT 50  -- Adjust as needed
    """)
    chat_history = cursor.fetchall()
    
    return render_template('index.html', locations=locations, people_who_smiled=people_who_smiled, 
                           people_in_location=people_in_location, selected_location=selected_location, 
                           user_name=user_name, chat_history=chat_history)

@app.route('/give_smile', methods=['POST'])
def give_smile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    receiver_id = request.form['receiver_id']
    sender_id = session['user_id']

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO smilies (id_sender, id_received) VALUES (%s, %s)", (sender_id, receiver_id))

    return redirect(url_for('index'))

@socketio.on('chat message')
def handle_chat_message(msg):
    user_id = session.get('user_id')
    if user_id:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO chat (id_user_info, message) VALUES (%s, %s)", (user_id, msg))
        connection.commit()  # Commit the transaction
        emit('chat message', (msg, session['user_name']), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
