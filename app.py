from flask import Flask, render_template, request, jsonify, session, send_file
import pandas as pd
import json
from modules.financial_agent import FinancialManagementAgent
from modules.data_processor import DataProcessor
from modules.visualization import ChartGenerator
from modules.storage import DataStorage
import io
import os

app = Flask(__name__)
app.secret_key = 'financial_management_secret_key_2025'

# Initialize data storage
storage = DataStorage()

# Add custom Jinja2 filters
@app.template_filter('min')
def min_filter(a, b):
    return min(a, b)

@app.template_filter('max')
def max_filter(a, b):
    return max(a, b)

def get_agent(user_id='default'):
    """Get or create financial agent with persistent storage"""
    agent = FinancialManagementAgent()
    
    # Load data from storage
    agent.transactions = storage.load_transactions(user_id)
    agent.budget_categories = storage.load_budgets(user_id)
    agent.income_sources = storage.load_income_sources(user_id)
    
    # If no transactions exist, generate sample data
    if agent.transactions.empty:
        agent.generate_sample_data()
        save_agent(agent, user_id)
    
    return agent

def save_agent(agent, user_id='default'):
    """Save agent data to persistent storage"""
    storage.save_transactions(agent.transactions, user_id)
    storage.save_budgets(agent.budget_categories, user_id)
    storage.save_income_sources(agent.income_sources, user_id)

@app.route('/')
def dashboard():
    try:
        agent = get_agent()
        summary = agent.get_summary_stats()
        
        # Generate charts
        expense_summary = agent.categorize_expenses()
        expense_data = DataProcessor.expense_summary_to_json(expense_summary)
        pie_chart = ChartGenerator.create_expense_pie_chart(expense_data)
        trends_chart = ChartGenerator.create_monthly_trends_chart(agent.transactions)
        
        return render_template('dashboard.html', 
                             summary=summary,
                             pie_chart=pie_chart,
                             trends_chart=trends_chart)
    except Exception as e:
        return f"Error in dashboard: {str(e)}", 500

@app.route('/transactions')
def transactions():
    try:
        agent = get_agent()
        transactions_data = DataProcessor.transactions_to_json(agent.transactions)
        categories = list(agent.budget_categories.keys()) + list(agent.income_sources.keys())
        return render_template('transactions.html', 
                             transactions=transactions_data,
                             categories=categories)
    except Exception as e:
        return f"Error in transactions: {str(e)}", 500

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        agent = get_agent()
        data = request.json
        
        agent.add_transaction(
            data['date'],
            data['description'],
            float(data['amount']),
            data['category'],
            data['type']
        )
        
        # Save updated data
        save_agent(agent)
        
        return jsonify({'success': True, 'message': 'Transaction added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/forecast')
def forecast():
    try:
        agent = get_agent()
        forecast_data = agent.forecast_budget()
        forecast_json = DataProcessor.forecast_to_json(forecast_data)
        
        # Build ML model score
        model_score = agent.build_ml_model()
        
        # Create forecast chart
        forecast_chart = ChartGenerator.create_forecast_chart(forecast_json)
        
        return render_template('forecast.html', 
                             forecast=forecast_json,
                             model_score=model_score,
                             forecast_chart=forecast_chart,
                             categories=list(agent.budget_categories.keys()))
    except Exception as e:
        return f"Error in forecast: {str(e)}", 500

@app.route('/predict_expense', methods=['POST'])
def predict_expense():
    try:
        agent = get_agent()
        data = request.json
        
        prediction = agent.predict_expense(
            int(data['day_of_week']),
            int(data['day_of_month']),
            int(data['month']),
            int(data['is_weekend']),
            data['category']
        )
        
        return jsonify({'success': True, 'prediction': prediction})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/insights')
def insights():
    try:
        agent = get_agent()
        savings_insights = agent.analyze_savings()
        
        # Generate trends chart
        trends_chart = ChartGenerator.create_monthly_trends_chart(agent.transactions)
        
        return render_template('insights.html', 
                             insights=savings_insights,
                             trends_chart=trends_chart)
    except Exception as e:
        return f"Error in insights: {str(e)}", 500

@app.route('/budget')
def budget():
    try:
        agent = get_agent()
        
        # Calculate spent amounts
        expenses = agent.transactions[agent.transactions['Type'] == 'Expense']
        category_totals = expenses.groupby('Category')['Amount'].sum()
        
        budget_data = []
        for category, budget_amount in agent.budget_categories.items():
            spent = category_totals.get(category, 0)
            remaining = budget_amount - spent
            percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
            
            # Ensure percentage doesn't exceed 100 for display
            display_percentage = min(percentage, 100)
            
            budget_data.append({
                'category': category,
                'budget': budget_amount,
                'spent': spent,
                'remaining': remaining,
                'percentage': percentage,
                'display_percentage': display_percentage
            })
        
        return render_template('budget.html', budget_data=budget_data)
    except Exception as e:
        return f"Error in budget: {str(e)}", 500

@app.route('/update_budgets', methods=['POST'])
def update_budgets():
    try:
        agent = get_agent()
        data = request.json
        
        for category, budget in data.items():
            agent.budget_categories[category] = float(budget)
        
        # Save updated budgets
        save_agent(agent)
        
        return jsonify({'success': True, 'message': 'Budgets updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/generate_report')
def generate_report():
    try:
        agent = get_agent()
        report = agent.generate_report()
        
        # Return report as downloadable file
        output = io.BytesIO()
        output.write(report.encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name='financial_report.txt',
            mimetype='text/plain'
        )
    except Exception as e:
        return f"Error generating report: {str(e)}", 500

@app.route('/clear_data', methods=['POST'])
def clear_data():
    try:
        # Clear all data files
        user_id = 'default'
        data_files = [
            f'data/{user_id}_transactions.csv',
            f'data/{user_id}_budgets.json', 
            f'data/{user_id}_income.json'
        ]
        
        for file_path in data_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return jsonify({'success': True, 'message': 'Data cleared successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/generate_sample_data', methods=['POST'])
def generate_sample_data():
    try:
        # Clear existing data
        user_id = 'default'
        data_files = [
            f'data/{user_id}_transactions.csv',
            f'data/{user_id}_budgets.json',
            f'data/{user_id}_income.json'
        ]
        
        for file_path in data_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Create new agent with sample data (will auto-generate)
        agent = get_agent()
        
        return jsonify({'success': True, 'message': 'Sample data generated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)