from datetime import date
from src.transaction_type import TransactionType

class Transaction:

    def __init__(self,date:date,description:str,category:str,amount:float,type:TransactionType):
        self.category = category
        self.date = date
        self.description = description
        self.amount = amount
        self.type = type

    def get_category(self):
        return self.category
    
    def get_date(self):     
        return self.date
    
    def get_description(self):  
        return self.description
    
    def get_amount(self):
        return self.amount

    def get_type(self):
        return self.type.get_type()

    
    def print_transaction(self):
        print(f"Date: {self.date.strftime('%Y-%m-%d')}, Description: {self.description}, Category: {self.category}, Amount: {self.amount}, Type: {self.type.type_name}")
