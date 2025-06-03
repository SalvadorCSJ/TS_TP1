from src.transactions import Transaction
from src.transaction_type import TransactionType
from src.db_manager import DatabaseManager
from datetime import date

class Interface:

    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)

    # Define função para exibir primeira tela do menu 
    # responsável por identificar o usuário
    def menu_initial(self):
        pass
    
    # Define menu de ações para o usuário 
    def menu_user(self, user: str):
        # Opções do menu
        # Ver saldo
        # Adicionar transação
        # Editar transação
        # Excluir transação
        # Ver todas as transações
        # Ver transações por categoria
        # Ver transações por mês
        # Ver balanço mensal
        # Voltar ao menu inicial
        # Adicionar outras funcionalidades conforme necessário
        pass
    
    # Definir funções para cada uma das ações do menu do usuário
    # Exemplo:
    # Define menu de transação que permite ao usuário fornecer os 
    # dados necessários
    def menu_add_transaction(self, user: str):
        pass
    