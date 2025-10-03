import pandas as pd
import json
import os
from datetime import datetime

class DataStorage:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_transactions(self, transactions_df, user_id='default'):
        """Save transactions to CSV file"""
        file_path = os.path.join(self.data_dir, f'{user_id}_transactions.csv')
        transactions_df.to_csv(file_path, index=False)
    
    def load_transactions(self, user_id='default'):
        """Load transactions from CSV file"""
        file_path = os.path.join(self.data_dir, f'{user_id}_transactions.csv')
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Category', 'Type'])
    
    def save_budgets(self, budget_categories, user_id='default'):
        """Save budget categories to JSON file"""
        file_path = os.path.join(self.data_dir, f'{user_id}_budgets.json')
        with open(file_path, 'w') as f:
            json.dump(budget_categories, f)
    
    def load_budgets(self, user_id='default'):
        """Load budget categories from JSON file"""
        file_path = os.path.join(self.data_dir, f'{user_id}_budgets.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            return {
                'Food & Dining': 5000, 
                'Transportation': 3000, 
                'Entertainment': 2000, 
                'Utilities': 2500, 
                'Shopping': 3000, 
                'Healthcare': 1500, 
                'Rent': 10000,
                'Education': 4000,
                'Personal Care': 1500,
                'Investments': 5000,
                'Other': 2000
            }
    
    def save_income_sources(self, income_sources, user_id='default'):
        """Save income sources to JSON file"""
        file_path = os.path.join(self.data_dir, f'{user_id}_income.json')
        with open(file_path, 'w') as f:
            json.dump(income_sources, f)
    
    def load_income_sources(self, user_id='default'):
        """Load income sources from JSON file"""
        file_path = os.path.join(self.data_dir, f'{user_id}_income.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            return {
                'Salary': 50000, 
                'Freelance': 15000, 
                'Investments': 5000,
                'Business': 20000,
                'Other Income': 5000
            }