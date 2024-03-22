import psycopg2

# Function to establish a connection to the database
def get_database_connection():
    try:
        # Replace the connection details with your actual ElephantSQL URL
        connection = psycopg2.connect(
            dbname='your_db_name',
            user='your_username',
            password='your_password',
            host='raja.db.elephantsql.com'
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
