from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname='your_dbname',
        user='your_user',
        password='your_password',
        host='your_host',
        port='your_port'
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM user_info WHERE name = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id_user_info']
            session['user_name'] = user['name']
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    
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
    smiled_people_ids = [row['id_received'] for row in cursor.fetchall()]
    
    # Get all users in the selected location who have not been smiled at by the logged-in user and are not the logged-in user
    if selected_location:
        cursor.execute("""
            SELECT * FROM user_info 
            WHERE id_location = %s AND id_user_info NOT IN %s AND id_user_info != %s
        """, (selected_location, tuple(smiled_people_ids) or (None,), user_id))
        people_in_location = cursor.fetchall()
    else:
        people_in_location = []
    
    return render_template('index.html', locations=locations, people_who_smiled=people_who_smiled, people_in_location=people_in_location, selected_location=selected_location, user_name=user_name)

@app.route('/give_smile', methods=['POST'])
def give_smile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    sender_id = session['user_id']
    receiver_id = request.form['receiver_id']

    if sender_id == int(receiver_id):
        return redirect(url_for('index'))  # Prevent smiling at oneself
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO smilies (id_sender, id_received) VALUES (%s, %s)", (sender_id, receiver_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
