from flask import Flask, jsonify, request
from db import *

app = Flask(name)

# Sample data
locations = [
    {'id': 1, 'name': 'Location A'},
    {'id': 2, 'name': 'Location B'}
]

people = [
    {'id': 1, 'name': 'Alice', 'location_id': 1},
    {'id': 2, 'name': 'Bob', 'location_id': 1},
    {'id': 3, 'name': 'Charlie', 'location_id': 2}
]

chats = []
chat_id_counter = 1

# List of Locations
@app.route('/locations', methods=['GET'])
def get_locations():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM locations")

        rows = cursor.fetchall()  # Fetch all rows from the result set

        listOfLocs = ""
        for row in rows:
            listOfLocs += f"{row}\n"
        print(f"List of locations:{listOfLocs}")

        print("[info] Data added")
    return jsonify(locations)

# List of People in Location
@app.route('/locations/<int:location_id>/people', methods=['GET'])
def get_people_in_location(location_id):
    ###not done et todo: 1 must be replesed with users' chose 
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM user_info WHERE id_location = 1#<<—-
                           """)

        rows = cursor.fetchall()  # Fetch all rows from the result set

        listOfPeople = ""
        for row in rows:
            listOfPeople += f"{row}\n"
        print(f"List of locations:{listOfLocs}")

        print("[info] Data added")
    location_people = [person for person in people if person['location_id'] == location_id]
    return jsonify(location_people)

# Create Chat
@app.route('/chats/<int:person1>/<int:person2>', methods=['POST'])
def create_chat():
    global chat_id_counter
    chat = {
        'id': chat_id_counter,
        'messages': []
    }
    chats.append(chat)
    chat_id_counter += 1
    return jsonify(chat), 201

# Send Message
@app.route('/chats/<int:chat_id>/messages', methods=['POST'])
def send_message(chat_id):
    message = request.json.get('message')
    chat = next((chat for chat in chats if chat['id'] == chat_id), None)
    if chat:
        chat['messages'].append(message)
        return jsonify(chat)
    else:
        return jsonify({'error': 'Chat not found'}), 404

# Send Chat Information
@app.route('/chats/<int:chat_id>', methods=['GET'])
def get_chat_info(chat_id):
    chat = next((chat for chat in chats if chat['id'] == chat_id), None)
    if chat:
        return jsonify(chat)
    else:
        return jsonify({'error': 'Chat not found'}), 404

if name == 'main':
    app.run(port=8000)