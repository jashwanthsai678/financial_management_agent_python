import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

class ChartGenerator:
    @staticmethod
    def create_expense_pie_chart(expense_data):
        """Create a pie chart for expense distribution"""
        if not expense_data:
            return None
            
        try:
            # Get the last month's data
            if isinstance(expense_data, dict):
                last_month_key = list(expense_data.keys())[-1]
                last_month_data = expense_data[last_month_key]
            else:
                last_month_data = expense_data.iloc[-1]
            
            # Ensure we have proper numeric data
            categories = []
            amounts = []
            
            for category, amount in last_month_data.items():
                categories.append(category)
                amounts.append(float(amount))
            
            fig = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=.3)])
            fig.update_layout(
                title='Expense Distribution',
                height=400
            )
            return fig.to_html(full_html=False)
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            return None
    
    @staticmethod
    def create_monthly_trends_chart(transactions_df):
        """Create monthly income, expenses, and savings chart"""
        try:
            expenses = transactions_df[transactions_df['Type'] == 'Expense']
            income = transactions_df[transactions_df['Type'] == 'Income']
            
            if expenses.empty or income.empty:
                return None
                
            expenses['Date'] = pd.to_datetime(expenses['Date'])
            income['Date'] = pd.to_datetime(income['Date'])
            
            expenses['Month'] = expenses['Date'].dt.to_period('M')
            income['Month'] = income['Date'].dt.to_period('M')
            
            monthly_expenses = expenses.groupby('Month')['Amount'].sum()
            monthly_income = income.groupby('Month')['Amount'].sum()
            monthly_savings = monthly_income - monthly_expenses
            
            # Convert Period index to string for JSON serialization
            months = [str(m) for m in monthly_income.index]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Income', 
                x=months, 
                y=monthly_income.values.tolist(), 
                marker_color='green'
            ))
            fig.add_trace(go.Bar(
                name='Expenses', 
                x=months, 
                y=monthly_expenses.values.tolist(), 
                marker_color='red'
            ))
            fig.add_trace(go.Bar(
                name='Savings', 
                x=months, 
                y=monthly_savings.values.tolist(), 
                marker_color='blue'
            ))
            
            fig.update_layout(
                title='Monthly Income, Expenses and Savings',
                xaxis_title='Month',
                yaxis_title='Amount (₹)',
                barmode='group',
                height=400
            )
            
            return fig.to_html(full_html=False)
        except Exception as e:
            print(f"Error creating trends chart: {e}")
            return None
    
    @staticmethod
    def create_forecast_chart(forecast_data):
        """Create a bar chart for budget forecast"""
        if not forecast_data:
            return None
            
        try:
            months = list(forecast_data.keys())
            categories_data = {}
            
            # Organize data by category
            for month, categories in forecast_data.items():
                for category, amount in categories.items():
                    if category not in categories_data:
                        categories_data[category] = []
                    categories_data[category].append(float(amount))
            
            fig = go.Figure()
            
            for category, amounts in categories_data.items():
                fig.add_trace(go.Bar(
                    name=category,
                    x=months,
                    y=amounts
                ))
            
            fig.update_layout(
                title='Budget Forecast (Next 3 Months)',
                xaxis_title='Month',
                yaxis_title='Amount (₹)',
                barmode='stack',
                height=400
            )
            
            return fig.to_html(full_html=False)
        except Exception as e:
            print(f"Error creating forecast chart: {e}")
            return None