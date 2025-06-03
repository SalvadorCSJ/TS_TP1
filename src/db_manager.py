import sqlite3
import os
from src.transactions import Transaction
from datetime import date


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()   

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
        
    def add_transaction(self, user:str , transaction: Transaction):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        query_parameters = (
            transaction.get_date(),
            transaction.get_description(),
            transaction.get_category(),
            transaction.get_amount(),
            transaction.get_type(),
            transaction.get_id()
        )
        insert_query = f"INSERT INTO {user} (date, description, category, amount, type, id) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(insert_query, query_parameters)
        self.commit()

    def update_transaction_by_id(self, user: str, transaction_id: int, updated_transaction: Transaction):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        query_parameters = (
            updated_transaction.get_date(),
            updated_transaction.get_description(),
            updated_transaction.get_category(),
            updated_transaction.get_amount(),
            updated_transaction.get_type(),
            transaction_id
            
        )
        update_query = f"UPDATE {user} SET date = ?, description = ?, category = ?, amount = ?, type = ? WHERE id = ?"
        self.cursor.execute(update_query, query_parameters)
        self.commit()
    
    def delete_transaction_by_id(self, user: str, transaction_id: int):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        delete_query = f"DELETE FROM {user} WHERE id = ?"
        self.cursor.execute(delete_query, (transaction_id,))
        self.commit()

    def get_category_transactions(self, user: str, category: str):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        select_query = f"SELECT * FROM {user} WHERE category = '{category}'"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    def get_all_transactions(self, user: str):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        select_query = f"SELECT * FROM {user}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    def get_all_debits(self, user: str):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        select_query = f"SELECT * FROM {user} WHERE type = 'Despesa'"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    def get_all_credits(self, user: str):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        select_query = f"SELECT * FROM {user} WHERE type = 'Receita'"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
    
    def get_month_transactions(self, user: str, month: int, year: int):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        select_query = f"SELECT * FROM {user} WHERE strftime('%m', date) = '{month:02d}' AND strftime('%Y', date) = '{year}'"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def commit(self):
        if not self.connection:
            raise RuntimeError("Database connection is not established.")
        self.connection.commit()

    def check_username_availability(self, user: str) -> bool:
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        check_username_availability_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{user}'"
        self.cursor.execute(check_username_availability_query)
        return self.cursor.fetchone() is None

    def create_user_table(self, user: str):
        if not self.cursor:
            raise RuntimeError("Database connection is not established.")
        if not self.check_username_availability(user):
            raise ValueError(f"Username '{user}' already exists.")
        create_table_query = f"CREATE TABLE IF NOT EXISTS {user} (date, description, category, amount, type, id)"
        self.cursor.execute(create_table_query)
        self.commit()