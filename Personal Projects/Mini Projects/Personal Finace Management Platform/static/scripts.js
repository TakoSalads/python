document.addEventListener('DOMContentLoaded', () => {
    const budgetList = document.getElementById('budget-list');
    const expenseList = document.getElementById('expense-list');
    const addBudgetBtn = document.getElementById('add-budget-btn');
    const addExpenseBtn = document.getElementById('add-expense-btn');

    const budgets = [];
    const expenses = [];

    addBudgetBtn.addEventListener('click', () => {
        const name = prompt('Enter budget name:');
        const amount = prompt('Enter budget amount:');
        if (name && amount) {
            budgets.push({ name, amount });
            renderBudgets();
        }
    });

    addExpenseBtn.addEventListener('click', () => {
        const name = prompt('Enter expense name:');
        const amount = prompt('Enter expense amount:');
        if (name && amount) {
            expenses.push({ name, amount });
            renderExpenses();
        }
    });

    function renderBudgets() {
        budgetList.innerHTML = '';
        budgets.forEach(budget => {
            const li = document.createElement('li');
            li.textContent = `${budget.name}: $${budget.amount}`;
            budgetList.appendChild(li);
        });
    }

    function renderExpenses() {
        expenseList.innerHTML = '';
        expenses.forEach(expense => {
            const li = document.createElement('li');
            li.textContent = `${expense.name}: $${expense.amount}`;
            expenseList.appendChild(li);
        });
    }
});