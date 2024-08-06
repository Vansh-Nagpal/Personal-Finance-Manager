import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    type TEXT,
    category TEXT,
    amount REAL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')

conn.commit()



def add_user(name):
    cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
    conn.commit()
    return cursor.lastrowid

def add_transaction(user_id, date, transaction_type, category, amount, description):
    cursor.execute('''
    INSERT INTO transactions (user_id, date, type, category, amount, description)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, date, transaction_type, category, amount, description))
    conn.commit()

def view_transactions(user_id):
    cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
    transactions = cursor.fetchall()
    for transaction in transactions:
        print(transaction)

def main():
    print("Welcome to Personal Finance Manager")
    print("1. Add User")
    print("2. Add Transaction")
    print("3. View Transactions")
    choice = input("Select an option: ")

    if choice == '1':
        name = input("Enter your name: ")
        user_id = add_user(name)
        print(f"User {name} added with ID {user_id}")

    elif choice == '2':
        user_id = int(input("Enter User ID: "))
        date = input("Enter Date (YYYY-MM-DD): ")
        transaction_type = input("Enter Type (Income/Expense): ")
        category = input("Enter Category: ")
        amount = float(input("Enter Amount: "))
        description = input("Enter Description: ")
        add_transaction(user_id, date, transaction_type, category, amount, description)
        print("Transaction added.")

    elif choice == '3':
        user_id = int(input("Enter User ID: "))
        view_transactions(user_id)

if __name__ == "__main__":
    main()



import pandas as pd

def generate_report(user_id):
    cursor.execute('SELECT date, type, category, amount FROM transactions WHERE user_id = ?', (user_id,))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Date', 'Type', 'Category', 'Amount'])
    print(df.groupby(['Type', 'Category']).sum())


conn.close()