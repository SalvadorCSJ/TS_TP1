from transactions import TransactionType,Transaction,TransactionManager
from datetime import date
import pytest

class TestTransactionType:
    
    def test_create_receipt_transaction_type(self):
      valid_type = TransactionType("Receita")
      assert valid_type.get_type() == "Receita"

    def test_create_expense_transaction_type(self):
      valid_type = TransactionType("Despesa")
      assert valid_type.get_type() == "Despesa"
        
    def test_invalid_transaction_type(self):
      try:
          TransactionType("InvalidType")
      except ValueError as e:
          assert str(e) == "Transaction type must be 'Receita' or 'Despesa'"

@pytest.fixture
def sample_transaction_1():
  transaction_category = "payment"
  transaction_date = date(2025, 5, 26)
  description = "Test Transaction"
  amount = 100.0
  type = TransactionType("Receita")
  id = 1
  cls = Transaction(transaction_date, description, transaction_category, amount, type, id)
  return cls

@pytest.fixture
def sample_transaction_2():
  transaction_category = "fuel"
  transaction_date = date(2025, 5, 27)
  description = "Test Transaction expense"
  amount = 50.0
  type = TransactionType("Despesa")
  id = 2
  cls = Transaction(transaction_date, description, transaction_category, amount, type, id)
  return cls

class TestTransaction:
  
  def test_create_transaction(self,sample_transaction_1):
    assert sample_transaction_1 is not None

  def test_edit_transaction_date(self,sample_transaction_1):
  
    new_date = date(2025, 6, 1)

    sample_transaction_1.edit_date(new_date)

    assert sample_transaction_1.date == new_date

  def test_edit_transaction_description(self,sample_transaction_1):
      
    new_description = "New Test Description"

    sample_transaction_1.edit_description(new_description)

    assert sample_transaction_1.description == new_description

  def test_edit_transaction_amount(self,sample_transaction_1):
    
    new_amount = 150.0

    sample_transaction_1.edit_amount(new_amount)

    assert sample_transaction_1.amount == new_amount

  def test_edit_transaction_type(self,sample_transaction_1):
      
    new_type = TransactionType("Despesa")

    sample_transaction_1.edit_type(new_type)

    assert sample_transaction_1.type.type_name == new_type.type_name

  def test_edit_transaction_category(self,sample_transaction_1):
      
    new_category = "rent"

    sample_transaction_1.edit_category(new_category)

    assert sample_transaction_1.category == new_category

class TestTransactionManager:

  def test_add_two_transactions(self, sample_transaction_1, sample_transaction_2):
    sample_manager = TransactionManager()

    sample_manager.add_transaction(sample_transaction_1)
    sample_manager.add_transaction(sample_transaction_2)

    assert sample_manager.transactions[0].id == 1
    assert sample_manager.transactions[1].id == 2

  def test_balance_with_two_transactions(self,sample_transaction_1,sample_transaction_2):
    sample_manager = TransactionManager()

    sample_manager.add_transaction(sample_transaction_1)
    sample_manager.add_transaction(sample_transaction_2)

    assert sample_manager.balance == 50
