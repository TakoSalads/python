import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import requests
from datetime import date

# Finnhub API Key
API_KEY = "cu8pmh1r01qgljargg20cu8pmh1r01qgljargg2g"

def init_db():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()

    # Create the stocks table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    buy_price REAL,
                    date_added TEXT
                )''')

    # Check if the group_name column exists
    c.execute("PRAGMA table_info(stocks)")
    columns = [column[1] for column in c.fetchall()]
    if "group_name" not in columns:
        c.execute('ALTER TABLE stocks ADD COLUMN group_name TEXT')

    # Create the daily_prices table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS daily_prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    date TEXT,
                    price REAL
                )''')

    conn.commit()
    conn.close()



# Fetch live stock price from Finnhub
def get_stock_price(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("c")  # Current price
    except requests.exceptions.RequestException:
        return None

# Save stock data to the database
def save_stock():
    symbol = symbol_entry.get().upper()
    buy_price = buy_price_entry.get()
    date_added = date_added_entry.get()
    group_name = group_entry.get()

    if not symbol or not buy_price or not date_added or not group_name:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        buy_price = float(buy_price)
        conn = sqlite3.connect("stocks.db")
        c = conn.cursor()
        c.execute("INSERT INTO stocks (symbol, buy_price, date_added, group_name) VALUES (?, ?, ?, ?)",
                  (symbol, buy_price, date_added, group_name))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Saved {symbol} in group '{group_name}'")
        update_stock_list()
    except ValueError:
        messagebox.showerror("Input Error", "Buy price must be a number!")

def remove_stock():
    try:
        # Get the selected item
        selected_item = stock_list.get(stock_list.curselection())
        
        # Extract details from the selected item
        parts = selected_item.split("|")
        symbol = parts[0].strip()
        buy_price = float(parts[1].split(":")[1].strip().replace("$", ""))
        
        # Confirm removal with the user
        if messagebox.askyesno("Remove Stock", f"Are you sure you want to remove {symbol} (Buy Price: ${buy_price})?"):
            # Remove from the database using both symbol and buy_price
            conn = sqlite3.connect("stocks.db")
            c = conn.cursor()
            c.execute("DELETE FROM stocks WHERE symbol = ? AND buy_price = ?", (symbol, buy_price))
            conn.commit()
            conn.close()

            # Update the stock list display
            update_stock_list()

            messagebox.showinfo("Success", f"Stock {symbol} with Buy Price ${buy_price} removed successfully!")
    except IndexError:
        messagebox.showerror("Error", "No stock selected. Please select a stock to remove.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Fetch and display saved stocks
def update_stock_list():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT symbol, buy_price, date_added, group_name FROM stocks")
    stocks = c.fetchall()
    conn.close()

    # Clear listbox
    stock_list.delete(0, tk.END)

    # Add stocks with grouping and daily performance
    groups = {}
    group_totals = {}
    for stock in stocks:
        symbol, buy_price, date_added, group_name = stock
        current_price = get_stock_price(symbol)

        # Store daily price
        store_daily_price(symbol, current_price)

        # Calculate performance
        prev_price = get_previous_day_price(symbol)
        performance = round(current_price - prev_price, 2) if prev_price else "N/A"

        if current_price is not None:
            change = round(current_price - buy_price, 2)
            total_value = round(current_price, 2)
            if group_name not in group_totals:
                group_totals[group_name] = 0
            group_totals[group_name] += total_value

            # Add stock details to the group
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(
                f"{symbol} | Buy: ${buy_price} | Current: ${current_price} | Change: ${change} | Day Change: ${performance}"
            )
        else:
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(
                f"{symbol} | Buy: ${buy_price} | Current: N/A | Failed to fetch price."
            )

    # Display grouped stocks and their total evaluations
    for group, stocks in groups.items():
        stock_list.insert(tk.END, f"Group: {group} (Total Evaluation: ${round(group_totals[group], 2)})")
        for stock in stocks:
            stock_list.insert(tk.END, f"  {stock}")
        stock_list.insert(tk.END, "")  # Blank line between groups

# Store daily stock prices
def store_daily_price(symbol, price):
    if not price:
        return
    today = str(date.today())
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT id FROM daily_prices WHERE symbol = ? AND date = ?", (symbol, today))
    if not c.fetchone():
        c.execute("INSERT INTO daily_prices (symbol, date, price) VALUES (?, ?, ?)", (symbol, today, price))
    conn.commit()
    conn.close()

# Get the previous day's price
def get_previous_day_price(symbol):
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    c.execute("SELECT price FROM daily_prices WHERE symbol = ? ORDER BY date DESC LIMIT 2", (symbol,))
    prices = c.fetchall()
    conn.close()
    return prices[1][0] if len(prices) > 1 else None

# GUI Setup
root = tk.Tk()
root.title("Stock Tracker")

# Input fields
tk.Label(root, text="Stock Symbol:").grid(row=0, column=0)
symbol_entry = tk.Entry(root)
symbol_entry.grid(row=0, column=1)

tk.Label(root, text="Buy Price:").grid(row=1, column=0)
buy_price_entry = tk.Entry(root)
buy_price_entry.grid(row=1, column=1)

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
date_added_entry = tk.Entry(root)
date_added_entry.grid(row=2, column=1)

tk.Label(root, text="Group Name:").grid(row=3, column=0)
group_entry = tk.Entry(root)
group_entry.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Add Stock", command=save_stock).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Update List", command=update_stock_list).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Remove Stock", command=remove_stock).grid(row=6, column=0, columnspan=2)

# Stock List
stock_list = tk.Listbox(root, width=80, selectmode=tk.SINGLE)
stock_list.grid(row=7, column=0, columnspan=2)

# Initialize database and populate stock list
init_db()
update_stock_list()

root.mainloop()