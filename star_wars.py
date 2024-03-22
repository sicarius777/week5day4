from flask import Flask, jsonify, request
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Function to establish a connection to the database
def get_database_connection():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None
    
# Function to close the database connection
def close_database_connection(connection):
    if connection:
        connection.close()

# Function to execute SQL queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except psycopg2.Error as e:
        print("Error executing query:", e)
        connection.rollback()
    finally:
        cursor.close()

# Routes for user CRUD operations

@app.route('/users', methods=['GET'])
def get_users():
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            return jsonify(users), 200
        except psycopg2.Error as e:
            print("Error fetching users:", e)
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id=%s;", (user_id,))
            user = cursor.fetchone()
            if user:
                return jsonify(user), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except psycopg2.Error as e:
            print("Error fetching user:", e)
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

@app.route('/users', methods=['POST'])
def add_user():
    new_user_data = request.json
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *;", 
                           (new_user_data['username'], new_user_data['password']))
            new_user = cursor.fetchone()
            connection.commit()
            return jsonify(new_user), 201
        except psycopg2.Error as e:
            print("Error adding user:", e)
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

# Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    connection = get_database_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor()
        query = f"UPDATE users SET username = %s, password = %s WHERE id = %s"
        cursor.execute(query, (request.json['username'], request.json['password'], user_id))
        connection.commit()
        
        return jsonify({'message': 'User updated'}), 200
    except psycopg2.Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        close_database_connection(connection)

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = get_database_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    try:
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()
        
        return jsonify({'message': 'User deleted'}), 200
    except psycopg2.Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        close_database_connection(connection)

# Routes for ship CRUD operations

@app.route('/ships', methods=['GET'])
def get_ships():
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM ships")
            ships = cursor.fetchall()
            return jsonify(ships), 200
        except psycopg2.Error as e:
            print("Error fetching ships:", e)
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

@app.route('/ships/<int:ship_id>', methods=['GET'])
def get_ship(ship_id):
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM ships WHERE id=%s", (ship_id,))
            ship = cursor.fetchone()
            if ship:
                return jsonify(ship), 200
            else:
                return jsonify({'error': 'Ship not found'}), 404
        except psycopg2.Error as e:
            print("Error fetching ship:", e)
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

@app.route('/ships', methods=['POST'])
def add_ship():
    new_ship_data = request.json
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO ships (name, model) VALUES (%s, %s) RETURNING id",
                           (new_ship_data['name'], new_ship_data['model']))
            new_ship_id = cursor.fetchone()[0]
            connection.commit()
            new_ship_data['id'] = new_ship_id
            return jsonify(new_ship_data), 201
        except psycopg2.Error as e:
            print("Error adding ship:", e)
            connection.rollback()
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

@app.route('/ships/<int:ship_id>', methods=['PUT'])
def update_ship(ship_id):
    updated_ship_data = request.json
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE ships SET name = %s, model = %s WHERE id = %s",
                           (updated_ship_data['name'], updated_ship_data['model'], ship_id))
            connection.commit()
            updated_ship_data['id'] = ship_id
            return jsonify(updated_ship_data), 200
        except psycopg2.Error as e:
            print("Error updating ship:", e)
            connection.rollback()
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

@app.route('/ships/<int:ship_id>', methods=['DELETE'])
def delete_ship(ship_id):
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM ships WHERE id = %s", (ship_id,))
            connection.commit()
            return jsonify({'message': 'Ship deleted'}), 200
        except psycopg2.Error as e:
            print("Error deleting ship:", e)
            connection.rollback()
            return jsonify({'error': 'Internal server error'}), 500
        finally:
            close_database_connection(connection)
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

if __name__ == '__main__':
    app.run(debug=True)

