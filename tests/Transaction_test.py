import sys
import os
import pytest


from src.transaction_type import TransactionType
from src.transactions import Transaction
from datetime import date

@pytest.fixture
def sample_transaction_1():
  transaction_category = "payment"
  transaction_date = date(2025, 5, 26)
  description = "Test Transaction"
  amount = 100.0
  type = TransactionType("Receita")
  cls = Transaction(transaction_date, description, transaction_category, amount, type)
  return cls

@pytest.fixture
def sample_transaction_2():
  transaction_category = "fuel"
  transaction_date = date(2025, 5, 27)
  description = "Test Transaction expense"
  amount = 50.0
  type = TransactionType("Despesa")
  cls = Transaction(transaction_date, description, transaction_category, amount, type)
  return cls

class TestTransaction:
  
  def test_create_receipt_transaction(self,sample_transaction_1):
    assert sample_transaction_1 is not None

  def test_create_expense_transaction(self,sample_transaction_2):
    assert sample_transaction_2 is not None

  def test_get_transaction_date(self,sample_transaction_1):
    assert sample_transaction_1.get_date() == date(2025, 5, 26)

  def test_get_transaction_description(self,sample_transaction_1):
      
    assert sample_transaction_1.get_description() == "Test Transaction"

  def test_get_transaction_amount(self,sample_transaction_1):
    
    assert sample_transaction_1.get_amount() == 100.0

  def test_get_transaction_category(self,sample_transaction_1):
    assert sample_transaction_1.get_category() == "payment"

  def test_get_transaction_type(self,sample_transaction_1):
    assert sample_transaction_1.get_type() == "Receita"

  def test_log_sample_transaction(self, sample_transaction_1):
    log_test = sample_transaction_1.log_transaction()
    assert log_test == "Date: 2025-05-26, Description: Test Transaction, Category: payment, Amount: 100.0, Type: Receita"

