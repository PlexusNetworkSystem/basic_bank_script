import sqlite3

# Connect to the database
conn = sqlite3.connect('bank.db')

# Create a cursor
c = conn.cursor()

# Create the accounts table
c.execute('''CREATE TABLE accounts
             (id INTEGER PRIMARY KEY, name TEXT, balance REAL)''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def create_account(name, balance):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
    account_id = c.lastrowid
    conn.commit()
    conn.close()
    return account_id

def deposit(account_id, amount):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    conn.commit()
    conn.close()

def withdraw(account_id, amount):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    balance = c.fetchone()[0]
    if balance >= amount:
        c.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def get_balance(account_id):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    balance = c.fetchone()[0]
    conn.close()
    return balance


while True:
    print("1. Create account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check balance")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        name = input("Enter name: ")
        balance = float(input("Enter starting balance: "))
        account_id = create_account(name, balance)
        print("Account created with ID", account_id)

    elif choice == '2':
        account_id = input("Enter account ID: ")
        amount = float(input("Enter amount to deposit: "))
        deposit(account_id, amount)
        print("Deposit successful")

    elif choice == '3':
        account_id = input("Enter account ID: ")
        amount = float(input("Enter amount to withdraw: "))
        success = withdraw(account_id, amount)
        if success:
            print("Withdrawal successful")
        else:
            print("Withdrawal failed: insufficient funds")

    elif choice == '4':
        account_id = input("Enter account ID: ")
        balance = get_balance(account_id)
        print("Balance:", balance)

    elif choice == '5':
        break

    else:
        print("Invalid choice")


