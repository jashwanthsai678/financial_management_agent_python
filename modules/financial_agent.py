import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class FinancialManagementAgent:
    def __init__(self):
        self.transactions = pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Category', 'Type'])
        self.budget_categories = {
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
        self.income_sources = {
            'Salary': 50000, 
            'Freelance': 15000, 
            'Investments': 5000,
            'Business': 20000,
            'Other Income': 5000
        }
        self.model = None
        self.encoder = LabelEncoder()
        
    def add_transaction(self, date, description, amount, category, transaction_type):
        """Add a new transaction to the dataset"""
        new_transaction = pd.DataFrame({
            'Date': [date],
            'Description': [description],
            'Amount': [amount],
            'Category': [category],
            'Type': [transaction_type]
        })
        self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)
        
    def generate_sample_data(self, months=3):
        """Generate sample transaction data for testing with Indian context"""
        # ... (same as original code)
        expense_categories = list(self.budget_categories.keys())
        income_categories = list(self.income_sources.keys())
        start_date = datetime.now() - timedelta(days=30*months)
        
        # Generate expense transactions
        for i in range(80):
            date = start_date + timedelta(days=np.random.randint(0, 30*months))
            category = np.random.choice(expense_categories)
            
            # Set appropriate amount ranges for Indian context
            amount_ranges = {
                'Food & Dining': (100, 1500),
                'Transportation': (50, 1000),
                'Entertainment': (200, 3000),
                'Utilities': (500, 5000),
                'Shopping': (300, 8000),
                'Healthcare': (200, 5000),
                'Rent': (8000, 15000),
                'Education': (1000, 10000),
                'Personal Care': (100, 2000),
                'Investments': (1000, 10000),
                'Other': (50, 2000)
            }
            
            min_amt, max_amt = amount_ranges[category]
            amount = round(np.random.uniform(min_amt, max_amt), 2)
            
            descriptions = {
                'Food & Dining': ['Restaurant', 'Zomato Order', 'Swiggy Order', 'Grocery', 'Street Food', 'Cafe'],
                'Transportation': ['Petrol', 'Auto Rickshaw', 'Metro', 'Bus', 'Ola', 'Uber', 'Train'],
                'Entertainment': ['Movie Tickets', 'Netflix', 'Amazon Prime', 'Concert', 'Amusement Park'],
                'Utilities': ['Electricity Bill', 'Water Bill', 'Internet Bill', 'Mobile Recharge', 'Gas Cylinder'],
                'Shopping': ['Clothes', 'Electronics', 'Amazon', 'Flipkart', 'Myntra', 'Local Market'],
                'Healthcare': ['Doctor Visit', 'Medicines', 'Hospital', 'Pharmacy', 'Health Checkup'],
                'Rent': ['House Rent', 'Maintenance'],
                'Education': ['School Fees', 'Books', 'Tuition', 'Online Course'],
                'Personal Care': ['Salon', 'Spa', 'Gym', 'Yoga Class'],
                'Investments': ['Mutual Funds', 'Stocks', 'Fixed Deposit', 'PPF'],
                'Other': ['Gift', 'Donation', 'Miscellaneous']
            }
            description = np.random.choice(descriptions[category])
                
            self.add_transaction(
                date.strftime('%Y-%m-%d'),
                description,
                amount,
                category,
                'Expense'
            )
        
        # Generate income transactions
        for i in range(20):
            date = start_date + timedelta(days=np.random.randint(0, 30*months))
            category = np.random.choice(income_categories)
            
            amount_ranges = {
                'Salary': (40000, 80000),
                'Freelance': (5000, 30000),
                'Investments': (1000, 10000),
                'Business': (10000, 50000),
                'Other Income': (1000, 10000)
            }
            
            min_amt, max_amt = amount_ranges[category]
            amount = round(np.random.uniform(min_amt, max_amt), 2)
            
            descriptions = {
                'Salary': ['Monthly Salary', 'Paycheck'],
                'Freelance': ['Freelance Project', 'Consulting'],
                'Investments': ['Dividends', 'Interest', 'Capital Gains'],
                'Business': ['Business Revenue', 'Client Payment'],
                'Other Income': ['Bonus', 'Cashback', 'Rewards']
            }
            description = np.random.choice(descriptions[category])
                
            self.add_transaction(
                date.strftime('%Y-%m-%d'),
                description,
                amount,
                category,
                'Income'
            )
    
    def categorize_expenses(self):
        """Categorize expenses and return summary"""
        expenses = self.transactions[self.transactions['Type'] == 'Expense']
        if expenses.empty:
            return pd.DataFrame()
        
        # Convert date to datetime and extract month
        expenses['Date'] = pd.to_datetime(expenses['Date'])
        expenses['Month'] = expenses['Date'].dt.to_period('M')
        
        # Group by month and category
        summary = expenses.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)
        return summary
    
    def forecast_budget(self, future_months=3):
        """Forecast future budget needs based on historical data"""
        expenses = self.categorize_expenses()
        if expenses.empty:
            return pd.DataFrame()
        
        # Prepare data for forecasting
        forecast_data = {}
        for category in expenses.columns:
            # Use weighted average with more weight to recent months
            weights = np.arange(1, len(expenses) + 1)
            weighted_avg = np.average(expenses[category], weights=weights)
            forecast_data[category] = [weighted_avg] * future_months
        
        # Create future dates
        last_month = expenses.index[-1]
        future_dates = [last_month + i for i in range(1, future_months+1)]
        
        return pd.DataFrame(forecast_data, index=future_dates)
    
    def analyze_savings(self):
        """Analyze savings patterns and provide insights"""
        # Calculate monthly income and expenses
        expenses = self.transactions[self.transactions['Type'] == 'Expense']
        income = self.transactions[self.transactions['Type'] == 'Income']
        
        if expenses.empty or income.empty:
            return "Not enough data for savings analysis"
        
        expenses['Date'] = pd.to_datetime(expenses['Date'])
        income['Date'] = pd.to_datetime(income['Date'])
        
        expenses['Month'] = expenses['Date'].dt.to_period('M')
        income['Month'] = income['Date'].dt.to_period('M')
        
        monthly_expenses = expenses.groupby('Month')['Amount'].sum()
        monthly_income = income.groupby('Month')['Amount'].sum()
        
        # Calculate savings
        monthly_savings = monthly_income - monthly_expenses
        avg_savings = monthly_savings.mean()
        savings_rate = (avg_savings / monthly_income.mean()) * 100
        
        # Generate insights
        insights = []
        insights.append(f"Average monthly savings: ₹{avg_savings:,.2f}")
        insights.append(f"Savings rate: {savings_rate:.1f}% of your income")
        
        if savings_rate > 20:
            insights.append("Excellent savings rate! You're on track for financial security.")
        elif savings_rate > 10:
            insights.append("Good savings rate. Consider increasing it to 20% for better financial health.")
        else:
            insights.append("Your savings rate is low. Try to reduce unnecessary expenses.")
            
        # Identify top spending categories
        top_categories = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        if not top_categories.empty:
            insights.append(f"Your top spending category is {top_categories.index[0]} (₹{top_categories.iloc[0]:,.2f})")
            
            # Suggest ways to reduce spending in top category
            reduction_tips = {
                'Food & Dining': "Consider cooking at home more often and limiting restaurant visits to weekends.",
                'Transportation': "Explore public transport options or carpooling to reduce fuel costs.",
                'Entertainment': "Look for free or low-cost entertainment options in your community.",
                'Shopping': "Implement a 24-hour waiting period before making non-essential purchases.",
                'Rent': "If possible, consider moving to a more affordable area or getting a roommate.",
                'Utilities': "Turn off appliances when not in use and consider energy-efficient options."
            }
            
            if top_categories.index[0] in reduction_tips:
                insights.append(f"Tip: {reduction_tips[top_categories.index[0]]}")
        
        return "\n".join(insights)
    
    def build_ml_model(self):
        """Build a machine learning model for expense prediction"""
        expenses = self.transactions[self.transactions['Type'] == 'Expense']
        if expenses.empty or len(expenses) < 20:
            return None
            
        # Feature engineering
        expenses['Date'] = pd.to_datetime(expenses['Date'])
        expenses['DayOfWeek'] = expenses['Date'].dt.dayofweek
        expenses['DayOfMonth'] = expenses['Date'].dt.day
        expenses['Month'] = expenses['Date'].dt.month
        expenses['IsWeekend'] = expenses['Date'].dt.dayofweek.isin([5, 6]).astype(int)
        
        # Encode categories
        expenses['CategoryEncoded'] = self.encoder.fit_transform(expenses['Category'])
        
        # Prepare features and target
        features = expenses[['DayOfWeek', 'DayOfMonth', 'Month', 'IsWeekend', 'CategoryEncoded']]
        target = expenses['Amount']
        
        # Train model
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        return self.model.score(X_test, y_test)
    
    def predict_expense(self, day_of_week, day_of_month, month, is_weekend, category):
        """Predict expense amount for given parameters"""
        if self.model is None:
            return "Model not trained yet"
            
        # Encode category
        try:
            category_encoded = self.encoder.transform([category])[0]
        except:
            return "Category not recognized"
            
        # Make prediction
        features = np.array([[day_of_week, day_of_month, month, is_weekend, category_encoded]])
        prediction = self.model.predict(features)
        
        return round(prediction[0], 2)
    
    def generate_report(self):
        """Generate a comprehensive financial report"""
        report = "FINANCIAL MANAGEMENT REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Expense categorization
        expense_summary = self.categorize_expenses()
        if not expense_summary.empty:
            report += "EXPENSE CATEGORIZATION (Last 3 Months):\n"
            report += expense_summary.to_string()
            report += "\n\n"
        
        # Budget forecast
        forecast = self.forecast_budget()
        if not forecast.empty:
            report += "BUDGET FORECAST (Next 3 Months):\n"
            report += forecast.to_string()
            report += "\n\n"
        
        # Savings insights
        savings_insights = self.analyze_savings()
        report += "SAVINGS INSIGHTS:\n"
        report += savings_insights
        report += "\n\n"
        
        # Budget recommendations
        expenses = self.transactions[self.transactions['Type'] == 'Expense']
        if not expenses.empty:
            category_totals = expenses.groupby('Category')['Amount'].sum()
            report += "BUDGET RECOMMENDATIONS:\n"
            for category, budget in self.budget_categories.items():
                spent = category_totals.get(category, 0)
                if spent > 0:
                    percentage = (spent / budget) * 100
                    report += f"{category}: Budget ₹{budget:,.2f}, Spent ₹{spent:,.2f} ({percentage:.1f}%)\n"
                    if percentage > 100:
                        report += f"  - You've exceeded your budget by ₹{spent - budget:,.2f}\n"
                    elif percentage > 80:
                        report += f"  - You're close to your budget limit\n"
                    else:
                        report += f"  - You're within your budget\n"
            report += "\n"
        
        return report

    def get_summary_stats(self):
        """Get summary statistics for dashboard"""
        total_income = self.transactions[self.transactions['Type'] == 'Income']['Amount'].sum()
        total_expenses = self.transactions[self.transactions['Type'] == 'Expense']['Amount'].sum()
        net_savings = total_income - total_expenses
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_savings': net_savings
        }