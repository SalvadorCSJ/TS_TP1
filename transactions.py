from datetime import date

class TransactionType:

    def __init__(self, type_name: str):
        if type_name not in ["Receita", "Despesa"]:
            raise ValueError("Transaction type must be 'Receita' or 'Despesa'")
        self.type_name = type_name

    def get_type(self):
        return self.type_name
    


class Transaction:

    def __init__(self,date:date,description:str,amount:float,type:TransactionType, id:int):
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
    

    def print_transaction(self):
        print(f"Date: {self.date.strftime('%Y-%m-%d')}, Description: {self.description}, Amount: {self.amount}, Type: {self.type.type_name}")

