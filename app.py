import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, date

from src.db_manager import DatabaseManager
from src.transactions import Transaction
from src.transaction_type import TransactionType

import sqlite3

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
    try:
        transactions_data = db_manager.get_all_transactions(username)
        return jsonify(format_transaction_rows(transactions_data)), 200
    except RuntimeError as e:
        app.logger.error(f"RuntimeError getting all transactions for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error getting all transactions for {username}: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    

@app.route('/users/<username>/transactions', methods=['POST'])
def add_user_transaction(username):
    """Adds a new transaction for a user."""
    if db_manager.check_username_availability(username):
        app.logger.warning(f"Add transaction attempt for non-existent user: {username}")
        return jsonify({"error": f"User '{username}' does not exist. Create the user first."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload. Request body is empty or not JSON."}), 400

    required_fields = ['date', 'description', 'category', 'amount', 'type']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        trans_date_str = data['date']
        trans_date_obj = datetime.strptime(trans_date_str, '%Y-%m-%d').date()

        trans_type_name = data['type']
        trans_type_obj = TransactionType(trans_type_name)

        transaction_amount = float(data['amount'])
        description = str(data['description'])
        category = str(data['category'])

        new_transaction = Transaction(
            date=trans_date_obj,
            description=description,
            category=category,
            amount=transaction_amount,
            type=trans_type_obj
        )

        transaction_id = db_manager.add_transaction(username, new_transaction)
        app.logger.info(f"Transaction {transaction_id} added for user: {username}")

        return jsonify({"message": f"Transaction added successfully.", "transactionId": transaction_id}), 200

    except ValueError as e:
        app.logger.warning(f"ValueError adding transaction for {username}: {str(e)}. Data: {data}")
        return jsonify({"error": f"Invalid data provided: {str(e)}"}), 400
    except sqlite3.OperationalError as e:
        app.logger.error(f"Database operational error adding transaction for {username}: {str(e)}")
        return jsonify({"error": "A database operational error occurred."}), 500
    except RuntimeError as e:
        app.logger.error(f"RuntimeError adding transaction for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error adding transaction for {username}: {str(e)}. Data: {data}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/users/<username>/transactions/<int:transaction_id>', methods=['PUT'])
def update_user_transaction(username, transaction_id):
    """Updates an existing transaction for a user."""
    if db_manager.check_username_availability(username):
        app.logger.warning(f"Update transaction attempt for non-existent user: {username}")
        return jsonify({"error": f"User '{username}' does not exist."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload. Request body is empty or not JSON."}), 400

    required_fields = ['date', 'description', 'category', 'amount', 'type']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields for update: {', '.join(missing_fields)}"}), 400

    try:
        trans_date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        trans_type_obj = TransactionType(data['type'])
        transaction_amount = float(data['amount'])
        description = str(data['description'])
        category = str(data['category'])

        updated_transaction = Transaction(
            date=trans_date_obj,
            description=description,
            category=category,
            amount=transaction_amount,
            type=trans_type_obj
        )

        db_manager.update_transaction_by_id(username, transaction_id, updated_transaction)
        app.logger.info(f"Transaction {transaction_id} updated for user: {username}")

        return jsonify({"message": f"Transaction ID {transaction_id} updated successfully."}), 200
    except ValueError as e:
        app.logger.warning(f"ValueError updating transaction {transaction_id} for {username}: {str(e)}. Data: {data}")
        return jsonify({"error": f"Invalid data provided: {str(e)}"}), 400
    except sqlite3.OperationalError as e:
        app.logger.error(f"Database operational error updating transaction {transaction_id} for {username}: {str(e)}")
        return jsonify({"error": "A database operational error occurred during update."}), 500
    except RuntimeError as e:
        app.logger.error(f"RuntimeError updating transaction {transaction_id} for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error updating transaction {transaction_id} for {username}: {str(e)}. Data: {data}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/users/<username>/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_user_transaction(username, transaction_id):
    """Deletes a transaction for a user."""
    if db_manager.check_username_availability(username):
        app.logger.warning(f"Delete transaction attempt for non-existent user: {username}")
        return jsonify({"error": f"User '{username}' does not exist."}), 404
    try:
        db_manager.delete_transaction_by_id(username, transaction_id)
        app.logger.info(f"Transaction {transaction_id} deleted for user: {username}")
        return jsonify({"message": f"Transaction ID {transaction_id} deleted successfully."}), 200
    except sqlite3.OperationalError as e:
        app.logger.error(f"Database operational error deleting transaction {transaction_id} for {username}: {str(e)}")
        return jsonify({"error": "A database operational error occurred during delete."}), 500
    except RuntimeError as e:
        app.logger.error(f"RuntimeError deleting transaction {transaction_id} for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error deleting transaction {transaction_id} for {username}: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    
@app.route('/users/<username>/transactions/category/<category_name>', methods=['GET'])
def get_user_transactions_by_category(username, category_name):
    """Gets transactions for a user filtered by category."""
    try:
        transactions_data = db_manager.get_category_transactions(username, category_name)
        return jsonify(format_transaction_rows(transactions_data)), 200
    except RuntimeError as e:
        app.logger.error(f"RuntimeError getting category '{category_name}' transactions for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error getting category '{category_name}' transactions for {username}: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/users/<username>/transactions/debits', methods=['GET'])
def get_user_debit_transactions(username):
    """Gets all debit transactions (Despesa) for a user."""
    try:
        transactions_data = db_manager.get_all_debits(username)
        return jsonify(format_transaction_rows(transactions_data)), 200
    except RuntimeError as e:
        app.logger.error(f"RuntimeError getting debit transactions for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error getting debit transactions for {username}: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/users/<username>/transactions/credits', methods=['GET'])
def get_user_credit_transactions(username):
    """Gets all credit transactions (Receita) for a user."""
    try:
        transactions_data = db_manager.get_all_credits(username)
        return jsonify(format_transaction_rows(transactions_data)), 200
    except RuntimeError as e:
        app.logger.error(f"RuntimeError getting credit transactions for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error getting credit transactions for {username}: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/users/<username>/transactions/month/<int:year>/<int:month>', methods=['GET'])
def get_user_transactions_by_month(username, year, month):
    """Gets transactions for a user filtered by month and year."""
    if not (1 <= month <= 12):
        return jsonify({"error": "Invalid month. Must be between 1 and 12."}), 400
    try:
        transactions_data = db_manager.get_month_transactions(username, month, year)
        return jsonify(format_transaction_rows(transactions_data)), 200
    except RuntimeError as e:
        app.logger.error(f"RuntimeError getting month {year}-{month} transactions for {username}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error getting month {year}-{month} transactions for {username}: {str(e)}")
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

