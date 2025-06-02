import sys
import os
import pytest


from src.transaction_type import TransactionType

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
