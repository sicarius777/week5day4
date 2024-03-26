from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ugamvnpf:1MpfujWOdVdmpKYxBx8Bpxh7yt5BPmLh@raja.db.elephantsql.com/ugamvnpf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Define Ship model
class Ship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Ship {self.name}>'

# Routes for user CRUD operations
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.username = data['username']
        user.password = data['password']
        db.session.commit()
        return jsonify({'message': 'User updated'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Routes for ship CRUD operations
@app.route('/ships', methods=['GET'])
def get_ships():
    ships = Ship.query.all()
    return jsonify([{'id': ship.id, 'name': ship.name, 'model': ship.model} for ship in ships]), 200

@app.route('/ships/<int:ship_id>', methods=['GET'])
def get_ship(ship_id):
    ship = Ship.query.get(ship_id)
    if ship:
        return jsonify({'id': ship.id, 'name': ship.name, 'model': ship.model}), 200
    else:
        return jsonify({'error': 'Ship not found'}), 404

@app.route('/ships', methods=['POST'])
def add_ship():
    data = request.json
    new_ship = Ship(name=data['name'], model=data['model'])
    db.session.add(new_ship)
    db.session.commit()
    return jsonify({'id': new_ship.id, 'name': new_ship.name, 'model': new_ship.model}), 201

@app.route('/ships/<int:ship_id>', methods=['PUT'])
def update_ship(ship_id):
    ship = Ship.query.get(ship_id)
    if ship:
        data = request.json
        ship.name = data['name']
        ship.model = data['model']
        db.session.commit()
        return jsonify({'message': 'Ship updated'}), 200
    else:
        return jsonify({'error': 'Ship not found'}), 404

@app.route('/ships/<int:ship_id>', methods=['DELETE'])
def delete_ship(ship_id):
    ship = Ship.query.get(ship_id)
    if ship:
        db.session.delete(ship)
        db.session.commit()
        return jsonify({'message': 'Ship deleted'}), 200
    else:
        return jsonify({'error': 'Ship not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
