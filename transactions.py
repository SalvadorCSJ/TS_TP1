from datetime import date

class TransactionType:

    def __init__(self, type_name: str):
        if type_name not in ["Receita", "Despesa"]:
            raise ValueError("Transaction type must be 'Receita' or 'Despesa'")
        self.type_name = type_name

    def get_type(self):
        return self.type_name

class Transaction:

    def __init__(self,date:date,description:str,category:str,amount:float,type:TransactionType, id:int):
        self.category = category
        self.date = date
        self.description = description
        self.amount = amount
        self.type = type
        self.id = id

    def edit_date(self,date:date):
        self.date = date
    
    def edit_description(self,description:str):
        self.description = description
    
    def edit_amount(self,amount:float):
        self.amount = amount
    
    def edit_type(self,type:TransactionType):
        self.type = type

    def edit_category(self,category:str):
        self.category = category
    
    def print_transaction(self):
        print(f"Date: {self.date.strftime('%Y-%m-%d')}, Description: {self.description}, Category: {self.category}, Amount: {self.amount}, Type: {self.type.type_name}")

class TransactionManager:
    def __init__(self):
        self.transactions = []
        self.balance = 0

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        if transaction.type.get_type() == "Despesa":
            self.balance -= transaction.amount
        elif transaction.type.get_type() == "Receita":
            self.balance += transaction.amount
        else:
            raise ValueError("Transaction type must be 'Receita' or 'Despesa'")
