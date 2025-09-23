from flask import Flask, jsonify, request

app = Flask(__name__)

#Simulated database (in memory)
users = {}

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Returns user info by user id"""
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    """adds a new user"""
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    user_id = len(users) + 1
    users[user_id] = {
        "id": user_id,
        "name": data['name'],
        "email": data['email']
    }
    return jsonify(users[user_id]), 201