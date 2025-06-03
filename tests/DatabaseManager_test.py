from src.db_manager import DatabaseManager
from src.transactions import Transaction
from src.transaction_type import TransactionType
from datetime import date
import pytest
import os

@pytest.fixture
def db_manager():
    db_path = ':memory:'
    db_manager = DatabaseManager(db_path)
    yield db_manager
    db_manager.close()
    if os.path.exists(db_path):
        os.remove(db_path)



class TestDatabaseManager:

    def test_create_db_manager(self,db_manager):
        assert db_manager.connection is not None
        assert db_manager.cursor is not None
        
    def test_create_table(self, db_manager):
        db_manager.create_user_table("test_user")
        assert db_manager.check_username_availability("test_user") == False

    def test_add_transaction(self, db_manager):
        transaction = Transaction(date(2023, 10, 1), "Test Transaction", "Test Category", 100.0, TransactionType('Receita'), 1)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction)
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 1
        assert transactions[0][1] == "Test Transaction"
        assert transactions[0][2] == "Test Category"
        assert transactions[0][3] == 100.0
        assert transactions[0][4] == "Receita"   

    def test_update_transaction(self, db_manager):
        transaction = Transaction(date(2023, 10, 1), "Test Transaction", "Test Category", 100.0, TransactionType('Receita'), 1)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction)
        
        updated_transaction = Transaction(date(2023, 10, 2), "Updated Transaction", "Updated Category", 200.0, TransactionType('Despesa'), 1)
        db_manager.update_transaction_by_id("test_user", 1, updated_transaction)
        
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 1
        assert transactions[0][1] == "Updated Transaction"
        assert transactions[0][2] == "Updated Category"
        assert transactions[0][3] == 200.0
        assert transactions[0][4] == "Despesa"
        assert transactions[0][5] == 1

    def test_delete_transaction(self, db_manager):
        transaction = Transaction(date(2023, 10, 1), "Test Transaction", "Test Category", 100.0, TransactionType('Receita'), 1)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction)
        
        db_manager.delete_transaction_by_id("test_user", 1)
        
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 0

    def test_get_category_transactions(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Test Transaction 1", "Test Category", 100.0, TransactionType('Receita'), 1)
        transaction2 = Transaction(date(2023, 10, 2), "Test Transaction 2", "Test Category", 200.0, TransactionType('Despesa'), 2)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        category_transactions = db_manager.get_category_transactions("test_user", "Test Category")
        assert len(category_transactions) == 2
        assert category_transactions[0][1] == "Test Transaction 1"
        assert category_transactions[1][1] == "Test Transaction 2"

    def test_get_all_transactions(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Test Transaction 1", "Test Category", 100.0, TransactionType('Receita'), 1)
        transaction2 = Transaction(date(2023, 10, 2), "Test Transaction 2", "Test Category 2", 200.0, TransactionType('Despesa'), 2)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 2
        assert transactions[0][1] == "Test Transaction 1"
        assert transactions[1][1] == "Test Transaction 2"

    def test_get_all_debits(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Debit Transaction 1", "Test Category", 100.0, TransactionType('Despesa'), 1)
        transaction2 = Transaction(date(2023, 10, 2), "Credit Transaction 1", "Test Category", 200.0, TransactionType('Receita'), 2)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        debits = db_manager.get_all_debits("test_user")
        assert len(debits) == 1
        assert debits[0][1] == "Debit Transaction 1"
        assert debits[0][4] == "Despesa"

    def test_get_all_credits(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Credit Transaction 1", "Test Category", 100.0, TransactionType('Receita'), 1)
        transaction2 = Transaction(date(2023, 10, 2), "Debit Transaction 1", "Test Category", 200.0, TransactionType('Despesa'), 2)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        credits = db_manager.get_all_credits("test_user")
        assert len(credits) == 1
        assert credits[0][1] == "Credit Transaction 1"
        assert credits[0][4] == "Receita"
        
    def test_get_month_transactions(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Transaction October 1", "Test Category", 100.0, TransactionType('Receita'), 1)
        transaction2 = Transaction(date(2023, 11, 1), "Transaction November 1", "Test Category", 200.0, TransactionType('Despesa'), 2)
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        october_transactions = db_manager.get_month_transactions("test_user", 10, 2023)
        assert len(october_transactions) == 1
        assert october_transactions[0][1] == "Transaction October 1"
        
        november_transactions = db_manager.get_month_transactions("test_user", 11, 2023)
        assert len(november_transactions) == 1
        assert november_transactions[0][1] == "Transaction November 1"
