import pandas as pd
import json
from pandas import Period

class DataProcessor:
    @staticmethod
    def transactions_to_json(transactions_df):
        """Convert transactions DataFrame to JSON format"""
        return transactions_df.to_dict('records')
    
    @staticmethod
    def expense_summary_to_json(expense_summary):
        """Convert expense summary to JSON format"""
        if expense_summary.empty:
            return {}
        
        # Convert Period index to string
        expense_summary_str = expense_summary.copy()
        expense_summary_str.index = expense_summary_str.index.astype(str)
        return expense_summary_str.to_dict()
    
    @staticmethod
    def forecast_to_json(forecast_df):
        """Convert forecast DataFrame to JSON format"""
        if forecast_df.empty:
            return {}
        
        # Convert Period index to string
        forecast_df_str = forecast_df.copy()
        forecast_df_str.index = forecast_df_str.index.astype(str)
        return forecast_df_str.to_dict()
    
    @staticmethod
    def serialize_period(obj):
        """Custom JSON serializer for pandas Period objects"""
        if isinstance(obj, Period):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")