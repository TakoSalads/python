#cd "D:\Code\python\Personal Projects\Personal Finace Management Platform\"
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage (replace with a database in production)
budgets = []
expenses = []

@app.route('/')
def index():
    return render_template('index.html', budgets=budgets, expenses=expenses)

@app.route('/add_budget', methods=['POST'])
def add_budget():
    name = request.form['name']
    amount = request.form['amount']
    if name and amount:
        budgets.append({'name': name, 'amount': amount})
    return redirect(url_for('index'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    name = request.form['name']
    amount = request.form['amount']
    if name and amount:
        expenses.append({'name': name, 'amount': amount})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
