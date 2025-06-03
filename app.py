import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, date

from src.db_manager import DatabaseManager

DB_FILE_PATH = 'finance.db'

app = Flask(__name__)
CORS(app)

db_manager = None

def initialize_database():
    """Initializes the database manager instance."""
    global db_manager
    try:
        app.logger.info(f"Attempting to connect to database at: {os.path.abspath(DB_FILE_PATH)}")
        db_manager = DatabaseManager(db_path=DB_FILE_PATH)
        app.logger.info(f"Successfully connected to database: {os.path.abspath(DB_FILE_PATH)}")
    except FileNotFoundError:
        app.logger.error(f"CRITICAL: Database file '{DB_FILE_PATH}' not found at {os.path.abspath(DB_FILE_PATH)}.")
        app.logger.error("The API cannot function without the database. Please ensure the file exists or the path is correct.")
    except Exception as e:
        app.logger.error(f"CRITICAL: An unexpected error occurred during database initialization: {str(e)}")

initialize_database()

def format_transaction_rows(rows):
    """Converts a list of transaction tuples from DB into a list of dictionaries."""
    columns = ['date', 'description', 'category', 'amount', 'type', 'id']
    formatted_transactions = []
    if rows:
        for row in rows:
            transaction_dict = dict(zip(columns, row))
            if isinstance(transaction_dict.get('date'), date):
                transaction_dict['date'] = transaction_dict['date'].isoformat()
            elif isinstance(transaction_dict.get('date'), str):
                pass
            formatted_transactions.append(transaction_dict)
    return formatted_transactions

@app.before_request
def check_db_connection():
    """Checks if the database manager is initialized before each request."""
    if db_manager is None:
        raise RuntimeError("Database is not initialized. Check server logs for details.")
    try:
        if db_manager.connection is None or db_manager.cursor is None:
            app.logger.warning("Database connection or cursor is None. Attempting to reconnect.")
            db_manager.connect()
    except Exception as e:
        app.logger.error(f"Error checking/re-establishing DB connection: {str(e)}")
        raise RuntimeError(f"Database connection issue: {str(e)}")


@app.route("/")
def home():
    return render_template("home.html")

@app.route('/users/<username>/transactions', methods=['GET'])
def get_user_transactions(username):
    """Gets all transactions for a user."""
    if db_manager.check_username_availability(username):
        app.logger.warning(f"Get transactions attempt for non-existent user: {username}")
        return jsonify({"error": f"User '{username}' does not exist."}), 404
    try:
        transactions_data = db_manager.get_all_transactions(username)
        return jsonify(format_transaction_rows(transactions_data)), 200
    except RuntimeError as e:
        app.logger.error(f"RuntimeError getting all transactions for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error getting all transactions for {username}: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    
@app.route('/users/<username>', methods=['GET'])
def create_user(username):
    """Creates a new user table."""
    try:
        db_manager.create_user_table(username)
        app.logger.info(f"User table created for: {username}")
        return jsonify({"message": f"User '{username}' table created successfully."}), 201
    except ValueError as e: # Username already exists
        app.logger.warning(f"Attempt to create existing user: {username} - {str(e)}")
        return jsonify({"error": str(e)}), 409 # Conflict
    except RuntimeError as e: # DB connection issue
        app.logger.error(f"RuntimeError during user creation for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error creating user {username}: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    if db_manager is None:
        app.logger.critical("Flask app cannot start because DatabaseManager failed to initialize.")
        app.logger.critical(f"Please check the database file path ('{DB_FILE_PATH}') and ensure it exists or can be accessed.")
    else:
        app.logger.info("Starting Flask development server...")
        app.run(host='0.0.0.0', port=5000, debug=True)

