import pandas as pd
import re

# Define the path to your CSV file
input_csv_path = r"D:\Code\python\Personal Projects\Mini Projects\RBC Parser & Data Sorting\Results\report.csv"
deposits_csv_path = r"D:\Code\python\Personal Projects\Mini Projects\RBC Parser & Data Sorting\Results\deposits.csv"
withdrawals_csv_path = r"D:\Code\python\Personal Projects\Mini Projects\RBC Parser & Data Sorting\Results\withdrawals.csv"

# Define keywords for deposits and withdrawals
deposit_keywords = ["Deposit", "e-Transfer received", "ATMdeposit", "OnlineBankingtransfer", "e-Transfer received", "e-Transfer - Autodeposit",]

# Function to classify transactions
def classify_transaction(description):
    if any(keyword in description for keyword in deposit_keywords):
        return 'Deposit'
    elif not deposit_keywords:
        return 'Withdrawal'
    else:
        return 'Unknown'

# Function to extract amounts from descriptions
def extract_amount(description):
    match = re.search(r'\d+\.\d{2}', description)
    return float(match.group()) if match else 0.0

# Load the CSV file into a DataFrame
df = pd.read_csv(input_csv_path)

# Check if 'Description' column exists
if 'Description' not in df.columns:
    raise ValueError("The CSV file does not contain a 'Description' column.")

# Classify each transaction
df['Type'] = df['Description'].apply(classify_transaction)

# Extract amounts from descriptions
df['Amount'] = df['Description'].apply(extract_amount)

# Separate into deposits and withdrawals
df_deposits = df[df['Type'] == 'Deposit']
df_withdrawals = df[df['Type'] == 'Withdrawal']

# Save to separate CSV files
df_deposits.to_csv(deposits_csv_path, index=False)
df_withdrawals.to_csv(withdrawals_csv_path, index=False)

print(f"Deposits saved to {deposits_csv_path}")
print(f"Withdrawals saved to {withdrawals_csv_path}")
