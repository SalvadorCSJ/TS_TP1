class TransactionType:

    def __init__(self, type_name: str):
        if type_name not in ["Receita", "Despesa"]:
            raise ValueError("Transaction type must be 'Receita' or 'Despesa'")
        self.type_name = type_name

    def get_type(self):
        return self.type_name
