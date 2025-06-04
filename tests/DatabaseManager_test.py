from src.db_manager import DatabaseManager
from src.transactions import Transaction
from src.transaction_type import TransactionType
from datetime import date
import pytest
import os
from sqlite3 import OperationalError

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
        transaction = Transaction(date(2023, 10, 1), "Test Transaction", "Test Category", 100.0, TransactionType('Receita'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction)
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 1
        assert transactions[0][1] == "Test Transaction"
        assert transactions[0][2] == "Test Category"
        assert transactions[0][3] == 100.0
        assert transactions[0][4] == "Receita"   

    def test_update_transaction(self, db_manager):
        transaction = Transaction(date(2023, 10, 1), "Test Transaction", "Test Category", 100.0, TransactionType('Receita'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction)
        
        updated_transaction = Transaction(date(2023, 10, 2), "Updated Transaction", "Updated Category", 200.0, TransactionType('Despesa'))
        db_manager.update_transaction_by_id("test_user", 1, updated_transaction)
        
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 1
        assert transactions[0][1] == "Updated Transaction"
        assert transactions[0][2] == "Updated Category"
        assert transactions[0][3] == 200.0
        assert transactions[0][4] == "Despesa"
        

    def test_delete_transaction(self, db_manager):
        transaction = Transaction(date(2023, 10, 1), "Test Transaction", "Test Category", 100.0, TransactionType('Receita'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction)
        
        db_manager.delete_transaction_by_id("test_user", 1)
        
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 0

    def test_get_category_transactions(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Test Transaction 1", "Test Category", 100.0, TransactionType('Receita'))
        transaction2 = Transaction(date(2023, 10, 2), "Test Transaction 2", "Test Category", 200.0, TransactionType('Despesa'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        category_transactions = db_manager.get_category_transactions("test_user", "Test Category")
        assert len(category_transactions) == 2
        assert category_transactions[0][1] == "Test Transaction 1"
        assert category_transactions[1][1] == "Test Transaction 2"

    def test_get_all_transactions(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Test Transaction 1", "Test Category", 100.0, TransactionType('Receita'))
        transaction2 = Transaction(date(2023, 10, 2), "Test Transaction 2", "Test Category 2", 200.0, TransactionType('Despesa'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        transactions = db_manager.get_all_transactions("test_user")
        assert len(transactions) == 2
        assert transactions[0][1] == "Test Transaction 1"
        assert transactions[1][1] == "Test Transaction 2"

    def test_get_all_debits(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Debit Transaction 1", "Test Category", 100.0, TransactionType('Despesa'))
        transaction2 = Transaction(date(2023, 10, 2), "Credit Transaction 1", "Test Category", 200.0, TransactionType('Receita'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        debits = db_manager.get_all_debits("test_user")
        assert len(debits) == 1
        assert debits[0][1] == "Debit Transaction 1"
        assert debits[0][4] == "Despesa"

    def test_get_all_credits(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Credit Transaction 1", "Test Category", 100.0, TransactionType('Receita'))
        transaction2 = Transaction(date(2023, 10, 2), "Debit Transaction 1", "Test Category", 200.0, TransactionType('Despesa'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        credits = db_manager.get_all_credits("test_user")
        assert len(credits) == 1
        assert credits[0][1] == "Credit Transaction 1"
        assert credits[0][4] == "Receita"
        
    def test_get_month_transactions(self, db_manager):
        transaction1 = Transaction(date(2023, 10, 1), "Transaction October 1", "Test Category", 100.0, TransactionType('Receita'))
        transaction2 = Transaction(date(2023, 11, 1), "Transaction November 1", "Test Category", 200.0, TransactionType('Despesa'))
        db_manager.create_user_table("test_user")
        db_manager.add_transaction("test_user", transaction1)
        db_manager.add_transaction("test_user", transaction2)
        
        october_transactions = db_manager.get_month_transactions("test_user", 10, 2023)
        assert len(october_transactions) == 1
        assert october_transactions[0][1] == "Transaction October 1"
        
        november_transactions = db_manager.get_month_transactions("test_user", 11, 2023)
        assert len(november_transactions) == 1
        assert november_transactions[0][1] == "Transaction November 1"

    def test_multiple_users_isolated_tables(self, db_manager):
        
        db_manager.create_user_table("Ana")
        Transaction1 = Transaction(date(2025,1,1), "A1", "Trabalho", 100.0, TransactionType('Receita'))
        db_manager.add_transaction("Ana", Transaction1)

        db_manager.create_user_table("Saulo")
        Transaction2 = Transaction(date(2025,1,1), "B1", "Comida", 50.0, TransactionType('Despesa'))
        db_manager.add_transaction("Saulo",Transaction2)

        Ana_transactions = db_manager.get_all_transactions("Ana")
        Saulo_transactions = db_manager.get_all_transactions("Saulo")

        assert len(Ana_transactions) == 1
        assert len(Saulo_transactions) == 1
        assert Ana_transactions[0][1] == "A1"
        assert Saulo_transactions[0][1] == "B1"

    def test_get_all_debits_and_credits_empty_table(self,db_manager):
        db_manager.create_user_table("Empty")
    
        assert db_manager.get_all_debits("Empty") == []
        assert db_manager.get_all_credits("Empty") == []

    def test_get_transactions_with_invalid_user_raises_exception(self,db_manager):
        with pytest.raises(OperationalError):
            db_manager.get_all_debits("nonexisting_user")

    def test_create_table_without_connection_raises_exception(self, db_manager):
        db_manager.close()
        with pytest.raises(RuntimeError):
            db_manager.create_user_table("new_user")
    
    def test_commit_without_connection_raises_exception(self, db_manager):
        db_manager.close()
        with pytest.raises(RuntimeError):
            db_manager.commit()
