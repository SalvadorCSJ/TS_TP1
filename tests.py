from transactions import TransactionType,Transaction
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
def sample_transaction():
  transaction_date = date(2025, 5, 26)
  description = "Test Transaction"
  amount = 100.0
  type = TransactionType("Receita")
  id = 1
  cls = Transaction(transaction_date, description, amount, type, id)
  return cls

class TestTransaction:
  
  def test_create_transaction(self,sample_transaction):
    assert sample_transaction is not None



  def test_edit_transaction_date(self,sample_transaction):
  
    new_date = date(2025, 6, 1)

    sample_transaction.edit_date(new_date)

    assert sample_transaction.date == new_date

  def test_edit_transaction_description(self,sample_transaction):
      
    new_description = "New Test Description"

    sample_transaction.edit_description(new_description)

    assert sample_transaction.description == new_description

  def test_edit_transaction_amount(self,sample_transaction):
    
    new_amount = 150.0

    sample_transaction.edit_amount(new_amount)

    assert sample_transaction.amount == new_amount

  def test_edit_transaction_type(self,sample_transaction):
      
    new_type = TransactionType("Despesa")

    sample_transaction.edit_type(new_type)

    assert sample_transaction.type.type_name == new_type.type_name