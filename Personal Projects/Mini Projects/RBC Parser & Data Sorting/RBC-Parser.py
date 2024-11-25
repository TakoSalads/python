import pdfplumber
import pandas as pd
import re
import os
from fpdf import FPDF

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
        
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to parse extracted text
def parse_text(text):
    transactions = []
    lines = text.splitlines()  # Split text into lines

    current_date = None  # To keep track of the last date found

    # Iterate through lines and try to parse each one
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Look for date first as an indicator of a transaction line (assuming dates like '6Jun', '7Jun')
        match = re.match(r'^\d{1,2}[A-Za-z]{3}', line)
        if match:
            # Update current date
            current_date = match.group(0)
            line = line[len(current_date):].strip()  # Remove the date part from the line

        if current_date:
            # Attempt to extract the rest of the transaction details
            parts = re.split(r'(\d+\.\d{2})', line)  # Split by the amount pattern
            
            if len(parts) >= 2:
                description = parts[0].strip()  # Description is everything before the amount
                amount = parts[1].strip()  # Amount is the second part

                # Ensure amount is numeric before adding the transaction
                if re.match(r'^\d+\.\d{2}$', amount):
                    transactions.append({
                        "Date": current_date,
                        "Description": description,
                        "Withdrawals": float(amount)
                    })
    
    return transactions

# Function to save data to a CSV file
def save_to_csv(transactions, csv_path):
    df = pd.DataFrame(transactions)
    df.to_csv(csv_path, index=False)

# Function to generate a PDF report
def generate_pdf_report(transactions, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Transaction Report", ln=True, align="C")

    # Add transaction details
    for transaction in transactions:
        line = f"{transaction['Date']}: {transaction['Description']} - ${transaction['Withdrawals']:.2f}"
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(pdf_path)

# Main function
def main():
    pdf_path = r"D:\Code\python\Personal Projects\Mini Projects\RBC Parser & Data Sorting\07-08.pdf"  # Absolute path
    csv_path = r"D:\Code\python\Personal Projects\Mini Projects\RBC Parser & Data Sorting\Results\report.csv"  # Output CSV file path
    pdf_report_path = r"D:\Code\python\Personal Projects\Mini Projects\RBC Parser & Data Sorting\Results\transaction_report.pdf"  # Output PDF report path

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Parse text to extract transactions
    transactions = parse_text(text)
    print(transactions)    
    
    # Save transactions to CSV
    if transactions:
        save_to_csv(transactions, csv_path)
        print(f"Data extracted and saved to {csv_path}")

        # Generate a PDF report
        generate_pdf_report(transactions, pdf_report_path)
        print(f"PDF report generated and saved to {pdf_report_path}")
    else:
        print("No Transactions Registered")

if __name__ == "__main__":
    main()